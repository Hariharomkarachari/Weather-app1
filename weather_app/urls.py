from drf_yasg import openapi
from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from weather_api.views import StatisticViewSet, WeatherRecordViewSet

"""
URL configuration for the weather_app project, including API endpoints, admin interface, and API documentation.
"""
schema_view = get_schema_view(
    openapi.Info(
        title="Weather API",
        default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
router = DefaultRouter()
router.register(r"weather", viewset=WeatherRecordViewSet, basename="weather")
router.register(r"weather/stats", viewset=StatisticViewSet, basename="weather-stats")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
