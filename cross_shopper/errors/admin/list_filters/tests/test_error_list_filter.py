"""Test the Error admin model list filter."""

from errors.admin.list_filters.error import error_list_filter
from utilities.admin.list_filters import GenericListFilter
from utilities.testing.comparisons.is_subclass import DynamicSubClass


class TestErrorAdminListFilter:

  def test_list_filter(self) -> None:
    assert error_list_filter == (
        DynamicSubClass(
            base=GenericListFilter,
            attributes={
                "title": "type",
                "parameter_name": "type__name",
                "is_boolean": False,
                "is_reversed": False,
            }
        ),
        "is_reoccurring",
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
                "title": "item",
                "parameter_name": "item__name",
                "is_boolean": False,
                "is_reversed": False,
            }
        ),
        DynamicSubClass(
            base=GenericListFilter,
            attributes={
                "title": "scraper",
                "parameter_name": "scraper_config__scraper__name",
                "is_boolean": False,
                "is_reversed": False,
            }
        ),
        DynamicSubClass(
            base=GenericListFilter,
            attributes={
                "title": "scraper config active",
                "parameter_name": "scraper_config__is_active",
                "is_boolean": True,
                "is_reversed": False,
            }
        ),
    )
