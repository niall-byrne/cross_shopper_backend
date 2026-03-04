"""Serializer for Item instances in Report model summaries."""

from items.models import Item
from items.models.serializers.packaging import PackagingSerializer
from reports.models.serializers.report_summary.item_price import (
    ReportSummaryItemPriceSerializer,
)
from rest_framework import serializers


class ReportSummaryItemSerializer(serializers.ModelSerializer[Item]):
  """Serializer for Item instances in Report model summaries."""

  brand = serializers.CharField(source="brand.name")
  packaging = PackagingSerializer()
  is_bulk = serializers.BooleanField(read_only=True)
  price = ReportSummaryItemPriceSerializer(source="*", read_only=True)

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
