from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Avg, Min, Max
from weather.models import WeatherData
from weather.serializers import WeatherSerializer


class WeatherViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows retrieving weather data."""

    queryset = WeatherData.objects.all().order_by("-timestamp")
    serializer_class = WeatherSerializer

    def list(self, request):
        """Get the latest 25 weather records."""

        queryset = self.get_queryset()[:25]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Get weather data for a specific city."""

        weather_data = WeatherData.objects.filter(city__iexact=pk).order_by("-timestamp")[:7]
        if not weather_data:
            return Response({"error": "No data found"}, status=404)

        serializer = self.get_serializer(weather_data, many=True)
        return Response(serializer.data)

    def get_latest_weather(self, request):
        """Get the latest weather data for all tracked cities."""

        cities = WeatherData.objects.values_list("city", flat=True).distinct()
        latest_weather = [WeatherData.objects.filter(city=city).order_by("-timestamp").first() for city in cities]
        serializer = self.get_serializer([w for w in latest_weather if w], many=True)
        return Response(serializer.data)

    def get_average_weather(self, request, pk=None):
        """Get the average temperature, humidity, and wind speed for a city."""

        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        weather_data = WeatherData.objects.filter(city__iexact=pk)

        if start_date and end_date:
            weather_data = weather_data.filter(timestamp__date__range=[start_date, end_date])

        if not weather_data.exists():
            return Response({"error": "No data found"}, status=404)

        avg_data = weather_data.aggregate(
            avg_temperature=Avg("temperature"),
            avg_humidity=Avg("humidity"),
            avg_wind_speed=Avg("wind_speed"),
        )

        return Response({"city": pk, **avg_data})

    def get_weather_stats(self, request, pk=None):
        """Get min/max temperature, humidity, and wind speed for a city."""

        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        weather_data = WeatherData.objects.filter(city__iexact=pk)

        if start_date and end_date:
            weather_data = weather_data.filter(timestamp__date__range=[start_date, end_date])

        if not weather_data.exists():
            return Response({"error": "No data found"}, status=404)

        stats_data = weather_data.aggregate(
            min_temperature=Min("temperature"),
            max_temperature=Max("temperature"),
            min_humidity=Min("humidity"),
            max_humidity=Max("humidity"),
            min_wind_speed=Min("wind_speed"),
            max_wind_speed=Max("wind_speed"),
        )

        return Response({"city": pk, **stats_data})
