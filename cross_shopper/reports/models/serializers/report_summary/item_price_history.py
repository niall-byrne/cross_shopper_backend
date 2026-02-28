"""Serializer for historical Item pricing in Report model summaries."""

from typing import Optional

from items.models import Item
from pricing.models import Price
from rest_framework import serializers


class ReportSummaryItemPriceHistorySerializer(serializers.ModelSerializer):
  """Serializer for historical Item pricing in Report model summaries."""

  average = serializers.SerializerMethodField()
  high = serializers.SerializerMethodField()
  low = serializers.SerializerMethodField()

  class Meta:
    model = Item
    fields = ('average', 'high', 'low')

  def get_average(self, instance: Item) -> Optional[str]:
    """Get the average price for this item at the report stores."""
    report = self.context.get('report')
    if not report:
      return None

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
    if not report:
      return None

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
    if not report:
      return None

    low = Price.aggregate_last_52_weeks.low(
        item=instance,
        store=report.store.all(),
    )

    if low:
      return str(low)
    return None
