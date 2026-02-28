"""Serializer for current Item pricing in Report model summaries."""

import decimal
import statistics
from functools import cache
from typing import Dict, Optional

from items.models import Item
from pricing.models import Price
from rest_framework import serializers


class ReportSummaryCurrentItemPriceSerializer(serializers.ModelSerializer):
  """Serializer for current Item pricing in Report model summaries."""

  average = serializers.SerializerMethodField()
  best = serializers.SerializerMethodField()
  per_store = serializers.SerializerMethodField()

  class Meta:
    model = Item
    fields = ('average', 'best', 'per_store')

  def get_average(self, instance: Item) -> Optional[str]:
    """Get the average price for this item across all stores in the report."""
    prices = self.get_per_store(instance).values()
    numeric_prices = [decimal.Decimal(p) for p in prices if p is not None]

    if not numeric_prices:
      return None

    average = statistics.mean(numeric_prices).quantize(
        decimal.Decimal('0.01'),
        rounding=decimal.ROUND_HALF_UP,
    )
    return str(average)

  def get_best(self, instance: Item) -> Optional[str]:
    """Get the best (lowest) price for this item across all stores."""
    prices = self.get_per_store(instance).values()
    numeric_prices = [decimal.Decimal(p) for p in prices if p is not None]

    if not numeric_prices:
      return None

    return str(min(numeric_prices))

  @cache
  def get_per_store(self, instance: Item) -> Dict[str, Optional[str]]:
    """Get the price for this item across all stores in the report."""
    report = self.context.get('report')
    week = self.context.get('week')
    year = self.context.get('year')

    if not report or not week or not year:
      return {}

    stores = report.store.all()
    prices_dict: Dict[str, Optional[str]] = {
        str(store.id): None for store in stores
    }

    for store in stores:
      price = Price.objects.filter(
          item=instance,
          store=store,
          week=week,
          year=year,
      ).first()

      if price:
        prices_dict[str(store.id)] = str(price.amount)

    return prices_dict
