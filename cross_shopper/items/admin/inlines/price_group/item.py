"""PriceGroup admin model Item inline."""

from django.contrib import admin
from items.models import Item
from items.models.price_group import PriceGroup


class PriceGroupItemInline(
    admin.TabularInline[Item, PriceGroup],
):
  extra = 0
  fields = (
      "name",
      "brand",
      "packaging",
      "is_non_gmo",
      "is_organic",
  )
  ordering = (
      "name",
      "brand__name",
      "is_organic",
      "packaging__container",
      "packaging__quantity",
  )
  show_change_link = True
  model = Item
  verbose_name = "Member"
  verbose_name_plural = "Members"
