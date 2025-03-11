import os
import requests
from weather.models import WeatherData

API_KEY = os.getenv("WEATHER_API_KEY")
CITIES = ["Kyiv", "Berlin", "Madrid", "Warsaw", "Oslo", "Ottawa", "London", "Barcelona", "Cairo", "Athens"]
BASE_URL = "https://api.weatherapi.com/v1/current.json"


def fetch_weather(city):
    """Fetch weather for one city."""
    params = {
        "key": API_KEY,
        "q": city
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        return {
            "city": data["location"]["name"],
            "temperature": data["current"]["temp_c"],
            "humidity": data["current"]["humidity"],
            "wind_speed": data["current"]["wind_kph"],
            "description": data["current"]["condition"]["text"],
            "pressure": data["current"]["pressure_mb"],
            "feels_like": data["current"]["feelslike_c"],
        }
    return None


def fetch_weather_data():
    """Fetch weather for all cities and save to database."""
    if not API_KEY:
        raise ValueError("Cannot found WEATHER_API_KEY!")

    for city in CITIES:
        weather = fetch_weather(city)
        if weather:
            WeatherData.objects.create(
                city=weather["city"],
                temperature=weather["temperature"],
                humidity=weather["humidity"],
                wind_speed=weather["wind_speed"],
                description=weather["description"]
            )
