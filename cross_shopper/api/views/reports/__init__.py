"""Reports API endpoints."""
from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import Prefetch
from reports.models import Report
from reports.models.serializers.read_only.report import ReportSerializerRO
from rest_framework import viewsets
from .filters import ReportFilter
from .qs import qs_item

if TYPE_CHECKING:
  from django.db.models import QuerySet


class ReportsReadOnlyViewSet(
    viewsets.ReadOnlyModelViewSet[Report],
):
  """Reports read only API endpoint."""

  queryset = Report.objects.all()
  serializer_class = ReportSerializerRO
  filterset_class = ReportFilter

  def get_queryset(self) -> QuerySet[Report]:
    """Retrieve the list of reports for this view."""
    return self.queryset.prefetch_related(
        Prefetch(
            "item",
            queryset=qs_item(),
        )
    )
