"""Serializer to retrieve, list, create or update Prices."""

from typing import Any, Dict, List

from pricing.models import Price
from pricing.models.defaults import default_pricing_week, default_pricing_year
from rest_framework import serializers, validators


class PricingSerializer(serializers.ModelSerializer[Price]):
  """Serializer to retrieve, list, create or update Prices."""

  week = serializers.IntegerField(
      default=default_pricing_week.default_pricing_week,
      min_value=0,
      max_value=52,
      required=False,
  )
  year = serializers.IntegerField(
      default=default_pricing_year.default_pricing_year(),
      min_value=2024,
      max_value=2100,
      required=False,
  )

  class Meta:
    model = Price
    fields = (
        'id',
        'amount',
        'item',
        'store',
        'week',
        'year',
    )

  def get_unique_together_validators(
      self,
  ) -> List[validators.UniqueTogetherValidator]:
    """Disable unique together checks to enable upsert operations."""
    return []

  def create(
      self,
      validated_data: Dict[str, Any],
  ) -> Price:
    """Create or update a Price instance."""
    item = validated_data.pop('item')
    store = validated_data.pop('store')
    week = validated_data.pop('week')
    year = validated_data.pop('year')

    instance, created = Price.objects.update_or_create(
        item=item,
        store=store,
        week=week,
        year=year,
        defaults=validated_data,
    )
    self.context['created'] = created
    return instance
