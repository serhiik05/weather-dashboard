from django.core.cache import cache
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from requests import Request
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Min, Max

from weather.filters import WeatherFilter
from weather.models import WeatherData
from weather.serializers import WeatherSerializer
from weather.swagger_params import weather_list_params
from weather.tasks import update_weather


class WeatherViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows retrieving weather data."""

    queryset = WeatherData.objects.all()
    serializer_class = WeatherSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = WeatherFilter
    search_fields = ["city", "description"]
    ordering_fields = ["timestamp", "temperature", "humidity", "wind_speed"]
    ordering = ["-timestamp"]

    @extend_schema(
        parameters=weather_list_params,
        summary="Get weather records with filtering",
        description="Retrieve weather data with optional filters such as "
                    "city, date range, temperature, humidity, and wind speed.",
    )
    def list(self, request: Request) -> Response:
        """Get the latest 25 weather records (cached for 5 minutes)."""

        cache_key = "latest_weather"
        cached_data = cache.get(cache_key)

        if cached_data is None:
            queryset = self.queryset

            serializer = self.get_serializer(queryset, many=True)
            cached_data = serializer.data
            cache.set(cache_key, cached_data, timeout=300)
            update_weather()
            return Response(serializer.data)

        return Response(cached_data)

    @action(detail=False, methods=['get'], url_path='city/(?P<city>[^/.]+)')
    def city(self, request: Request, city=None) -> Response:
        cache_key = f"weather_{city.lower()}"
        cached_data = cache.get(cache_key)

        if cached_data is None:
            weather_data = WeatherData.objects.filter(city__iexact=city).order_by("-timestamp").first()
            if not weather_data:
                return Response({"error": "No data found"}, status=404)

            serializer = self.get_serializer(weather_data)
            cache.set(cache_key, serializer.data, timeout=600)
            update_weather.delay()

            return Response(serializer.data)

        return Response(cached_data)

    @action(detail=False, methods=["get"], url_path="latest")
    def get_latest_weather(self, request: Request) -> Response:
        cache_key = "latest_weather_all"
        cached_data = cache.get(cache_key)

        if cached_data is None:
            cities = WeatherData.objects.values_list("city", flat=True).distinct()
            latest_weather = [
                WeatherData.objects.filter(city=city).order_by("-timestamp").first()
                for city in cities
            ]
            latest_weather = [w for w in latest_weather if w]

            if not latest_weather:
                return Response({"error": "No data found"}, status=404)

            serializer = self.get_serializer(latest_weather, many=True)
            cached_data = serializer.data
            cache.set(cache_key, cached_data, timeout=600)
            update_weather.delay()

        return Response(cached_data)

    @action(detail=False, methods=["get"], url_path="average/(?P<city>[^/.]+)")
    def get_average_weather(self, request: Request, city=None) -> Response:
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        cache_key = f"average_weather_{city}_{start_date}_{end_date}"
        cached_data = cache.get(cache_key)

        if cached_data is None:
            weather_data = WeatherData.objects.filter(city__iexact=city)

            if start_date and end_date:
                weather_data = weather_data.filter(timestamp__date__range=[start_date, end_date])

            if not weather_data.exists():
                return Response({"error": "No data found"}, status=404)

            avg_data = weather_data.aggregate(
                avg_temperature=Avg("temperature"),
                avg_humidity=Avg("humidity"),
                avg_wind_speed=Avg("wind_speed"),
            )

            cached_data = {"city": city, **avg_data}
            cache.set(cache_key, cached_data, timeout=600)
            update_weather.delay()

        return Response(cached_data)

    @action(detail=False, methods=["get"], url_path="stats/(?P<city>[^/.]+)")
    def get_weather_stats(self, request: Request, city=None) -> Response:
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        cache_key = f"weather_stats_{city}_{start_date}_{end_date}"
        cached_data = cache.get(cache_key)

        if cached_data is None:
            weather_data = WeatherData.objects.filter(city__iexact=city)

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

            cached_data = {"city": city, **stats_data}
            cache.set(cache_key, cached_data, timeout=1200)
            update_weather.delay()

        return Response(cached_data)


def weather_dashboard(request):
    return render(request, "weather_dashboard.html")
