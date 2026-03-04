"""Serializer for Item pricing in Report model summaries."""

from items.models import Item
from reports.models.serializers.report_summary.item_price_current import (
    ReportSummaryCurrentItemPriceSerializer,
)
from reports.models.serializers.report_summary.item_price_historical import (
    ReportSummaryHistoricalItemPriceSerializer,
)
from rest_framework import serializers


class ReportSummaryItemPriceSerializer(serializers.ModelSerializer[Item]):
  """Serializer for Item pricing in Report model summaries."""

  last_52_weeks = ReportSummaryHistoricalItemPriceSerializer(
      source='*',
      read_only=True,
  )
  selected_week = ReportSummaryCurrentItemPriceSerializer(
      source='*',
      read_only=True,
  )

  class Meta:
    model = Item
    fields = ('last_52_weeks', 'selected_week')
