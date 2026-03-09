"""Report targets API endpoints."""

from reports.models import Report
from reports.models.serializers.read_only.report_target import (
    ReportTargetSerializerRO,
)
from rest_framework import viewsets
from .filters import ReportTargetFilter


class ReportTargetReadOnlyViewSet(
    viewsets.ReadOnlyModelViewSet[Report],
):
  """Report model targets read only API endpoint."""

  queryset = Report.objects.all().order_by('name')
  serializer_class = ReportTargetSerializerRO
  filterset_class = ReportTargetFilter
