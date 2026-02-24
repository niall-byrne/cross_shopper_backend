"""Test the franchise model list filters."""

from stores.admin.filters.franchise import (
    ScraperFilter,
)
from utilities.admin.filters.bases.base_admin_list_filter import (
    AdminListFilterBase,
)


class TestScraperFilter:
  """Test the ScraperFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(ScraperFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert ScraperFilter.title == 'scraper'
    assert ScraperFilter.parameter_name == 'scraper__name'
