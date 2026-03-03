"""Serializer for current Item pricing in summarized results of Reports."""

import decimal
import statistics
from typing import Dict, Optional

from items.models import Item
from pricing.models import Price
from rest_framework import serializers
from utilities.cache import memoize


class ReportSummaryCurrentItemPriceSerializerRO(
    serializers.ModelSerializer[Item],
):
  """Serializer for current Item pricing in summarized results of Reports."""

  average = serializers.SerializerMethodField()
  best = serializers.SerializerMethodField()
  per_store = serializers.SerializerMethodField()

  class Meta:
    model = Item
    fields = ("average", "best", "per_store")

  @memoize(timeout=60)
  def get_average(self, instance: Item) -> Optional[str]:
    """Get the average price for this item across all stores in the report."""
    prices = self.get_per_store(instance).values()
    numeric_prices = [decimal.Decimal(p) for p in prices if p is not None]

    if not numeric_prices:
      return None

    average = statistics.mean(numeric_prices).quantize(
        decimal.Decimal("0.01"),
        rounding=decimal.ROUND_HALF_UP,
    )
    return str(average)

  @memoize(timeout=60)
  def get_best(self, instance: Item) -> Optional[str]:
    """Get the best (lowest) price for this item across all stores."""
    prices = self.get_per_store(instance).values()
    numeric_prices = [decimal.Decimal(p) for p in prices if p is not None]

    if not numeric_prices:
      return None

    return str(min(numeric_prices))

  @memoize(timeout=60)
  def get_per_store(self, instance: Item) -> Dict[str, Optional[str]]:
    """Get the price for this item across all stores in the report."""
    report = self.context.get("report")
    week = self.context.get("week")
    year = self.context.get("year")

    if not report or not week or not year:
      return {}

    stores = report.store.all()
    prices_dict: Dict[str, Optional[str]] = {
        str(store.pk): None for store in stores
    }

    prices = Price.objects.filter(
        item=instance,
        store__in=stores,
        week=week,
        year=year,
    )

    for price in prices:
      prices_dict[str(price.store.pk)] = str(price.amount)

    return prices_dict

  def __repr__(self) -> str:
    """Control caching behaviour across instances."""
    return ":".join(
        map(
            repr, [
                self.context.get("week", None),
                self.context.get("year", None),
                self.context.get("report", None),
                self.__class__,
            ]
        )
    )
