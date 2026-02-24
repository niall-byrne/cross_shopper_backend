"""Test the FranchiseNameFilter class."""

import pytest
from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)
from errors.admin.list_filter.error.franchise_name_filter import (
    FranchiseNameFilter,
)


class TestFranchiseNameFilter:
  """Test the FranchiseNameFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(FranchiseNameFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert FranchiseNameFilter.title == 'franchise'
    assert FranchiseNameFilter.parameter_name == 'store__franchise__name'
