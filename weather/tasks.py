from celery import shared_task
from weather.services import fetch_weather_data


@shared_task(priority="high_priority")
def update_weather():
    fetch_weather_data()
