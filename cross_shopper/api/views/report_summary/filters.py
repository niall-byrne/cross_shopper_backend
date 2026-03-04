"""Report summary API endpoint filters."""
from __future__ import annotations

from typing import Any

from django_filters import rest_framework as filters
from pricing.models import Price
from pricing.models.defaults.default_pricing_week import default_pricing_week
from pricing.models.defaults.default_pricing_year import default_pricing_year
from reports.models import Report
from utilities.views.filters.passthrough import PassThroughFilter
from utilities.views.filtersets.default import DefaultFilterSet


class ReportSummaryFilter(DefaultFilterSet):
  """Report summary API endpoint filter."""

  is_testing = filters.BooleanFilter(field_name="is_testing")
  name = filters.CharFilter(
      field_name="name",
      lookup_expr="iexact",
  )
  week = PassThroughFilter(field_name="week", for_model=Price)
  year = PassThroughFilter(field_name="year", for_model=Price)

  class Meta:
    model = Report
    fields = [
        "id",
        "is_testing",
        "name",
        "week",
        "year",
    ]

  def default_week(self) -> Any:
    """Return the default week value."""
    return default_pricing_week()

  def default_year(self) -> Any:
    """Return the default year value."""
    return default_pricing_year()
