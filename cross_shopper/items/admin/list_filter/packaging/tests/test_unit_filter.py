"""Test the UnitFilter class."""

import pytest
from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)
from items.admin.list_filter.packaging.unit_filter import UnitFilter


@pytest.mark.django_db
class TestUnitFilter:
  """Test the UnitFilter class."""

  def test_inheritance(self) -> None:
    """Test that UnitFilter inherits from AdminListFilterBase."""
    assert issubclass(UnitFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    """Test the UnitFilter attributes."""
    assert UnitFilter.title == 'unit name'
    assert UnitFilter.parameter_name == 'unit__name'
