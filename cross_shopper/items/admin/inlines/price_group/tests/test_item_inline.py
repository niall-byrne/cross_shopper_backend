"""Test the PriceGroupItem admin model inline."""

from django.contrib import admin
from items.admin.inlines.price_group.item import (
    PriceGroupItemInline,
)
from items.models.item import Item


class TestPriceGroupItemInline:

  def test_instantiate__inheritance(
      self,
      price_group_item_inline: PriceGroupItemInline,
  ) -> None:
    assert isinstance(price_group_item_inline, admin.TabularInline)

  def test_instantiate__has_correct_extra(
      self,
      price_group_item_inline: PriceGroupItemInline,
  ) -> None:
    assert price_group_item_inline.extra == 0

  def test_instantiate__has_correct_fields(
      self,
      price_group_item_inline: PriceGroupItemInline,
  ) -> None:
    assert price_group_item_inline.fields == (
        'name',
        'brand',
        'packaging',
        'is_non_gmo',
        'is_organic',
    )

  def test_instantiate__has_correct_ordering(
      self,
      price_group_item_inline: PriceGroupItemInline,
  ) -> None:
    assert price_group_item_inline.ordering == (
        'name',
        'brand__name',
        'is_organic',
        'packaging__container',
        'packaging__quantity',
    )

  def test_instantiate__has_show_change_link(
      self,
      price_group_item_inline: PriceGroupItemInline,
  ) -> None:
    assert price_group_item_inline.show_change_link is True

  def test_instantiate__has_correct_model(
      self,
      price_group_item_inline: PriceGroupItemInline,
  ) -> None:
    assert price_group_item_inline.model == Item

  def test_instantiate__has_correct_verbose_name(
      self,
      price_group_item_inline: PriceGroupItemInline,
  ) -> None:
    assert price_group_item_inline.verbose_name == 'Member'

  def test_instantiate__has_correct_verbose_name_plural(
      self,
      price_group_item_inline: PriceGroupItemInline,
  ) -> None:
    assert price_group_item_inline.verbose_name_plural == 'Members'
