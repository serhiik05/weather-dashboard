from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Avg, Min, Max
from weather.models import WeatherData
from weather.serializers import WeatherSerializer
from weather.tasks import update_weather


class WeatherViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows retrieving weather data."""

    queryset = WeatherData.objects.all().order_by("-timestamp")
    serializer_class = WeatherSerializer

    def list(self, request):
        """Get the latest 25 weather records (cached for 5 minutes)."""

        cache_key = "latest_weather"
        cached_data = cache.get(cache_key)

        if not cached_data:
            queryset = self.get_queryset()[:25]
            serializer = self.get_serializer(queryset, many=True)
            cache.set(cache_key, serializer.data, timeout=300)
            update_weather.delay()
            return Response(serializer.data)

        return Response(cached_data)

    def retrieve(self, request, pk=None):
        """Get weather data for a specific city (cached for 10 minutes)."""

        cache_key = f"weather_{pk}"
        cached_data = cache.get(cache_key)

        if not cached_data:
            weather_data = WeatherData.objects.filter(city__iexact=pk).order_by("-timestamp")[:7]
            if not weather_data.exists():
                return Response({"error": "No data found"}, status=404)

            serializer = self.get_serializer(weather_data, many=True)
            cache.set(cache_key, serializer.data, timeout=600)
            update_weather.delay()

            return Response(serializer.data)

        return Response(cached_data)

    def get_latest_weather(self, request):
        """Get the latest weather data for
        all tracked cities (cached for 10 minutes)."""

        cache_key = "latest_weather_all"
        cached_data = cache.get(cache_key)

        if not cached_data:
            cities = WeatherData.objects.values_list("city", flat=True).distinct()
            latest_weather = [WeatherData.objects.filter(city=city).order_by("-timestamp").first() for city in cities]
            serializer = self.get_serializer([w for w in latest_weather if w], many=True)
            cache.set(cache_key, serializer.data, timeout=600)
            update_weather.delay()

            return Response(serializer.data)

        return Response(cached_data)

    def get_average_weather(self, request, pk=None):
        """Get the average temperature, humidity, and wind speed for a city (cached for 10 minutes)."""

        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        cache_key = f"average_weather_{pk}_{start_date}_{end_date}"
        cached_data = cache.get(cache_key)

        if not cached_data:
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

            result = {"city": pk, **avg_data}
            cache.set(cache_key, result, timeout=600)
            update_weather.delay()

            return Response(result)

        return Response(cached_data)

    def get_weather_stats(self, request, pk=None):
        """Get min/max temperature, humidity, and wind speed
        for a city (cached for 20 minutes)."""

        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        cache_key = f"weather_stats_{pk}_{start_date}_{end_date}"
        cached_data = cache.get(cache_key)

        if not cached_data:
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

            result = {"city": pk, **stats_data}
            cache.set(cache_key, result, timeout=1200)
            update_weather.delay()

            return Response(result)

        return Response(cached_data)