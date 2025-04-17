"""Reports API endpoints."""

from reports.models import Report
from reports.models.serializers.report import ReportSerializer
from rest_framework import viewsets
from .filters import ReportFilter


class ReportsReadOnlyViewSet(
    viewsets.ReadOnlyModelViewSet[Report],
):
  """Reports read only API endpoint."""

  queryset = Report.objects.all()
  serializer_class = ReportSerializer
  filterset_class = ReportFilter
