"""Scrapers API endpoints filters."""

import django_filters
from scrapers.models import Scraper


class ScraperFilter(django_filters.FilterSet):
  """Scraper API endpoint filter."""

  name = django_filters.CharFilter(field_name="name", lookup_expr="iexact")

  class Meta:
    model = Scraper
    fields = ["id", "name"]
