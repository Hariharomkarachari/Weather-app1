from django.db import models


class WeatherRecord(models.Model):
    """Represents daily weather data for a specific station, including temperature and precipitation."""

    station = models.CharField(verbose_name="Name of Station", max_length=100)
    date = models.DateField(verbose_name="Record Date", null=True, blank=True)
    maximum_temperature = models.IntegerField(
        verbose_name="Maximum Temperature", null=True, blank=True
    )
    minimum_temperature = models.IntegerField(
        verbose_name="Minimum Temperature", null=True, blank=True
    )
    precipitation = models.IntegerField(
        verbose_name="Precipitation", null=True, blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["date", "station"], name="unique_date_station"
            )
        ]
        indexes = [models.Index("date", "station", name="index_date_station")]
        ordering = ["-id"]

    def __str__(self):
        return f"Record for {self.station} on {self.date}"


class Statistic(models.Model):
    """Stores yearly weather statistics for a station, including average temperatures and total precipitation."""

    station = models.CharField(verbose_name="Name of Station", max_length=100)
    year = models.IntegerField(verbose_name="Record Year")
    average_max_temperature = models.FloatField(
        verbose_name="Average Maximum Temperature"
    )
    average_min_temperature = models.FloatField(
        verbose_name="Average Minimum Temperature"
    )
    total_precipitation = models.FloatField(verbose_name="Total Precipitation")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["year", "station"], name="unique_year_station"
            )
        ]
        indexes = [models.Index("year", "station", name="index_year_station")]
        ordering = ["-id"]

    def __str__(self):
        return f"Statistics for {self.station} on {self.year}"
