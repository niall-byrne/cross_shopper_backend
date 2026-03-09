"""Report targets API endpoints filters."""

import django_filters
from reports.models import Report


class ReportTargetFilter(django_filters.FilterSet):
  """Reports API endpoint filter."""

  name = django_filters.CharFilter(field_name="name", lookup_expr="iexact")
  is_testing = django_filters.BooleanFilter(field_name="is_testing")

  class Meta:
    model = Report
    fields = ["id", "name", "is_testing"]
