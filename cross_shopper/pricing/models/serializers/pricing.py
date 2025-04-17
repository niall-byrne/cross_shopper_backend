"""Serializer for the Pricing model."""

from typing import List

from pricing.models import Price
from pricing.models.defaults import default_pricing_week, default_pricing_year
from rest_framework import serializers, validators


class PricingSerializer(serializers.ModelSerializer):
  """Serializer for creating or updating a Pricing model instance."""

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
    """Disable unique together checks to enable update operations."""
    return []
