"""Test the ScraperConfigIsActiveFilter class."""

import pytest
from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)
from errors.admin.list_filter.error.scraper_config_is_active_filter import (
    ScraperConfigIsActiveFilter,
)


@pytest.mark.django_db
class TestScraperConfigIsActiveFilter:
  """Test the ScraperConfigIsActiveFilter class."""

  def test_inheritance(self) -> None:
    """Test that ScraperConfigIsActiveFilter inherits from AdminListFilterBase."""
    assert issubclass(ScraperConfigIsActiveFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    """Test the ScraperConfigIsActiveFilter attributes."""
    assert ScraperConfigIsActiveFilter.title == 'scraper_config active'
    assert ScraperConfigIsActiveFilter.parameter_name == 'scraper_config__is_active'
    assert ScraperConfigIsActiveFilter.is_boolean is True
