"""Test the FranchiseFilter class."""

import pytest
from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)
from reports.admin.list_filter.report.franchise_filter import FranchiseFilter


class TestFranchiseFilter:
  """Test the FranchiseFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(FranchiseFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert FranchiseFilter.title == 'franchise'
    assert FranchiseFilter.parameter_name == 'store__franchise__name'
