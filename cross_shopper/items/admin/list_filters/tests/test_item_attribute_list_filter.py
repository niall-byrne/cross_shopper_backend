"""Test the ItemAttribute admin model list filter."""

from items.admin.list_filters.item_attribute import (
    item_attribute_list_filter,
)
from utilities.admin.list_filters import GenericListFilter
from utilities.testing.comparisons.is_subclass import DynamicSubClass


class TestItemAttributeAdminListFilter:

  def test_list_filter(self) -> None:
    assert item_attribute_list_filter == (
        DynamicSubClass(
            base=GenericListFilter,
            attributes={
                "title": "attribute",
                "parameter_name": "attribute__name",
                "is_boolean": False,
                "is_reversed": False,
            },
        ),
        DynamicSubClass(
            base=GenericListFilter,
            attributes={
                "title": "item",
                "parameter_name": "item__name",
                "is_boolean": False,
                "is_reversed": False,
            },
        ),
    )
