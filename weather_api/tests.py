from faker import Faker
from datetime import date
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from weather_api.models import Statistic, WeatherRecord
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from weather_api.serializers import StatisticSerializer, WeatherRecordSerializer


class WeatherRecordTest(APITestCase):
    """Tests for WeatherRecord API endpoints."""

    def setUp(self) -> None:
        """Set up test data and client for WeatherRecord tests."""
        self.client = APIClient()
        self.route = reverse(viewname="weather-list")
        self.faker = Faker()

        for _ in range(10):
            WeatherRecord.objects.create(
                station=self.faker.city(),
                date=self.faker.date_this_century(),
                maximum_temperature=self.faker.random_int(min=-30, max=40),
                minimum_temperature=self.faker.random_int(min=-50, max=20),
                precipitation=self.faker.random_int(min=0, max=100),
            )

    def test_list_weather_record(self):
        """Test listing all weather records."""
        response = self.client.get(path=self.route, content_type="applicatin/json")
        queryset = WeatherRecord.objects.all()
        serializer = WeatherRecordSerializer(queryset, many=True)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_list_weather_record_with_station_filter(self):
        """Test listing weather records filtered by station."""
        station = WeatherRecord.objects.first().station
        response = self.client.get(
            path=f"{self.route}?station={station}", content_type="application/json"
        )
        records = WeatherRecord.objects.filter(station=station)
        serializer = WeatherRecordSerializer(records, many=True)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(response.data["count"], len(serializer.data))

    def test_list_weather_record_with_date_filter(self):
        """Test listing weather records filtered by date."""
        date = WeatherRecord.objects.first().date
        response = self.client.get(
            path=f"{self.route}?date={date}", content_type="application/json"
        )
        records = WeatherRecord.objects.filter(date=date)
        serializer = WeatherRecordSerializer(records, many=True)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["count"], len(serializer.data))
        self.assertEqual(response.data["results"], serializer.data)

    def test_list_weather_record_with_station_and_date_filter(self):
        """Test listing weather records filtered by both station and date."""
        station = WeatherRecord.objects.first().station
        date = WeatherRecord.objects.first().date
        response = self.client.get(
            path=f"{self.route}?station={station}&date={date}",
            content_type="application/json",
        )
        records = WeatherRecord.objects.filter(date=date)
        serializer = WeatherRecordSerializer(records, many=True)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["count"], len(serializer.data))
        self.assertEqual(response.data["results"], serializer.data)

    def test_list_weather_record_with_invalid_filter(self):
        """Test listing weather records with invalid filter parameters."""
        station = "Wrong-Station"
        date = "2025-01-01"
        response = self.client.get(
            path=f"{self.route}?station={station}&date={date}",
            content_type="application/json",
        )
        records = WeatherRecord.objects.filter(station=station, date=date)
        serializer = WeatherRecordSerializer(records, many=True)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["count"], len(serializer.data))
        self.assertEqual(response.data["results"], serializer.data)

    def test_list_weather_record_exception(self):
        """Test handling of exceptions in weather record listing."""
        date = "2024-01-01"
        response = self.client.get(
            path=f'{self.route}?date="{date}"', content_type="application/json"
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_weather_record_str(self):
        """Test the string representation of a WeatherRecord instance."""
        self.weather_record = WeatherRecord.objects.create(
            station="Test Station",
            date=date(2024, 1, 1),
            maximum_temperature=35,
            minimum_temperature=22,
            precipitation=5,
        )
        self.assertEqual(
            str(self.weather_record), "Record for Test Station on 2024-01-01"
        )


class StatisticsTest(APITestCase):
    """Tests for Statistics API endpoints."""

    def setUp(self):
        """Set up test data and client for Statistics tests."""
        self.client = APIClient()
        self.route = reverse("weather-stats-list")
        self.faker = Faker()

        for _ in range(10):
            Statistic.objects.create(
                station=self.faker.city(),
                year=self.faker.year(),
                average_max_temperature=self.faker.random_int(min=-10, max=30),
                average_min_temperature=self.faker.random_int(min=-20, max=10),
                total_precipitation=self.faker.random_number(digits=2),
            )

    def test_list_statistics(self):
        """Test listing all statistics."""
        response = self.client.get(path=self.route, content_type="application/json")
        statistics = Statistic.objects.all()
        serializer = StatisticSerializer(statistics, many=True)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_list_statistics_with_station_filter(self):
        """Test listing statistics filtered by station."""
        station = Statistic.objects.first().station
        response = self.client.get(
            path=f"{self.route}?station={station}", content_type="application/json"
        )
        statistics = Statistic.objects.filter(station=station)
        serializer = StatisticSerializer(statistics, many=True)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(response.data["count"], len(serializer.data))

    def test_list_statistics_with_year_filter(self):
        """Test listing statistics filtered by year."""
        year = Statistic.objects.first().year
        response = self.client.get(
            path=f"{self.route}?year={year}", content_type="application/json"
        )
        statistics = Statistic.objects.filter(year=year)
        serializer = StatisticSerializer(statistics, many=True)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(response.data["count"], len(serializer.data))

    def test_list_statistics_with_station_and_year_filter(self):
        """Test listing statistics filtered by both station and year."""
        station = Statistic.objects.first().station
        year = Statistic.objects.first().year
        response = self.client.get(
            path=f"{self.route}?station={station}&year={year}",
            content_type="application/json",
        )
        statistics = Statistic.objects.filter(station=station, year=year)
        serializer = StatisticSerializer(statistics, many=True)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["count"], len(serializer.data))
        self.assertEqual(response.data["results"], serializer.data)

    def test_list_statistics_with_invalid_filter(self):
        """Test listing statistics with invalid filter parameters."""
        station = "Wrong-Station"
        year = 2024
        response = self.client.get(
            path=f"{self.route}?station={station}&year={year}",
            content_type="application/json",
        )
        statistics = Statistic.objects.filter(station=station, year=year)
        serializer = StatisticSerializer(statistics, many=True)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(response.data["count"], len(serializer.data))

    def test_list_statistics_exception(self):
        """Test handling of exceptions in statistics listing."""
        year = "2024"
        response = self.client.get(
            path=f'{self.route}?year="{year}"', content_type="application/json"
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_statistic_str(self):
        """Test the string representation of a Statistic instance."""
        self.statistic = Statistic.objects.create(
            station="Test Station",
            year=2024,
            average_max_temperature=30.5,
            average_min_temperature=20.5,
            total_precipitation=150.0,
        )
        self.assertEqual(str(self.statistic), "Statistics for Test Station on 2024")
