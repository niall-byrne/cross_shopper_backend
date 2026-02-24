"""Test the error model list filters."""

from utilities.admin.filters.bases.base_admin_list_filter import (
    AdminListFilterBase,
)
from errors.admin.filters.error import (
    ErrorTypeFilter,
    FranchiseNameFilter,
    IsReoccurringFilter,
    ItemNameFilter,
    ScraperConfigIsActiveFilter,
    ScraperNameFilter,
)


class TestErrorTypeFilter:
  """Test the ErrorTypeFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(ErrorTypeFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert ErrorTypeFilter.title == 'type'
    assert ErrorTypeFilter.parameter_name == 'type__name'


class TestFranchiseNameFilter:
  """Test the FranchiseNameFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(FranchiseNameFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert FranchiseNameFilter.title == 'franchise'
    assert FranchiseNameFilter.parameter_name == 'store__franchise__name'


class TestIsReoccurringFilter:
  """Test the IsReoccurringFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(IsReoccurringFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert IsReoccurringFilter.title == 'is_reoccurring'
    assert IsReoccurringFilter.parameter_name == 'is_reoccurring'
    assert IsReoccurringFilter.is_boolean is True


class TestItemNameFilter:
  """Test the ItemNameFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(ItemNameFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert ItemNameFilter.title == 'item'
    assert ItemNameFilter.parameter_name == 'item__name'


class TestScraperConfigIsActiveFilter:
  """Test the ScraperConfigIsActiveFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(ScraperConfigIsActiveFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert ScraperConfigIsActiveFilter.title == 'scraper_config active'
    assert ScraperConfigIsActiveFilter.parameter_name == 'scraper_config__is_active'
    assert ScraperConfigIsActiveFilter.is_boolean is True


class TestScraperNameFilter:
  """Test the ScraperNameFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(ScraperNameFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert ScraperNameFilter.title == 'scraper'
    assert ScraperNameFilter.parameter_name == 'scraper_config__scraper__name'
