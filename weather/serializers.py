from rest_framework import serializers
from weather.models import WeatherData


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = "__all__"
