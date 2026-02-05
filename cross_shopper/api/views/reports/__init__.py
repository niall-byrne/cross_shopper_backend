"""Reports API endpoints."""

from typing import TYPE_CHECKING
from django.conf import settings
from reports.models import Report
from reports.models.serializers.report import ReportSerializer
from rest_framework import viewsets
from .filters import ReportFilter

if TYPE_CHECKING:
  from django.db import models


class ReportsReadOnlyViewSet(
    viewsets.ReadOnlyModelViewSet,
):
  """Reports read only API endpoint."""

  queryset = Report.objects.all()
  serializer_class = ReportSerializer
  filterset_class = ReportFilter

  def get_queryset(self) -> "models.QuerySet[Report]":
    """Retrieve the list of reports for this view."""
    is_testing = getattr(
        settings,
        "QUERY_PARAMETER_REPORT_TESTING",
        None,
    ) in self.request.query_params
    return self.queryset.filter(is_testing_only=is_testing)
