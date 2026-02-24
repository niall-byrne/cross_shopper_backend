"""Report JSON API endpoints."""

from typing import TYPE_CHECKING, Any, Dict

from django.conf import settings
from pricing.models.defaults.default_pricing_week import default_pricing_week
from pricing.models.defaults.default_pricing_year import default_pricing_year
from reports.models import Report
from reports.models.serializers.json.report import ReportJsonSerializer
from rest_framework import viewsets
from ..reports.filters import ReportFilter

if TYPE_CHECKING:  # no cover
  from django.db import models


class ReportJsonViewSet(
    viewsets.ReadOnlyModelViewSet,
):
  """Report JSON read only API endpoint."""

  queryset = Report.objects.all().prefetch_related('store', 'item')
  serializer_class = ReportJsonSerializer
  filterset_class = ReportFilter

  def get_queryset(self) -> "models.QuerySet[Report]":
    """Retrieve the list of reports for this view."""
    query_param = getattr(
        settings,
        "QUERY_PARAMETER_REPORT_TESTING",
        None,
    )
    is_testing = (
        query_param in self.request.query_params if query_param else False
    )
    return self.queryset.filter(is_testing_only=is_testing)

  def get_serializer_context(self) -> Dict[str, Any]:
    """Retrieve additional context for the serializer."""
    context = super().get_serializer_context()

    week = self.request.query_params.get('week')
    year = self.request.query_params.get('year')

    if week is None:
      week = default_pricing_week()
    if year is None:
      year = default_pricing_year()

    context.update({
        'week': int(week),
        'year': int(year),
    })

    return context
