"""Pricing API endpoint filters."""
from __future__ import annotations

from typing import Any

from django_filters import rest_framework as filters
from items.models import Item
from pricing.models import Price
from pricing.models.defaults.default_pricing_week import default_pricing_week
from pricing.models.defaults.default_pricing_year import default_pricing_year
from stores.models import Store
from utilities.views.filtersets.default import DefaultFilterSet


class PricingFilter(DefaultFilterSet):
  """Pricing API endpoint filter."""

  itemId = filters.ModelMultipleChoiceFilter(
      field_name="item",
      queryset=Item.objects.all(),
  )
  storeId = filters.ModelMultipleChoiceFilter(
      field_name="store",
      queryset=Store.objects.all(),
  )

  class Meta:
    model = Price
    fields = ["itemId", "storeId", "week", "year"]

  def default_week(self) -> Any:
    """Return the default week value."""
    return default_pricing_week()

  def default_year(self) -> Any:
    """Return the default year value."""
    return default_pricing_year()
