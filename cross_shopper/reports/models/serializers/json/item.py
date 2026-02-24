"""Serializer for the Item model in JSON format."""

import decimal
from typing import Dict, Optional

from items.models import Item
from items.models.serializers.packaging import PackagingSerializer
from pricing.models import Price
from rest_framework import serializers


class ItemJsonSerializer(serializers.ModelSerializer):
  """Serializer for the Item model in JSON format."""

  best_price = serializers.SerializerMethodField()
  brand = serializers.CharField(source='brand.name')
  packaging = PackagingSerializer()
  is_bulk = serializers.BooleanField(read_only=True)
  average_price = serializers.SerializerMethodField()
  prices = serializers.SerializerMethodField()

  _cached_prices: Optional[Dict[str, Optional[str]]] = None

  class Meta:
    model = Item
    fields = (
        'id',
        'name',
        'best_price',
        'brand',
        'packaging',
        'is_bulk',
        'is_organic',
        'is_non_gmo',
        'average_price',
        'prices',
    )

  def get_prices(self, instance: Item) -> Dict[str, Optional[str]]:
    """Get the latest price for this item across all stores in the report."""
    if self._cached_prices is not None:
      return self._cached_prices

    report = self.context.get('report')
    if not report:
      return {}

    stores = report.store.all()
    prices_dict = {}

    for store in stores:
      latest_price = Price.objects.filter(
          item=instance,
          store=store,
      ).order_by('-year', '-week').first()

      if latest_price:
        prices_dict[str(store.id)] = str(latest_price.amount)
      else:
        prices_dict[str(store.id)] = None

    self._cached_prices = prices_dict
    return prices_dict

  def get_best_price(self, instance: Item) -> Optional[str]:
    """Get the best (lowest) current price for this item across all stores."""
    prices = self.get_prices(instance).values()
    numeric_prices = [
        decimal.Decimal(p) for p in prices if p is not None
    ]

    if not numeric_prices:
      return None

    return str(min(numeric_prices))

  def get_average_price(self, instance: Item) -> Optional[str]:
    """Get the average price for this item across all stores in the report."""
    report = self.context.get('report')
    if not report:
      return None

    average = Price.aggregate_last_52_weeks.average(
        item=instance,
        store=report.store.all(),
    )

    if average is None:
      return None

    return str(average)
