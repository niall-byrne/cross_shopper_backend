"""Test the Price admin model list filter."""

from pricing.admin.list_filters.price import price_list_filter
from utilities.admin.list_filters import GenericListFilter
from utilities.testing.comparisons.is_subclass import DynamicSubClass


class TestPriceAdminListFilter:

  def test_list_filter(self) -> None:
    assert price_list_filter == (
        DynamicSubClass(
            base=GenericListFilter,
            attributes={
                "title": "item",
                "parameter_name": "item__name",
                "is_boolean": False,
                "is_reversed": False,
            }
        ),
        DynamicSubClass(
            base=GenericListFilter,
            attributes={
                "title": "brand",
                "parameter_name": "item__brand__name",
                "is_boolean": False,
                "is_reversed": False,
            }
        ),
        DynamicSubClass(
            base=GenericListFilter,
            attributes={
                "title": "franchise",
                "parameter_name": "store__franchise__name",
                "is_boolean": False,
                "is_reversed": False,
            }
        ),
        DynamicSubClass(
            base=GenericListFilter,
            attributes={
                "title": "location",
                "parameter_name": "store__address__locality__name",
                "is_boolean": False,
                "is_reversed": False,
            }
        ),
        DynamicSubClass(
            base=GenericListFilter,
            attributes={
                "title": "year",
                "parameter_name": "year",
                "is_boolean": False,
                "is_reversed": True,
            }
        ),
        "week",
    )
