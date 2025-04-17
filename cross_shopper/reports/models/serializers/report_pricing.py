"""Serializer for aggregate Pricing per Item per Report."""

import decimal
from typing import Optional

from items.models import Item
from pricing.models import Price
from rest_framework import serializers


class ReportPricingSerializer(serializers.ModelSerializer[Item]):
  """Serializer for aggregate Pricing per Item per Report."""

  name = serializers.SerializerMethodField(read_only=True)
  last_52_weeks_average = serializers.SerializerMethodField(
      read_only=True,
      allow_null=True,
  )
  last_52_weeks_high = serializers.SerializerMethodField(
      read_only=True,
      allow_null=True,
  )
  last_52_weeks_low = serializers.SerializerMethodField(
      read_only=True,
      allow_null=True,
  )

  class Meta:
    model = Item
    fields = (
        "id",
        "name",
        "last_52_weeks_average",
        "last_52_weeks_high",
        "last_52_weeks_low",
    )

  def get_last_52_weeks_average(self, instance: Item) -> Optional[str]:
    """Get the average price for this Item across all Stores in the Report."""
    average = Price.aggregate_last_52_weeks.average(
        item=instance,
        store=self.context["report"].store.all(),
    )

    return self._optional_decimal_to_string(average)

  def get_last_52_weeks_high(self, instance: Item) -> Optional[str]:
    """Get the highest price for this Item across all Stores in the Report."""
    high = Price.aggregate_last_52_weeks.high(
        item=instance,
        store=self.context["report"].store.all(),
    )

    return self._optional_decimal_to_string(high)

  def get_last_52_weeks_low(self, instance: Item) -> Optional[str]:
    """Get the lowest price for this Item across all Stores in the Report."""
    low = Price.aggregate_last_52_weeks.low(
        item=instance,
        store=self.context["report"].store.all(),
    )

    return self._optional_decimal_to_string(low)

  def _optional_decimal_to_string(
      self,
      value: Optional[decimal.Decimal],
  ) -> Optional[str]:
    if not value:
      return None

    return str(value)

  def get_name(self, instance: Item) -> str:
    """Generate a readable name for the item."""
    return str(instance)
