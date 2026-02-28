"""Report summary API endpoint filters."""

from typing import TYPE_CHECKING

from django_filters import rest_framework as filters
from pricing.models.defaults.default_pricing_week import default_pricing_week
from pricing.models.defaults.default_pricing_year import default_pricing_year
from reports.models import Report

if TYPE_CHECKING:  # no cover
  from typing import Any

  from django.db.models import QuerySet


class ReportSummaryFilter(filters.FilterSet):
  """Report summary API endpoint filter."""

  is_testing = filters.BooleanFilter(field_name="is_testing")
  name = filters.CharFilter(field_name="name", lookup_expr='iexact')
  week = filters.NumberFilter(method="filter_week")
  year = filters.NumberFilter(method="filter_year")

  class Meta:
    model = Report
    fields = [
        'is_testing',
        'name',
    ]

  def filter_week(
      self,
      queryset: "QuerySet[Report]",
      field_name: "str",
      value: "Any",
  ) -> "QuerySet[Report]":
    """Update the week query parameter."""
    return queryset

  def filter_year(
      self,
      queryset: "QuerySet[Report]",
      field_name: "str",
      value: "Any",
  ) -> "QuerySet[Report]":
    """Update the year query parameter."""
    return queryset
