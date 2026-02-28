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
  week = filters.NumberFilter(method="get_week")
  year = filters.NumberFilter(method="get_year")

  def __init__(self, *args: "Any", **kwargs: "Any") -> None:
    super().__init__(*args, **kwargs)
    self.data = self.data.copy()
    if not self.data.get('week'):
      self.data['week'] = default_pricing_week()
    if not self.data.get('year'):
      self.data['year'] = default_pricing_year()

  class Meta:
    model = Report
    fields = [
        'is_testing',
        'name',
    ]

  def get_week(
      self,
      queryset: "QuerySet[Report]",
      field_name: "str",
      value: "bool",
  ) -> "QuerySet[Report]":
    """Update the week query parameter."""
    self.request.GET = self.request.GET.copy()
    self.request.GET.update({'week': value})
    return queryset

  def get_year(
      self,
      queryset: "QuerySet[Report]",
      field_name: "str",
      value: "bool",
  ) -> "QuerySet[Report]":
    """Update the year query parameter."""
    self.request.GET = self.request.GET.copy()
    self.request.GET.update({'year': value})
    return queryset
