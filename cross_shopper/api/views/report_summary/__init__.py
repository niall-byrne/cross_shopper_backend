"""Report Summary API endpoints."""

from typing import TYPE_CHECKING, Any, Dict

from django.db.models import Prefetch
from reports.models import Report
from reports.models.serializers.report_summary.report import (
    ReportSummarySerializer,
)
from rest_framework import viewsets
from .filters import ReportSummaryFilter
from .qs import qs_item

if TYPE_CHECKING:  # no cover
  from typing import Any, Dict
  from django.db.models import QuerySet


class ReportSummaryViewSet(
    viewsets.ReadOnlyModelViewSet,
):
  """Report Summary read only API endpoint."""

  queryset = Report.objects.all().prefetch_related('store')
  serializer_class = ReportSummarySerializer
  filterset_class = ReportSummaryFilter

  def get_queryset(self) -> "QuerySet[Report]":
    """Retrieve the list of reports for this view."""
    return self.queryset.prefetch_related(
        Prefetch(
            'item',
            queryset=qs_item(),
        )
    )

  def get_serializer_context(self) -> "Dict[str, Any]":
    """Retrieve additional context for the serializer."""
    context = super().get_serializer_context()

    # These query params are initialized in the filter.
    week = self.request.GET.get('week')
    year = self.request.GET.get('year')

    context.update({
        'week': week,
        'year': year,
    })

    return context
