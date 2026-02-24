"""Test the store model list filters."""

from utilities.admin.filters.bases.base_admin_list_filter import (
    AdminListFilterBase,
)
from stores.admin.filters.store import (
    FranchiseFilter,
    LocationFilter,
)


class TestFranchiseFilter:
  """Test the FranchiseFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(FranchiseFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert FranchiseFilter.title == 'franchise'
    assert FranchiseFilter.parameter_name == 'franchise__name'


class TestLocationFilter:
  """Test the LocationFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(LocationFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert LocationFilter.title == 'location'
    assert LocationFilter.parameter_name == 'address__locality__name'
