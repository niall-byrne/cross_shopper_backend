"""Test the FranchiseNameFilter class."""

import pytest
from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)
from errors.admin.list_filter.error.franchise_name_filter import (
    FranchiseNameFilter,
)


@pytest.mark.django_db
class TestFranchiseNameFilter:
  """Test the FranchiseNameFilter class."""

  def test_inheritance(self) -> None:
    """Test that FranchiseNameFilter inherits from AdminListFilterBase."""
    assert issubclass(FranchiseNameFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    """Test the FranchiseNameFilter attributes."""
    assert FranchiseNameFilter.title == 'franchise'
    assert FranchiseNameFilter.parameter_name == 'store__franchise__name'
