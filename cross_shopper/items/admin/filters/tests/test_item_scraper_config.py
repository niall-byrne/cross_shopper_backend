"""Test the item scraper config model list filters."""

from utilities.admin.filters.bases.base_admin_list_filter import (
    AdminListFilterBase,
)
from items.admin.filters.item_scraper_config import (
    ItemFilter,
    ScraperFilter,
    ScraperIsActiveFilter,
)


class TestItemFilter:
  """Test the ItemFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(ItemFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert ItemFilter.title == 'item name'
    assert ItemFilter.parameter_name == 'item__name'


class TestScraperFilter:
  """Test the ScraperFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(ScraperFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert ScraperFilter.title == 'scraper name'
    assert ScraperFilter.parameter_name == 'scraper_config__scraper__name'


class TestScraperIsActiveFilter:
  """Test the ScraperIsActiveFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(ScraperIsActiveFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert ScraperIsActiveFilter.title == 'is active'
    assert ScraperIsActiveFilter.parameter_name == 'scraper_config__is_active'
    assert ScraperIsActiveFilter.is_boolean is True
