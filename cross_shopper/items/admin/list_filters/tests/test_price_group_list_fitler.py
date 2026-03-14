"""Test the PriceGroup admin model list filter."""

from items.admin.list_filters.filters.price_group.in_use import (
    InUseFilter,
)
from items.admin.list_filters.price_group import (
    price_group_list_filter,
)
from utilities.admin.list_filters.generic_list_filter import GenericListFilter
from utilities.testing.comparisons.is_subclass import DynamicSubClass


class TestPriceGroupAdminListFilter:

  def test_list_filter(self) -> None:
    assert price_group_list_filter == (
        InUseFilter,
        DynamicSubClass(
            base=GenericListFilter,
            attributes={
                "title": "name",
                "parameter_name": "name",
                "is_boolean": False,
                "is_reversed": False,
            }
        ),
        DynamicSubClass(
            base=GenericListFilter,
            attributes={
                "title": "unit",
                "parameter_name": "unit__name",
                "is_boolean": False,
                "is_reversed": False,
            }
        ),
        DynamicSubClass(
            base=GenericListFilter,
            attributes={
                "title": "attribute",
                "parameter_name": "attribute__name",
                "is_boolean": False,
                "is_reversed": False,
            }
        ),
    )
