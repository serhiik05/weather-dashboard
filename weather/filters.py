import django_filters
from weather.models import WeatherData


class WeatherFilter(django_filters.FilterSet):
    """Advanced filtering for weather data."""

    start_date = django_filters.DateFilter(field_name="timestamp", lookup_expr="gte", label="Start Date (YYYY-MM-DD)")
    end_date = django_filters.DateFilter(field_name="timestamp", lookup_expr="lte", label="End Date (YYYY-MM-DD)")
    city = django_filters.CharFilter(field_name="city", lookup_expr="iexact", label="City (case insensitive)")
    min_temperature = django_filters.NumberFilter(field_name="temperature", lookup_expr="gte", label="Min Temperature (°C)")
    max_temperature = django_filters.NumberFilter(field_name="temperature", lookup_expr="lte", label="Max Temperature (°C)")
    min_humidity = django_filters.NumberFilter(field_name="humidity", lookup_expr="gte", label="Min Humidity (%)")
    max_humidity = django_filters.NumberFilter(field_name="humidity", lookup_expr="lte", label="Max Humidity (%)")
    min_wind_speed = django_filters.NumberFilter(field_name="wind_speed", lookup_expr="gte", label="Min Wind Speed (km/h)")
    max_wind_speed = django_filters.NumberFilter(field_name="wind_speed", lookup_expr="lte", label="Max Wind Speed (km/h)")

    class Meta:
        model = WeatherData
        fields = [
            "city",
            "start_date",
            "end_date",
            "min_temperature",
            "max_temperature",
            "min_humidity",
            "max_humidity",
            "min_wind_speed",
            "max_wind_speed",
        ]
