"""Serializer for the Report model."""

from typing import Any, Dict

from django.conf import settings
from django.db.models import Prefetch
from items.models.serializers.item import ItemSerializer
from reports.models import Report
from rest_framework import serializers
from scrapers.models import ScraperConfig
from stores.models.serializers.store import StoreSerializer
from utilities.models.serializers.fields.title import TitleField
from utilities.models.serializers.mixins.boolean_query_string_mixin import (
    BooleanQueryParamMixin,
)


class ReportSerializer(serializers.ModelSerializer, BooleanQueryParamMixin):
  """Serializer for the Report model."""

  name = TitleField(max_length=80, allow_blank=False)
  user = serializers.HiddenField(default=serializers.CurrentUserDefault())
  item = serializers.SerializerMethodField()
  store = StoreSerializer(many=True)
  is_testing_only = serializers.BooleanField(default=False)

  class Meta:
    model = Report
    fields = ('id', 'name', 'item', 'store', 'user', 'is_testing_only')

  ITEM_FIELD_ORDERING = (
      'name',
      'brand__name',
      'is_organic',
      'packaging__container',
      'packaging__quantity',
  )

  def get_item(self, instance: Report) -> Dict[str, Any]:
    """Get the serialized item model representation."""
    item = instance.item.all().order_by(*self.ITEM_FIELD_ORDERING)
    query_param = self.get_boolean_query_param(
        settings.QUERY_PARAMETER_REPORT_ITEM_SCRAPER_CONFIG_IS_ACTIVE
    )

    if query_param is not None:
      item = item.prefetch_related(
          Prefetch(
              'scraper_config',
              queryset=ScraperConfig.objects.filter(is_active=query_param),
          )
      )

    return ItemSerializer(item, many=True).data
