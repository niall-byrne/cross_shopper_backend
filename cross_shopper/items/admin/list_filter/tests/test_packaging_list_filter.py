"""Test the Packaging admin model list filter."""

from items.admin.list_filter.packaging import packaging_list_filter
from utilities.admin.list_filter import GenericListFilter
from utilities.testing.comparisons.is_subclass import DynamicSubClass


class TestPackagingAdminListFilter:

  def test_list_filter(self) -> None:
    assert packaging_list_filter == (
        DynamicSubClass(
            base=GenericListFilter,
            attributes={
                "title": 'container',
                "parameter_name": 'container__name',
                "is_boolean": False,
                "is_reversed": False,
            }
        ),
        DynamicSubClass(
            base=GenericListFilter,
            attributes={
                "title": 'unit',
                "parameter_name": 'unit__name',
                "is_boolean": False,
                "is_reversed": False,
            }
        ),
    )
