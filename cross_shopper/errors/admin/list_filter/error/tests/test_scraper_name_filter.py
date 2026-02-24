"""Test the ScraperNameFilter class."""

import pytest
from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)
from errors.admin.list_filter.error.scraper_name_filter import (
    ScraperNameFilter,
)


@pytest.mark.django_db
class TestScraperNameFilter:
  """Test the ScraperNameFilter class."""

  def test_inheritance(self) -> None:
    """Test that ScraperNameFilter inherits from AdminListFilterBase."""
    assert issubclass(ScraperNameFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    """Test the ScraperNameFilter attributes."""
    assert ScraperNameFilter.title == 'scraper'
    assert ScraperNameFilter.parameter_name == 'scraper_config__scraper__name'
