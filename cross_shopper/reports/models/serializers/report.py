"""Serializer for the Report model."""

from typing import Any

from items.models.serializers.item import ItemSerializer
from reports.models import Report
from rest_framework import serializers
from stores.models.serializers.store import StoreSerializer
from utilities.models.serializers.fields.title import TitleField


class ReportSerializer(serializers.ModelSerializer[Report]):
  """Serializer for the Report model."""

  name = TitleField(max_length=80, allow_blank=False)
  user = serializers.HiddenField(default=serializers.CurrentUserDefault())
  item = serializers.SerializerMethodField()
  store = StoreSerializer(many=True)
  is_testing_only = serializers.BooleanField(default=False)

  class Meta:
    model = Report
    fields = ("id", "name", "item", "store", "user", "is_testing_only")

  ITEM_FIELD_ORDERING = (
      "name",
      "brand__name",
      "is_organic",
      "packaging__container",
      "packaging__quantity",
  )

  def get_item(self, instance: Report) -> dict[str, Any]:
    """Get the serialized item model representation."""
    item = instance.item.all().order_by(*self.ITEM_FIELD_ORDERING)
    return ItemSerializer(item, many=True).data
