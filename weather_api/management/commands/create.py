from django.core.management.base import BaseCommand

import os
import csv
import logging
from datetime import datetime
from django.db.models import Q
from django.db.models import Avg, Sum
from weather_api.models import WeatherRecord, Statistic
from django.db.models.functions import ExtractYear


class Command(BaseCommand):
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename="log.log",
    )
    logger = logging.getLogger(__name__)
    help = "Create database tables and ingest data"

    def read_data(self):
        """Reads weather data from txt files and returns it as a list of WeatherRecord objects."""
        self.logger.info("Reading txt files to dump data")
        folder = "data/wx_data"
        weather_data = []
        try:
            for file in os.scandir(folder):
                if file.name.endswith(".txt"):
                    self.logger.info(f"Processing file: {file.name}")
                    station = file.name.split(".")[0]
                    with open(file.path, mode="r") as input_file:
                        reader = csv.reader(input_file, delimiter="\t")
                        data = list(reader)
                        existing_records = set(
                            WeatherRecord.objects.filter(station=station).values_list(
                                "date", flat=True
                            )
                        )
                        for row in data:
                            try:
                                date = datetime.strptime(row[0], "%Y%m%d").date()
                                maximum_temperature = (
                                    int(row[1]) if row[1] != "-9999" else None
                                )
                                minimum_temperature = (
                                    int(row[2]) if row[2] != "-9999" else None
                                )
                                precipitation = (
                                    int(row[3]) if row[3] != "-9999" else None
                                )
                                if date not in existing_records:
                                    weather_data.append(
                                        WeatherRecord(
                                            station=station,
                                            date=date,
                                            maximum_temperature=maximum_temperature,
                                            minimum_temperature=minimum_temperature,
                                            precipitation=precipitation,
                                        )
                                    )
                                else:
                                    self.logger.info(f"Record already exists: {row}")
                            except (ValueError, IndexError) as e:
                                self.logger.error(f"Error processing row: {row} - {e}")
            if not weather_data:
                self.logger.info(f"No new records to insert")
        except FileNotFoundError:
            self.logger.error(f"Folder not found: {folder}")
        except Exception as e:
            self.logger.error(f"An error occured: {e}")
        finally:
            return weather_data

    def dump_wx_data(self):
        """Reads weather data using read_data() and bulk inserts it into the WeatherRecord model."""
        try:
            start = datetime.now()
            weather_data = self.read_data()
            WeatherRecord.objects.bulk_create(weather_data)
        except Exception as e:
            self.logger.error(f"Error in inserting weather row: {e}")
        finally:
            end = datetime.now()
            self.logger.info(
                f"Weather Data inserted in : {(end-start).total_seconds()} seconds. Rows count: {len(weather_data)}"
            )

    def dump_statistics(self):
        """Calculates and bulk inserts yearly statistics for each weather station into the Statistic model."""
        try:
            start = datetime.now()
            statistics = (
                WeatherRecord.objects.exclude(
                    Q(maximum_temperature=None)
                    | Q(minimum_temperature=None)
                    | Q(precipitation=None)
                )
                .annotate(year=ExtractYear("date"))
                .values("station", "year")
                .annotate(
                    average_max_temperature=Avg("maximum_temperature"),
                    average_min_temperature=Avg("minimum_temperature"),
                    total_precipitation=Sum("precipitation"),
                )
            )
            stats_to_create = []
            for stat in statistics:
                if not Statistic.objects.filter(
                    station=stat["station"], year=stat["year"]
                ).exists():
                    stats_to_create.append(
                        Statistic(
                            station=stat["station"],
                            year=stat["year"],
                            average_max_temperature=stat["average_max_temperature"],
                            average_min_temperature=stat["average_min_temperature"],
                            total_precipitation=stat["total_precipitation"],
                        )
                    )
            if stats_to_create:
                Statistic.objects.bulk_create(stats_to_create)
            else:
                self.logger.info(f"No new statistics to insert")
        except Exception as e:
            self.logger.error(f"Error in inserting statistics row: {e}")
        finally:
            end = datetime.now()
            self.logger.info(
                f"Statistics Data inserted in : {(end-start).total_seconds()} seconds. Rows count: {len(stats_to_create)}"
            )

    def handle(self, *args, **kwargs):
        """Executes the weather data and statistics dump process."""
        self.dump_wx_data()
        self.dump_statistics()
