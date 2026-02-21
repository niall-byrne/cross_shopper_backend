"""Test the ItemScraperConfig admin model list filter."""

from items.admin.list_filters.item_scraper_config import (
    item_scraper_config_list_filter,
)
from utilities.admin.list_filters import GenericListFilter
from utilities.testing.comparisons.is_subclass import DynamicSubClass


class TestItemScraperConfigAdminListFilter:

  def test_list_filter(self) -> None:
    assert item_scraper_config_list_filter == (
        DynamicSubClass(
            base=GenericListFilter,
            attributes={
                "title": 'is active',
                "parameter_name": 'scraper_config__is_active',
                "is_boolean": True,
                "is_reversed": False,
            }
        ),
        DynamicSubClass(
            base=GenericListFilter,
            attributes={
                "title": 'scraper',
                "parameter_name": 'scraper_config__scraper__name',
                "is_boolean": False,
                "is_reversed": False,
            }
        ),
        DynamicSubClass(
            base=GenericListFilter,
            attributes={
                "title": 'item',
                "parameter_name": 'item__name',
                "is_boolean": False,
                "is_reversed": False,
            }
        ),
    )
