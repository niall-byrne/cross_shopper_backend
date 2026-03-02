"""Serializer for the Report model."""

from items.models.serializers.item import ItemSerializer
from reports.models import Report
from rest_framework import serializers
from stores.models.serializers.read_only.store import StoreSerializerRO
from utilities.models.serializers.fields.title import TitleField


class ReportSerializer(serializers.ModelSerializer[Report]):
  """Serializer for the Report model."""

  name = TitleField(max_length=80, allow_blank=False)
  user = serializers.HiddenField(default=serializers.CurrentUserDefault())
  item = ItemSerializer(many=True)
  store = StoreSerializerRO(many=True)
  is_testing = serializers.BooleanField(default=False)

  class Meta:
    model = Report
    fields = ('id', 'name', 'item', 'store', 'user', 'is_testing')
