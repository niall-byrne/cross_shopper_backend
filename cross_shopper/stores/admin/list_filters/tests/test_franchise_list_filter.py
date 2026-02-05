"""Test the Franchise admin model list filter."""

from stores.admin.list_filters.franchise import franchise_list_filter
from utilities.admin.list_filters import GenericListFilter
from utilities.testing.comparisons.is_subclass import DynamicSubClass


class TestFranchiseAdminListFilter:

  def test_list_filter(self) -> None:
    assert franchise_list_filter == (
        DynamicSubClass(
            base=GenericListFilter,
            attributes={
                "title": "scraper",
                "parameter_name": "scraper__name",
                "is_boolean": False,
                "is_reversed": False,
            }
        ),
    )
