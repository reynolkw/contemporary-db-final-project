import requests

class OpenWeather:
    def __init__(self) -> None:
        pass

    API_KEY = "106f250f9988b2e174bda3e36df6a10d"

    def get_weather_at_coords(self, lat: float, lon: float):
        """Returns OpenWeather JSON data for input coordinates"""
        return requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.API_KEY}").json()