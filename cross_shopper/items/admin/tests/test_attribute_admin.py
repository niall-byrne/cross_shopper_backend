"""Test the admin for the Attribute model."""

from django.contrib import admin
from items.admin.attribute import AttributeAdmin
from items.admin.list_displays.attribute import (
    attribute_list_display,
)
from items.admin.list_filters.attribute import (
    attribute_list_filter,
)


class TestAttributeAdmin:

  def test_instantiate__inheritance(
      self,
      attribute_admin: AttributeAdmin,
  ) -> None:
    assert isinstance(attribute_admin, admin.ModelAdmin)

  def test_instantiate__has_correct_list_display(
      self,
      attribute_admin: AttributeAdmin,
  ) -> None:
    assert attribute_admin.list_display == tuple(
        map(str, attribute_list_display)
    )

  def test_instantiate__has_correct_list_filter(
      self,
      attribute_admin: AttributeAdmin,
  ) -> None:
    assert attribute_admin.list_filter == attribute_list_filter

  def test_instantiate__has_correct_ordering(
      self,
      attribute_admin: AttributeAdmin,
  ) -> None:
    assert attribute_admin.ordering == ('name',)
