"""Test the report model list filters."""

from reports.admin.filters.report import (
    FranchiseFilter,
    ItemFilter,
    LocationFilter,
)
from utilities.admin.filters.bases.base_admin_list_filter import (
    AdminListFilterBase,
)


class TestItemFilter:
  """Test the ItemFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(ItemFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert ItemFilter.title == 'item'
    assert ItemFilter.parameter_name == 'item__name'


class TestFranchiseFilter:
  """Test the FranchiseFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(FranchiseFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert FranchiseFilter.title == 'franchise'
    assert FranchiseFilter.parameter_name == 'store__franchise__name'


class TestLocationFilter:
  """Test the LocationFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(LocationFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert LocationFilter.title == 'location'
    assert LocationFilter.parameter_name == 'store__address__locality__name'
