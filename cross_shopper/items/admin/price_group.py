"""Admin for the price group model."""

from django.contrib import admin
from items.admin.list_displays.price_group import price_group_list_display
from items.admin.list_filters.price_group import price_group_list_filter
from items.admin.mixins.price_group_members import PriceGroupMembersAdminMixin
from items.models import PriceGroup
from utilities.admin.list_displays.decorator import generate_list_display


@generate_list_display(price_group_list_display)
class PriceGroupAdmin(
    admin.ModelAdmin[PriceGroup],
    PriceGroupMembersAdminMixin,
):
  fields = (
      'name',
      'quantity',
      'unit',
      'members',
  )
  list_filter = price_group_list_filter
  ordering = ('name', 'unit__name', 'quantity')
  readonly_fields = ('members',)
  search_fields = (
      'name',
      'unit__name',
  )
