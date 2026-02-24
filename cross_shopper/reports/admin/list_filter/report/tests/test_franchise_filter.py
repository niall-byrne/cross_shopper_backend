"""Test the FranchiseFilter class."""

import pytest
from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)
from reports.admin.list_filter.report.franchise_filter import FranchiseFilter


@pytest.mark.django_db
class TestFranchiseFilter:
  """Test the FranchiseFilter class."""

  def test_inheritance(self) -> None:
    """Test that FranchiseFilter inherits from AdminListFilterBase."""
    assert issubclass(FranchiseFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    """Test the FranchiseFilter attributes."""
    assert FranchiseFilter.title == 'franchise'
    assert FranchiseFilter.parameter_name == 'store__franchise__name'
