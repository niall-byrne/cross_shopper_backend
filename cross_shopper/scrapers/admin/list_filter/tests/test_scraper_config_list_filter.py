"""Test the ScraperConfig admin model list filter."""

from scrapers.admin.list_filter.scraper_config import scraper_config_list_filter
from utilities.admin.list_filter import GenericListFilter
from utilities.testing.comparisons.is_subclass import DynamicSubClass


class TestScraperConfigListFilter:

  def test_list_filter(self) -> None:
    assert scraper_config_list_filter == (
        "is_active",
        DynamicSubClass(
            base=GenericListFilter,
            attributes={
                "title": 'scraper',
                "parameter_name": 'scraper__name',
                "is_boolean": False,
                "is_reversed": False,
            }
        ),
    )
