"""Serializer for the Report model in JSON format."""

from typing import Any

from django.utils import timezone
from reports.models import Report
from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict
from utilities.models.serializers.fields.context import SerializerContextField
from .item import ReportSummaryItemSerializer
from .store import ReportSummaryStoreSerializer


class ReportSummarySerializer(serializers.ModelSerializer):
  """Serializer for Report model summaries."""

  generated_at = serializers.SerializerMethodField()
  stores = ReportSummaryStoreSerializer(source='store', many=True)
  items = serializers.SerializerMethodField()
  week = SerializerContextField(context_field="week")
  year = SerializerContextField(context_field="year")

  class Meta:
    model = Report
    fields = (
        'id',
        'name',
        'year',
        'week',
        'generated_at',
        'stores',
        'items',
    )

  def get_generated_at(self, instance: Report) -> str:
    """Get the current time as the generation time."""
    return timezone.now().strftime("%a, %d %b %Y %H:%M:%S GMT")

  def get_items(self, instance: Report) -> ReturnDict[Any, Any]:
    """Get the serialized item model representation."""
    week = self.context.get('week')
    year = self.context.get('year')

    items = list(instance.item.all())
    items.sort(
        key=lambda i: (
            i.name,
            i.brand.name,
            i.is_organic,
            i.packaging.container.name if i.packaging.container else "",
            i.packaging.quantity,
        )
    )

    return ReportSummaryItemSerializer(
        items,
        many=True,
        context={
            'report': instance,
            'week': week,
            'year': year,
        },
    ).data
