from drf_yasg import openapi

trade_date_parameter = openapi.Parameter(
    "trade_date",
    openapi.IN_QUERY,
    type=openapi.TYPE_STRING,
)
