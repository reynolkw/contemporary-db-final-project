from mongodb import dbclient
from pymongo.mongo_client import MongoClient
from openweather import OpenWeather
from datetime import datetime, timedelta, UTC
import random
import time

class CrosleyWeather:
    def __init__(self, dbclient: MongoClient, openweather: OpenWeather) -> None:
        self.dbclient = dbclient
        self.openweather = openweather

    LATITUDE = 39.133620
    LONGITUDE = -84.520190

    def get_weather(self):
        return self.openweather.get_weather_at_coords(self.LATITUDE, self.LONGITUDE)
    
    def create_weather_document(self, weather_json):
        weather_collection = self.dbclient["CrosleyWeather"]["weather"]
        weather_collection.insert_one(weather_json)

    def update_forecast_document(self):
        weather_collection = self.dbclient["CrosleyWeather"]["weather"]
        
        current_time = datetime.now(UTC)
        one_hour_ago = current_time - timedelta(hours=1)

        pipeline = [
            {'$match': {'dt': {'$gte': int(one_hour_ago.timestamp())}}},
            {'$group': {
                '_id': None,
                'average_temp': {'$avg': '$main.temp'}
            }}
        ]

        result = list(weather_collection.aggregate(pipeline))
        if not result:
            print("No data found for the last hour.")
            exit()

        average_temp = result[0]['average_temp']

        if current_time.hour < 12:
            forecasted_temp = average_temp + random.uniform(0, 1)
        else:
            forecasted_temp = average_temp - random.uniform(0, 1)

        
        def poll(self):
            weather_json = self.get_weather()
            self.create_weather_document(weather_json)

cw = CrosleyWeather(dbclient, OpenWeather())

while True:
    cw.poll()
    # Poll every 10 minutes
    time.sleep(600)