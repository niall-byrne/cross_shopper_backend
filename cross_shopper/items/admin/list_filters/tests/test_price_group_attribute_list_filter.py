"""Test the PriceGroupAttribute admin model list filter."""

from items.admin.list_filters.price_group_attribute import (
    price_group_attribute_list_filter,
)
from utilities.admin.list_filters import GenericListFilter
from utilities.testing.comparisons.is_subclass import DynamicSubClass


class TestPriceGroupAttributeAdminListFilter:

  def test_list_filter(self) -> None:
    assert price_group_attribute_list_filter == (
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
                "title": "price group",
                "parameter_name": "price_group__name",
                "is_boolean": False,
                "is_reversed": False,
            },
        ),
    )
