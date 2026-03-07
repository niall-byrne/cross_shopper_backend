"""Admin for the item attribute model."""

from typing import TYPE_CHECKING

from django.contrib import admin
from items.admin.list_displays.item_attribute import item_attribute_list_display
from items.admin.list_filters.item_attribute import item_attribute_list_filter
from utilities.admin.list_displays import generate_list_display

if TYPE_CHECKING:  # no cover
  from items.models import ItemAttribute  # noqa: F401


@generate_list_display(item_attribute_list_display)
class ItemAttributeAdmin(admin.ModelAdmin["ItemAttribute"]):
  list_filter = item_attribute_list_filter
  ordering = (
      'item__name',
      'attribute__name',
  )
  search_fields = (
      'item__name',
      'attribute__name',
  )
