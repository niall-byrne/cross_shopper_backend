"""Test the admin for the PriceGroupAttribute model."""
from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import admin
from items.admin.list_displays.price_group_attribute import (
    price_group_attribute_list_display,
)
from items.admin.list_filters.price_group_attribute import (
    price_group_attribute_list_filter,
)

if TYPE_CHECKING:
  from items.admin.price_group_attribute import PriceGroupAttributeAdmin


class TestPriceGroupAttributeAdmin:

  def test_instantiate__inheritance(
      self,
      price_group_attribute_admin: PriceGroupAttributeAdmin,
  ) -> None:
    assert isinstance(price_group_attribute_admin, admin.ModelAdmin)

  def test_instantiate__has_correct_list_display(
      self,
      price_group_attribute_admin: PriceGroupAttributeAdmin,
  ) -> None:
    assert price_group_attribute_admin.list_display == tuple(
        map(str, price_group_attribute_list_display)
    )

  def test_instantiate__has_correct_list_filter(
      self,
      price_group_attribute_admin: PriceGroupAttributeAdmin,
  ) -> None:
    assert price_group_attribute_admin.list_filter == (
        price_group_attribute_list_filter
    )

  def test_instantiate__has_correct_ordering(
      self,
      price_group_attribute_admin: PriceGroupAttributeAdmin,
  ) -> None:
    assert price_group_attribute_admin.ordering == (
        "price_group__name",
        "attribute__name",
    )

  def test_instantiate__has_correct_search_fields(
      self,
      price_group_attribute_admin: PriceGroupAttributeAdmin,
  ) -> None:
    assert price_group_attribute_admin.search_fields == (
        "price_group__name",
        "attribute__name",
    )
