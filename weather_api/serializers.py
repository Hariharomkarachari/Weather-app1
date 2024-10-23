from rest_framework import serializers
from .models import WeatherRecord, Statistic


class WeatherRecordSerializer(serializers.ModelSerializer):
    """Serializes WeatherRecord model instances, including station, date, temperatures, and precipitation."""

    class Meta:
        model = WeatherRecord
        fields = (
            "station",
            "date",
            "maximum_temperature",
            "minimum_temperature",
            "precipitation",
        )


class StatisticSerializer(serializers.ModelSerializer):
    """Serializes Statistic model instances, including station, year, average temperatures, and total precipitation."""

    class Meta:
        model = Statistic
        fields = (
            "station",
            "year",
            "average_max_temperature",
            "average_min_temperature",
            "total_precipitation",
        )
