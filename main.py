from mongodb import dbclient
from pymongo.mongo_client import MongoClient
from openweather import OpenWeather
from datetime import datetime, timedelta, UTC
import random
import time
from completions import get_forecast_summary

class CrosleyWeather:
    def __init__(self, dbclient: MongoClient, openweather: OpenWeather) -> None:
        print("INITIALIZING...")
        self.LATITUDE = 39.133620
        print(f"LATITUDE: {self.LATITUDE}")
        self.LONGITUDE = -84.520190
        print(f"LONGITUDE: {self.LONGITUDE}")
        self.dbclient = dbclient
        self.openweather = openweather
        self.runtime_current_time = datetime.now(UTC)
        self.time_resolution = 0.5 #minutes
        print(f"TIME RESOLUTION: {self.time_resolution} MINUTES")
        self.cutoff_datetime = self.runtime_current_time - timedelta(minutes=60)
        print(f"CUTOFF TIMESTAMP: {self.cutoff_datetime.timestamp()}")

    def get_weather(self):
        return self.openweather.get_weather_at_coords(self.LATITUDE, self.LONGITUDE)
    
    def create_weather_document(self, weather_json):
        weather_collection = self.dbclient["CrosleyWeather"]["weather"]
        result = weather_collection.insert_one(weather_json)
        print(f"CREATED WEATHER DOCUMENT ({result.inserted_id})\n")

    def update_forecast_document(self):
        weather_collection = self.dbclient["CrosleyWeather"]["weather"]
        
        pipeline = [
            {'$match': {'dt': {'$gte': int(self.cutoff_datetime.timestamp())}}},
            {'$group': {
                '_id': None,
                'average_temp': {'$avg': '$main.temp'},
                'average_humidity': {'$avg': '$main.humidity'},
                'average_visibility': {'$avg': '$visibility'},
                'average_wind': {'$avg': '$wind.speed'},
                'unique_descriptions': {'$addToSet': '$weather.description'},
            }}
        ]

        result = list(weather_collection.aggregate(pipeline))
        if not result:
            print(f"NO DATA FOUND FOR THE LAST {self.time_resolution} HOUR.")
            exit()

        average_temp = result[0]["average_temp"]

        if self.runtime_current_time.hour < 12:
            forecasted_temp = average_temp + random.uniform(0, 1)
        else:
            forecasted_temp = average_temp - random.uniform(0, 1)

        forecast = {
            "next_hour_temp_farenheit": (forecasted_temp - 273.15) * 9/5 + 32,
        }

        forecast = forecast | get_forecast_summary(forecasted_temp, result[0])

        forecast_collection = self.dbclient["CrosleyWeather"]["forecast"]
        query = {"_id": self.runtime_current_time.strftime('%Y%m%d%H')}
        result = forecast_collection.update_one(query, {"$set": forecast}, upsert=True)

        print(f"UPSERTED FORECAST DOCUMENT.\n")

    def get_forecast_document(self):
        forecast_collection = self.dbclient["CrosleyWeather"]["forecast"]
        filter = {"_id": self.runtime_current_time.strftime('%Y%m%d%H')}
        return forecast_collection.find_one(filter)

    def delete_old_weather_documents(self):
        """Delete weather documents that are older than one hour"""
        weather_collection = self.dbclient["CrosleyWeather"]["weather"]

        result = weather_collection.delete_many({"timestamp": {"$lt": self.cutoff_datetime}})

        print(f"\nDELETED {result.deleted_count} DOCUMENTS OLDER THAN ONE HOUR.")

    def poll(self):
        print("\nPOLLING...\n")
        self.runtime_current_time = datetime.now(UTC)
        print(f"CURRENT TIME: {self.runtime_current_time}")
        weather_json = self.get_weather()
        print("RETRIEVED WEATHER DATA FROM OPENWEATHER.")
        self.create_weather_document(weather_json)
        self.update_forecast_document()

        forecast = self.get_forecast_document()
        print(f"FORECASTED NEXT HOUR: {forecast.get('next_hour_temp_farenheit'):.2g}F")
        print(f"CLOUDS: {forecast.get('clouds')}")
        print(f"HUMIDITY: {forecast.get('humidity')}")
        print(f"TEMPERATURE: {forecast.get('temperature')}")
        print(f"VISIBILITY: {forecast.get('visibility')}")
        print(f"WIND: {forecast.get('wind')}")

        self.delete_old_weather_documents()

cw = CrosleyWeather(dbclient, OpenWeather())

while True:
    cw.poll()
    time.sleep(cw.time_resolution*60)