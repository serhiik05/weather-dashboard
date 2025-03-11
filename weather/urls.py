from django.urls import path, include
from rest_framework.routers import DefaultRouter
from weather.views import WeatherViewSet

app_name = "weather"

router = DefaultRouter()
router.register("weather", WeatherViewSet, basename="weather")

urlpatterns = [
    path("", include(router.urls)),
]
