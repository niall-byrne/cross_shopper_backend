"""Serializer for the Item model in JSON format."""

import decimal
from functools import cache
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

  @cache
  def get_prices(self, instance: Item) -> Dict[str, Optional[str]]:
    """Get the price for this item across all stores in the report."""
    report = self.context.get('report')
    if not report:
      return {}

    stores = report.store.all()
    prices_dict = {str(store.id): None for store in stores}

    # Check if prices were prefetched
    current_prices = getattr(instance, 'current_prices', None)
    if current_prices is not None:
      for price in current_prices:
        prices_dict[str(price.store_id)] = str(price.amount)
      return prices_dict

    # Fallback to manual query
    week = self.context.get('week')
    year = self.context.get('year')

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

  def get_best_price(self, instance: Item) -> Optional[str]:
    """Get the best (lowest) price for this item across all stores."""
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
