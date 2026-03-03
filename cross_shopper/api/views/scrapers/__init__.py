"""Scrapers API endpoints."""

from rest_framework import viewsets
from scrapers.models import Scraper
from scrapers.models.serializers.read_only.scraper import ScraperSerializerRO
from .filters import ScraperFilter


class ScrapersReadOnlyViewSet(
    viewsets.ReadOnlyModelViewSet[Scraper],
):
  """Scrapers read only API endpoint."""

  queryset = Scraper.objects.all()
  serializer_class = ScraperSerializerRO
  filterset_class = ScraperFilter
