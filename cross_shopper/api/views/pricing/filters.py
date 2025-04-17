"""Pricing API endpoint filters."""

from typing import Any

from django_filters import rest_framework as filters
from items.models import Item
from pricing.models import Price
from pricing.models.defaults.default_pricing_week import default_pricing_week
from pricing.models.defaults.default_pricing_year import default_pricing_year
from stores.models import Store


class PricingFilter(filters.FilterSet):
  """Pricing API endpoint filter."""

  itemId = filters.ModelMultipleChoiceFilter(
      field_name='item',
      queryset=Item.objects.all(),
  )
  storeId = filters.ModelMultipleChoiceFilter(
      field_name='store',
      queryset=Store.objects.all(),
  )

  def __init__(self, *args: Any, **kwargs: Any) -> None:
    super().__init__(*args, **kwargs)
    data = self.data.copy()  # Mutable QueryDict
    if not self.data.get('week'):
      data['week'] = default_pricing_week()
    if not self.data.get('year'):
      data['year'] = default_pricing_year()
    self.data = data

  class Meta:
    model = Price
    fields = ['week', 'year']
