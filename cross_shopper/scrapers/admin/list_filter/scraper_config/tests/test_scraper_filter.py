"""Test the ScraperFilter class."""

import pytest
from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)
from scrapers.admin.list_filter.scraper_config.scraper_filter import (
    ScraperFilter,
)


class TestScraperFilter:
  """Test the ScraperFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(ScraperFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert ScraperFilter.title == 'scraper name'
    assert ScraperFilter.parameter_name == 'scraper__name'
