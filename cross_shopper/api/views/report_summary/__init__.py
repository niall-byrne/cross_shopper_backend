"""Report Summary API endpoints."""

from typing import TYPE_CHECKING, Any, Dict

from pricing.models.defaults.default_pricing_week import default_pricing_week
from pricing.models.defaults.default_pricing_year import default_pricing_year
from reports.models import Report
from reports.models.serializers.report_summary.report import (
    ReportSummarySerializer,
)
from rest_framework import viewsets

from .filters import ReportSummaryFilter

if TYPE_CHECKING:  # no cover
  from typing import Any, Dict


class ReportSummaryViewSet(
    viewsets.ReadOnlyModelViewSet,
):
  """Report Summary read only API endpoint."""

  queryset = Report.objects.all().prefetch_related(
      'store',
      'store__franchise',
      'item',
      'item__brand',
      'item__packaging',
      'item__packaging__unit',
      'item__packaging__container',
  )
  serializer_class = ReportSummarySerializer
  filterset_class = ReportSummaryFilter

  def get_serializer_context(self) -> "Dict[str, Any]":
    """Retrieve additional context for the serializer."""
    context = super().get_serializer_context()

    week = self.request.GET.get('week', default_pricing_week())
    year = self.request.GET.get('year', default_pricing_year())

    context.update({
        'week': week,
        'year': year,
    })

    return context
