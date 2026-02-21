"""Error API endpoint filters."""

from django_filters import rest_framework as filters
from errors.models import Error
from items.models import Item
from stores.models import Store


class ErrorFilter(filters.FilterSet):
  """Pricing API endpoint filter."""

  itemId = filters.ModelMultipleChoiceFilter(
      field_name="item",
      queryset=Item.objects.all(),
  )
  is_reoccurring = filters.BooleanFilter()
  storeId = filters.ModelMultipleChoiceFilter(
      field_name="store",
      queryset=Store.objects.all(),
  )
  type = filters.CharFilter(field_name="type__name", lookup_expr="iexact")

  class Meta:
    model = Error
    fields = ["id", "type"]
