"""Serializer for the Report model in JSON format."""

from typing import Any

from django.utils import timezone
from reports.models import Report
from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict
from utilities.models.serializers.fields.context import ContextField
from .item import ReportSummaryItemSerializer
from .store import ReportSummaryStoreSerializer


class ReportSummarySerializer(serializers.ModelSerializer[Report]):
  """Serializer for Report model summaries."""

  generated_at = serializers.SerializerMethodField()
  store = ReportSummaryStoreSerializer(many=True)
  item = serializers.SerializerMethodField()
  week = ContextField(context_key="week")
  year = ContextField(context_key="year")

  class Meta:
    model = Report
    fields = (
        'id',
        'name',
        'year',
        'week',
        'generated_at',
        'store',
        'item',
    )

  def get_generated_at(self, instance: Report) -> str:
    """Get the current time as the generation time."""
    return timezone.now().strftime("%a, %d %b %Y %H:%M:%S GMT")

  def get_item(
      self,
      instance: Report,
  ) -> ReturnDict[Any, Any]:
    """Serialize the report items with the appropriate context."""
    return ReportSummaryItemSerializer(
        instance.item.all(),
        many=True,
        context={
            **self.context,
            'report': instance,
        },
    ).data
