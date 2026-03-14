"""Test the admin for the PriceGroup model."""

from django.contrib import admin
from items.admin.inlines.price_group import price_group_inlines
from items.admin.list_displays.price_group import (
    price_group_list_display,
)
from items.admin.list_filters.price_group import (
    price_group_list_filter,
)
from items.admin.mixins.price_group_members import PriceGroupMembersAdminMixin
from items.admin.price_group import PriceGroupAdmin


class TestPriceGroupAdmin:

  def test_instantiate__inheritance(
      self,
      price_group_admin: PriceGroupAdmin,
  ) -> None:
    assert isinstance(price_group_admin, admin.ModelAdmin)
    assert isinstance(price_group_admin, PriceGroupMembersAdminMixin)

  def test_instantiate__has_correct_fieldsets(
      self,
      price_group_admin: PriceGroupAdmin,
  ) -> None:
    assert price_group_admin.fieldsets == (
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

  def test_instantiate__has_correct_inlines(
      self,
      price_group_admin: PriceGroupAdmin,
  ) -> None:
    assert price_group_admin.inlines == price_group_inlines

  def test_instantiate__has_correct_list_display(
      self,
      price_group_admin: PriceGroupAdmin,
  ) -> None:
    assert price_group_admin.list_display == tuple(
        map(str, price_group_list_display)
    )

  def test_instantiate__has_correct_list_filter(
      self,
      price_group_admin: PriceGroupAdmin,
  ) -> None:
    assert price_group_admin.list_filter == price_group_list_filter

  def test_instantiate__has_correct_ordering(
      self,
      price_group_admin: PriceGroupAdmin,
  ) -> None:
    assert price_group_admin.ordering == (
        "name",
        "is_non_gmo",
        "is_organic",
        "unit__name",
        "quantity",
    )

  def test_instantiate__has_correct_search_fields(
      self,
      price_group_admin: PriceGroupAdmin,
  ) -> None:
    assert price_group_admin.search_fields == (
        "name",
        "unit__name",
    )
