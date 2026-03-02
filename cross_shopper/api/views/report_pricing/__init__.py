"""Reports pricing per item API endpoints."""

from typing import Any, Dict

from django.db import models
from django.utils.functional import cached_property
from items.models import Item
from reports.models import Report
from reports.models.serializers.read_only.report_pricing import (
    ReportPricingSerializerRO,
)
from rest_framework import generics, viewsets


class ReportPricingReadOnlyViewSet(
    viewsets.ReadOnlyModelViewSet,
):
  """Report pricing per item read only API endpoint."""

  queryset = Report.objects.all()
  serializer_class = ReportPricingSerializerRO

  @cached_property
  def requested_report_instance(self) -> Report:
    """Retrieve the object the view is displaying."""
    obj = generics.get_object_or_404(
        self.queryset,
        pk=self.kwargs['report_pk'],
    )
    self.check_object_permissions(self.request, obj)
    return obj

  def get_object(self) -> Item:
    """Retrieve the nested object the view is displaying."""
    obj = generics.get_object_or_404(
        self.requested_report_instance.item,
        pk=self.kwargs['pk'],
    )
    self.check_object_permissions(self.request, obj)
    return obj

  def get_queryset(self) -> models.QuerySet[Item]:
    """Retrieve the list of items for this view."""
    return self.requested_report_instance.item.all()

  def get_serializer_context(self) -> Dict[str, Any]:
    """Generate extra context provided to the serializer class."""
    context = super().get_serializer_context()
    context.update({"report": self.requested_report_instance})
    return context
