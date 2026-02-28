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
  store = ReportSummaryStoreSerializer(many=True)
  item = serializers.SerializerMethodField()
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
        'store',
        'item',
    )

  ITEM_FIELD_ORDERING = (
      'name',
      'brand__name',
      'is_organic',
      'packaging__container',
      'packaging__quantity',
  )

  def get_generated_at(self, instance: Report) -> str:
    """Get the current time as the generation time."""
    return timezone.now().strftime("%a, %d %b %Y %H:%M:%S GMT")

  def get_item(self, instance: Report) -> ReturnDict[Any, Any]:
    """Get the serialized item model representation."""
    week = self.context.get('week')
    year = self.context.get('year')

    items = instance.item.all().order_by(*self.ITEM_FIELD_ORDERING)

    return ReportSummaryItemSerializer(
        items,
        many=True,
        context={
            'report': instance,
            'week': week,
            'year': year,
        },
    ).data
