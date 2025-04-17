"""Reports pricing per item API endpoints."""

from typing import TYPE_CHECKING, Any, Dict

from django.utils.functional import cached_property
from items.models import Item
from reports.models import Report
from reports.models.serializers.report_pricing import ReportPricingSerializer
from rest_framework import generics, viewsets

if TYPE_CHECKING:  # no cover
  from django.db.models import QuerySet


class ReportPricingReadOnlyViewSet(
    viewsets.ReadOnlyModelViewSet[Item],
):
  """Report pricing per item read only API endpoint."""

  queryset = Item.objects.all()
  serializer_class = ReportPricingSerializer

  @cached_property
  def report(self) -> Report:
    """Retrieve the Report object the view is nested under."""
    obj = generics.get_object_or_404(
        Report.objects.all(),
        pk=self.kwargs["report_pk"],
    )
    self.check_object_permissions(self.request, obj)
    return obj

  def get_queryset(self) -> "QuerySet[Item]":
    """Retrieve the list of items for this view."""
    return self.report.item.all()

  def get_serializer_context(self) -> Dict[str, Any]:
    """Generate extra context provided to the serializer class."""
    context = super().get_serializer_context()
    context.update({"report": self.report})
    return context
