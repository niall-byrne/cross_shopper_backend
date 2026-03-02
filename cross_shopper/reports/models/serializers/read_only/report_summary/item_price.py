"""Serializer for Item pricing in summarized results of Reports."""

from items.models import Item
from rest_framework import serializers
from .item_price_current import (
    ReportSummaryCurrentItemPriceSerializerRO,
)
from .item_price_historical import (
    ReportSummaryHistoricalItemPriceSerializerRO,
)


class ReportSummaryItemPriceSerializerRO(serializers.ModelSerializer):
  """Serializer for Item pricing in summarized results of Reports."""

  last_52_weeks = ReportSummaryHistoricalItemPriceSerializerRO(
      source='*',
      read_only=True,
  )
  selected_week = ReportSummaryCurrentItemPriceSerializerRO(
      source='*',
      read_only=True,
  )

  class Meta:
    model = Item
    fields = ('last_52_weeks', 'selected_week')
