from drf_yasg import openapi
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.status import HTTP_400_BAD_REQUEST
from weather_api.models import WeatherRecord, Statistic
from weather_api.serializers import WeatherRecordSerializer, StatisticSerializer


class WeatherRecordViewSet(ListModelMixin, GenericViewSet):
    """ViewSet for listing WeatherRecord instances with optional date and station filters."""

    queryset = WeatherRecord.objects.all()
    serializer_class = WeatherRecordSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "date",
                openapi.IN_QUERY,
                description="Date of the record.",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
            ),
            openapi.Parameter(
                "station",
                openapi.IN_QUERY,
                description="Name of the station.",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def list(self, request):
        """List WeatherRecord instances, optionally filtered by date and/or station."""
        try:
            date = request.GET.get("date", None)
            station = request.GET.get("station", None)

            if date:
                self.queryset = self.queryset.filter(date=date)
            if station:
                self.queryset = self.queryset.filter(station=station)

            page = self.paginate_queryset(self.queryset)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        except Exception as error:
            return Response({"error": str(error)}, status=HTTP_400_BAD_REQUEST)


class StatisticViewSet(ListModelMixin, GenericViewSet):
    """ViewSet for listing Statistic instances with optional year and station filters."""

    queryset = Statistic.objects.all()
    serializer_class = StatisticSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "year",
                openapi.IN_QUERY,
                description="Year of the stats.",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "station",
                openapi.IN_QUERY,
                description="Name of the station.",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def list(self, request):
        """List Statistic instances, optionally filtered by year and/or station."""
        try:
            year = request.GET.get("year", None)
            station = request.GET.get("station", None)

            if year:
                self.queryset = self.queryset.filter(year=year)
            if station:
                self.queryset = self.queryset.filter(station=station)

            page = self.paginate_queryset(self.queryset)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        except Exception as error:
            return Response({"error": str(error)}, status=HTTP_400_BAD_REQUEST)
