"""Serializer for the Report model in JSON format."""

from typing import Any, Dict

from django.utils import timezone
from reports.models import Report
from rest_framework import serializers
from .item import ItemJsonSerializer
from .store import StoreJsonSerializer


class ReportJsonSerializer(serializers.ModelSerializer):
  """Serializer for the Report model in JSON format."""

  generated_at = serializers.SerializerMethodField()
  stores = StoreJsonSerializer(source='store', many=True)
  items = serializers.SerializerMethodField()

  class Meta:
    model = Report
    fields = ('id', 'name', 'generated_at', 'stores', 'items')

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

  def get_items(self, instance: Report) -> list[Dict[str, Any]]:
    """Get the serialized item model representation."""
    items = instance.item.all().order_by(*self.ITEM_FIELD_ORDERING)
    return ItemJsonSerializer(
        items,
        many=True,
        context={'report': instance},
    ).data
