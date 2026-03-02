"""Serializer to retrieve, list, create or update Prices."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pricing.models import Price
from pricing.models.defaults import default_pricing_week, default_pricing_year
from rest_framework import serializers

if TYPE_CHECKING:
  from rest_framework import validators


class PricingSerializerRW(serializers.ModelSerializer[Price]):
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
        "id",
        "amount",
        "item",
        "store",
        "week",
        "year",
    )

  def get_unique_together_validators(
      self,
  ) -> list[validators.UniqueTogetherValidator]:
    """Disable unique together checks to enable upsert operations."""
    return []

  def create(
      self,
      validated_data: dict[str, Any],
  ) -> Price:
    """Create or update a Price instance."""
    item = validated_data.pop("item")
    store = validated_data.pop("store")
    week = validated_data.pop("week")
    year = validated_data.pop("year")

    instance, created = Price.objects.update_or_create(
        item=item,
        store=store,
        week=week,
        year=year,
        defaults=validated_data,
    )
    self.context["created"] = created
    return instance
