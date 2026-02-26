"""Reports API endpoints filters."""
from __future__ import annotations

from typing import TYPE_CHECKING

import django_filters
from django.db.models import Prefetch
from reports.models import Report
from .qs import qs_item, qs_scraper_config

if TYPE_CHECKING:
  from django.db.models import QuerySet


class ReportFilter(django_filters.FilterSet):
  """Reports API endpoint filter."""

  name = django_filters.CharFilter(field_name="name", lookup_expr="iexact")
  is_active = django_filters.BooleanFilter(
      field_name="is_active",
      method="get_query_set__is_active",
  )
  is_testing = django_filters.BooleanFilter(field_name="is_testing_only")

  class Meta:
    model = Report
    fields = ["id", "name", "is_active", "is_testing"]

  def get_query_set__is_active(
      self,
      queryset: QuerySet[Report],
      field_name: str,
      value: bool,
  ) -> QuerySet[Report]:
    """Filter each Item's ScraperConfigs in the Report query set."""
    prefetched_scraper_config = qs_scraper_config().filter(
        **{field_name: value}
    )

    prefetched_item = qs_item().prefetch_related(
        Prefetch(
            "scraper_config",
            queryset=prefetched_scraper_config,
        )
    )

    return queryset.prefetch_related(None).prefetch_related(
        Prefetch(
            "item",
            queryset=prefetched_item,
        )
    )
