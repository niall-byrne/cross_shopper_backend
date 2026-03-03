"""Serializer for Item instances in summarized results of Reports."""

from items.models import Item
from items.models.serializers.read_write.packaging import PackagingSerializerRW
from rest_framework import serializers
from .item_price import (
    ReportSummaryItemPriceSerializerRO,
)


class ReportSummaryItemSerializerRO(serializers.ModelSerializer):
  """Serializer for Item instances in summarized results of Reports."""

  brand = serializers.CharField(source='brand.name')
  packaging = PackagingSerializerRW()
  is_bulk = serializers.BooleanField(read_only=True)
  price = ReportSummaryItemPriceSerializerRO(source='*', read_only=True)

  class Meta:
    model = Item
    fields = (
        'id',
        'name',
        'brand',
        'is_bulk',
        'is_organic',
        'is_non_gmo',
        'packaging',
        'price',
    )
