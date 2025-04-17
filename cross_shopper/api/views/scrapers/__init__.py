"""Scrapers API endpoints."""

from rest_framework import viewsets
from scrapers.models import Scraper
from scrapers.models.serializers.scraper import ScraperSerializer
from .filters import ScraperFilter


class ScrapersReadOnlyViewSet(
    viewsets.ReadOnlyModelViewSet,
):
  """Scrapers read only API endpoint."""

  queryset = Scraper.objects.all()
  serializer_class = ScraperSerializer
  filterset_class = ScraperFilter
