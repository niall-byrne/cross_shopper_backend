"""Report JSON API endpoints."""

from typing import TYPE_CHECKING

from django.conf import settings
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
