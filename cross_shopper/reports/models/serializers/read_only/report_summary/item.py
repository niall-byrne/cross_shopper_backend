"""Serializer for Item instances in summarized results of Reports."""

from items.models import Item
from items.models.serializers.packaging import PackagingSerializer
from rest_framework import serializers
from .item_price import (
    ReportSummaryItemPriceSerializerRO,
)


class ReportSummaryItemSerializerRO(serializers.ModelSerializer[Item]):
  """Serializer for Item instances in summarized results of Reports."""

  brand = serializers.CharField(source="brand.name")
  packaging = PackagingSerializer()
  is_bulk = serializers.BooleanField(read_only=True)
  price = ReportSummaryItemPriceSerializerRO(source="*", read_only=True)

  class Meta:
    model = Item
    fields = (
        "id",
        "name",
        "brand",
        "is_bulk",
        "is_organic",
        "is_non_gmo",
        "packaging",
        "price",
    )
