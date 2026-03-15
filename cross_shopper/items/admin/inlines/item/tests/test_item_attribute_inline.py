"""Test the ItemAttribute admin model inline."""

from typing import TYPE_CHECKING

from django.contrib import admin
from items.models.item_attribute import ItemAttribute

if TYPE_CHECKING:  # no cover
  from items.admin.inlines.item.item_attribute import ItemAttributeInline


class TestItemAttributeInline:

  def test_instantiate__inheritance(
      self,
      item_attribute_inline: 'ItemAttributeInline',
  ) -> None:
    assert isinstance(item_attribute_inline, admin.TabularInline)

  def test_instantiate__has_correct_extra(
      self,
      item_attribute_inline: 'ItemAttributeInline',
  ) -> None:
    assert item_attribute_inline.extra == 0

  def test_instantiate__has_correct_ordering(
      self,
      item_attribute_inline: 'ItemAttributeInline',
  ) -> None:
    assert item_attribute_inline.ordering == ('attribute__name',)

  def test_instantiate__has_correct_model(
      self,
      item_attribute_inline: 'ItemAttributeInline',
  ) -> None:
    assert item_attribute_inline.model == ItemAttribute

  def test_instantiate__has_correct_verbose_name(
      self,
      item_attribute_inline: 'ItemAttributeInline',
  ) -> None:
    assert item_attribute_inline.verbose_name == 'Attribute'

  def test_instantiate__has_correct_verbose_name_plural(
      self,
      item_attribute_inline: 'ItemAttributeInline',
  ) -> None:
    assert item_attribute_inline.verbose_name_plural == 'Attributes'
