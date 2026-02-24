"""Test the ScraperFilter class."""

import pytest
from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)
from scrapers.admin.list_filter.scraper_config.scraper_filter import (
    ScraperFilter,
)


@pytest.mark.django_db
class TestScraperFilter:
  """Test the ScraperFilter class."""

  def test_inheritance(self) -> None:
    """Test that ScraperFilter inherits from AdminListFilterBase."""
    assert issubclass(ScraperFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    """Test the ScraperFilter attributes."""
    assert ScraperFilter.title == 'scraper name'
    assert ScraperFilter.parameter_name == 'scraper__name'
