"""Serializer for Price instances in Report model summaries."""

from typing import Optional

from items.models import Item
from pricing.models import Price
from rest_framework import serializers


class ReportSummaryHistoricalItemPriceSerializer(serializers.ModelSerializer):
  """Serializer for Item price history in Report model summaries."""

  average = serializers.SerializerMethodField()
  high = serializers.SerializerMethodField()
  low = serializers.SerializerMethodField()

  class Meta:
    model = Item
    fields = ('average', 'high', 'low')

  def get_average(self, instance: Item) -> Optional[str]:
    """Get the average price for this item at the report stores."""
    report = self.context.get('report')

    if report:
      average = Price.aggregate_last_52_weeks.average(
          item=instance,
          store=report.store.all(),
      )

      if average:
        return str(average)
    return None

  def get_high(self, instance: Item) -> Optional[str]:
    """Get the average price for this item at the report stores."""
    report = self.context.get('report')

    if report:
      high = Price.aggregate_last_52_weeks.high(
          item=instance,
          store=report.store.all(),
      )

      if high:
        return str(high)
    return None

  def get_low(self, instance: Item) -> Optional[str]:
    """Get the average price for this item at the report stores."""
    report = self.context.get('report')

    if report:
      low = Price.aggregate_last_52_weeks.low(
          item=instance,
          store=report.store.all(),
      )

      if low:
        return str(low)
    return None


class ReportSummaryPriceSerializer(serializers.ModelSerializer):
  """Serializer for Price instances in Report model summaries."""

  class Meta:
    model = Price
    fields = ('id', 'name')
