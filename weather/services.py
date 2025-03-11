import os
import requests
from django.core.cache import cache
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


def update_weather_data():
    """Fetch weather for all cities, update the database, and clear the cache.
    Returns a list of updated cities."""
    updated_cities = []

    for city in CITIES:
        weather = fetch_weather(city)
        if weather:
            WeatherData.objects.update_or_create(
                city=weather["city"],
                defaults={
                    "temperature": weather["temperature"],
                    "humidity": weather["humidity"],
                    "wind_speed": weather["wind_speed"],
                    "description": weather["description"],
                    "pressure": weather["pressure"],
                    "feels_like": weather["feels_like"],
                }
            )
            updated_cities.append(city.lower())

    if updated_cities:
        cache.delete_many([f"weather_{city}" for city in updated_cities])

    return updated_cities
