"""Serializer to retrieve or list summarized results of Reports."""

from typing import Any

from django.utils import timezone
from reports.models import Report
from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict
from utilities.models.serializers.fields.context import SerializerContextField
from .item import ReportSummaryItemSerializerRO
from .store import ReportSummaryStoreSerializerRO


class ReportSummarySerializerRO(serializers.ModelSerializer):
  """Serializer to retrieve or list summarized results of Reports."""

  generated_at = serializers.SerializerMethodField()
  store = ReportSummaryStoreSerializerRO(many=True)
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

  def get_generated_at(self, instance: Report) -> str:
    """Get the current time as the generation time."""
    return timezone.now().strftime("%a, %d %b %Y %H:%M:%S GMT")

  def get_item(
      self,
      instance: Report,
  ) -> ReturnDict[Any, Any]:
    """Serialize the report items with the appropriate context."""
    return ReportSummaryItemSerializerRO(
        instance.item.all(),
        many=True,
        context={
            **self.context,
            'report': instance,
        },
    ).data
