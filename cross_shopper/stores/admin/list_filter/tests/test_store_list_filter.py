"""Test the Store admin model list filter."""

from stores.admin.list_filter.store import store_list_filter
from utilities.admin.list_filter import GenericListFilter
from utilities.testing.comparisons.is_subclass import DynamicSubClass


class TestStoreAdminListFilter:

  def test_list_filter(self) -> None:
    assert store_list_filter == (
        DynamicSubClass(
            base=GenericListFilter,
            attributes={
                "title": 'franchise',
                "parameter_name": 'franchise__name',
                "is_boolean": False,
                "is_reversed": False,
            }
        ),
        DynamicSubClass(
            base=GenericListFilter,
            attributes={
                "title": 'location',
                "parameter_name": 'address__locality__name',
                "is_boolean": False,
                "is_reversed": False,
            }
        ),
    )
