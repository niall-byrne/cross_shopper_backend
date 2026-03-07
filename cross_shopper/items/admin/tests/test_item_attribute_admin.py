"""Test the admin for the ItemAttribute model."""

from typing import TYPE_CHECKING

from django.contrib import admin
from items.admin.list_displays.item_attribute import (
    item_attribute_list_display,
)
from items.admin.list_filters.item_attribute import (
    item_attribute_list_filter,
)

if TYPE_CHECKING:  # no cover
  from items.admin.item_attribute import ItemAttributeAdmin


class TestItemAttributeAdmin:

  def test_instantiate__inheritance(
      self,
      item_attribute_admin: "ItemAttributeAdmin",
  ) -> None:
    assert isinstance(item_attribute_admin, admin.ModelAdmin)

  def test_instantiate__has_correct_list_display(
      self,
      item_attribute_admin: "ItemAttributeAdmin",
  ) -> None:
    assert item_attribute_admin.list_display == tuple(
        map(str, item_attribute_list_display)
    )

  def test_instantiate__has_correct_list_filter(
      self,
      item_attribute_admin: "ItemAttributeAdmin",
  ) -> None:
    assert item_attribute_admin.list_filter == (item_attribute_list_filter)

  def test_instantiate__has_correct_ordering(
      self,
      item_attribute_admin: "ItemAttributeAdmin",
  ) -> None:
    assert item_attribute_admin.ordering == (
        "item__name",
        "attribute__name",
    )

  def test_instantiate__has_correct_search_fields(
      self,
      item_attribute_admin: "ItemAttributeAdmin",
  ) -> None:
    assert item_attribute_admin.search_fields == (
        "item__name",
        "attribute__name",
    )
