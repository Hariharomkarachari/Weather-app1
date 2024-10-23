from .models import *
from django.contrib import admin


@admin.register(WeatherRecord)
class WeatherRecordAdmin(admin.ModelAdmin):
    """Admin configuration for WeatherRecord model."""

    search_fields = ("station",)
    list_display = (
        "id",
        "date",
        "maximum_temperature",
        "minimum_temperature",
        "precipitation",
        "station",
    )


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    """Admin configuration for Statistic model."""

    search_fields = ("station",)
    list_display = (
        "id",
        "average_max_temperature",
        "average_min_temperature",
        "total_precipitation",
        "year",
        "station",
    )
