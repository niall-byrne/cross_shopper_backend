"""Reports API endpoints filters."""

import django_filters
from reports.models import Report


class ReportFilter(django_filters.FilterSet):
  """Reports API endpoint filter."""

  name = django_filters.CharFilter(field_name="name", lookup_expr="iexact")

  class Meta:
    model = Report
    fields = ["id", "name"]
