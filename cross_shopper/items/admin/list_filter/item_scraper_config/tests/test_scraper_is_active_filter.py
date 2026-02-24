"""Test the ScraperIsActiveFilter class."""

import pytest
from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)
from items.admin.list_filter.item_scraper_config.scraper_is_active_filter import (
    ScraperIsActiveFilter,
)


@pytest.mark.django_db
class TestScraperIsActiveFilter:
  """Test the ScraperIsActiveFilter class."""

  def test_inheritance(self) -> None:
    """Test that ScraperIsActiveFilter inherits from AdminListFilterBase."""
    assert issubclass(ScraperIsActiveFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    """Test the ScraperIsActiveFilter attributes."""
    assert ScraperIsActiveFilter.title == 'is active'
    assert ScraperIsActiveFilter.parameter_name == 'scraper_config__is_active'
    assert ScraperIsActiveFilter.is_boolean is True
