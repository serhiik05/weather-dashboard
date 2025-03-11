from django.urls import path, include
from rest_framework.routers import DefaultRouter
from weather.views import WeatherViewSet

app_name = "weather"

router = DefaultRouter()
router.register("weather", WeatherViewSet, basename="weather")

urlpatterns = [
    path("", include(router.urls)),
    path("weather/latest/", WeatherViewSet.as_view({'get': 'get_latest_weather'}), name="latest-weather"),
    path("weather/average/<str:pk>/", WeatherViewSet.as_view({'get': 'get_average_weather'}), name="average-weather"),
    path("weather/stats/<str:pk>/", WeatherViewSet.as_view({'get': 'get_weather_stats'}), name="weather-stats"),
]