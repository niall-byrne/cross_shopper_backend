"""Admin for the price group attribute model."""

from typing import TYPE_CHECKING

from django.contrib import admin
from items.admin.list_displays.price_group_attribute import (
    price_group_attribute_list_display,
)
from items.admin.list_filters.price_group_attribute import (
    price_group_attribute_list_filter,
)
from utilities.admin.list_displays import generate_list_display

if TYPE_CHECKING:
  from items.models import PriceGroupAttribute  # noqa: F401


@generate_list_display(price_group_attribute_list_display)
class PriceGroupAttributeAdmin(admin.ModelAdmin["PriceGroupAttribute"]):
  list_filter = price_group_attribute_list_filter
  ordering = (
      "price_group__name",
      "attribute__name",
  )
  search_fields = (
      "price_group__name",
      "attribute__name",
  )
