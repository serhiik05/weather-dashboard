from drf_spectacular.utils import OpenApiParameter, OpenApiTypes

weather_list_params = [
    OpenApiParameter(
        name="city",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        description="Filter by city (case insensitive)",
        required=False
    ),
    OpenApiParameter(
        name="start_date",
        type=OpenApiTypes.DATE,
        location=OpenApiParameter.QUERY,
        description="Start date for filtering (format: YYYY-MM-DD)",
        required=False
    ),
    OpenApiParameter(
        name="end_date",
        type=OpenApiTypes.DATE,
        location=OpenApiParameter.QUERY,
        description="End date for filtering (format: YYYY-MM-DD)",
        required=False
    ),
    OpenApiParameter(
        name="min_temperature",
        type=OpenApiTypes.FLOAT,
        location=OpenApiParameter.QUERY,
        description="Filter for minimum temperature (°C)",
        required=False
    ),
    OpenApiParameter(
        name="max_temperature",
        type=OpenApiTypes.FLOAT,
        location=OpenApiParameter.QUERY,
        description="Filter for maximum temperature (°C)",
        required=False
    ),
    OpenApiParameter(
        name="min_humidity",
        type=OpenApiTypes.FLOAT,
        location=OpenApiParameter.QUERY,
        description="Filter for minimum humidity (%)",
        required=False
    ),
    OpenApiParameter(
        name="max_humidity",
        type=OpenApiTypes.FLOAT,
        location=OpenApiParameter.QUERY,
        description="Filter for maximum humidity (%)",
        required=False
    ),
    OpenApiParameter(
        name="min_wind_speed",
        type=OpenApiTypes.FLOAT,
        location=OpenApiParameter.QUERY,
        description="Filter for minimum wind speed (km/h)",
        required=False
    ),
    OpenApiParameter(
        name="max_wind_speed",
        type=OpenApiTypes.FLOAT,
        location=OpenApiParameter.QUERY,
        description="Filter for maximum wind speed (km/h)",
        required=False
    ),
    OpenApiParameter(
        name="ordering",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        description="Sort results by field (e.g., `timestamp`, `temperature`, `humidity`, `wind_speed`)",
        required=False
    ),
    OpenApiParameter(
        name="search",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        description="Search by city name or weather description",
        required=False
    ),
]
