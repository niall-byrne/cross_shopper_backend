"""Reports API endpoints."""

from typing import TYPE_CHECKING

from django.db.models import Prefetch
from reports.models import Report
from reports.models.serializers.report import ReportSerializer
from rest_framework import viewsets
from .filters import ReportFilter
from .qs import qs_item

if TYPE_CHECKING:  # no cover
  from django.db.models import QuerySet


class ReportsReadOnlyViewSet(
    viewsets.ReadOnlyModelViewSet,
):
  """Reports read only API endpoint."""

  queryset = Report.objects.all()
  serializer_class = ReportSerializer
  filterset_class = ReportFilter

  def get_queryset(self) -> "QuerySet[Report]":
    """Retrieve the list of reports for this view."""
    return self.queryset.prefetch_related(
        Prefetch(
            'item',
            queryset=qs_item(),
        )
    )
