"""Admin for the price group model."""

from django.contrib import admin
from items.admin.inlines.price_group import price_group_inlines
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
  fieldsets = (
      (
          "IDENTIFICATION",
          {
              "fields": ("name",)
          },
      ),
      (
          "COMPARISON BASE",
          {
              "fields": ("quantity", "unit"),
          },
      ),
      (
          "COMPARISON CERTIFICATIONS",
          {
              "fields": (
                  "is_non_gmo",
                  "is_organic",
              ),
          },
      ),
  )
  inlines = price_group_inlines
  list_filter = price_group_list_filter
  ordering = (
      "name",
      "is_non_gmo",
      "is_organic",
      "unit__name",
      "quantity",
  )
  search_fields = (
      "name",
      "unit__name",
  )
