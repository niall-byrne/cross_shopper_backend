"""Test the Item admin model list filter."""

from items.admin.list_filter.item import item_list_filter
from utilities.admin.list_filter import GenericListFilter
from utilities.testing.comparisons.is_subclass import DynamicSubClass


class TestItemAdminListFilter:

  def test_list_filter(self) -> None:
    assert item_list_filter == (
        'is_non_gmo',
        'is_organic',
        DynamicSubClass(
            base=GenericListFilter,
            attributes={
                "title": 'brand',
                "parameter_name": 'brand__name',
                "is_boolean": False,
                "is_reversed": False,
            }
        ),
        DynamicSubClass(
            base=GenericListFilter,
            attributes={
                "title": 'packaging',
                "parameter_name": 'packaging__container__name',
                "is_boolean": False,
                "is_reversed": False,
            }
        ),
        'name',
    )
