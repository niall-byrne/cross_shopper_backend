"""Test the PriceGroupAttribute admin model inline."""

from typing import TYPE_CHECKING

from django.contrib import admin
from items.models.price_group_attribute import PriceGroupAttribute

if TYPE_CHECKING:  # no cover
  from items.admin.inlines.price_group.price_group_attribute import (
      PriceGroupAttributeInline,
  )


class TestPriceGroupAttributeInline:

  def test_instantiate__inheritance(
      self,
      price_group_attribute_inline: "PriceGroupAttributeInline",
  ) -> None:
    assert isinstance(price_group_attribute_inline, admin.TabularInline)

  def test_instantiate__has_correct_extra(
      self,
      price_group_attribute_inline: "PriceGroupAttributeInline",
  ) -> None:
    assert price_group_attribute_inline.extra == 0

  def test_instantiate__has_correct_ordering(
      self,
      price_group_attribute_inline: "PriceGroupAttributeInline",
  ) -> None:
    assert price_group_attribute_inline.ordering == ("attribute__name",)

  def test_instantiate__has_correct_model(
      self,
      price_group_attribute_inline: "PriceGroupAttributeInline",
  ) -> None:
    assert price_group_attribute_inline.model == PriceGroupAttribute

  def test_instantiate__has_correct_verbose_name(
      self,
      price_group_attribute_inline: "PriceGroupAttributeInline",
  ) -> None:
    assert price_group_attribute_inline.verbose_name == "Attribute"

  def test_instantiate__has_correct_verbose_name_plural(
      self,
      price_group_attribute_inline: "PriceGroupAttributeInline",
  ) -> None:
    assert price_group_attribute_inline.verbose_name_plural == "Attributes"
