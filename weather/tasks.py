from celery import shared_task

from weather.services import update_weather_data


@shared_task(priority="high_priority")
def update_weather():
    """Celery task to update weather data and clear only relevant cache entries."""

    updated_cities = update_weather_data()
    return f"Updated cities: {", ".join(updated_cities)}" if updated_cities else "No updates."
