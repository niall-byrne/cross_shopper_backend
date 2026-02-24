"""Test the UnitFilter class."""

import pytest
from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)
from items.admin.list_filter.packaging.unit_filter import UnitFilter


class TestUnitFilter:
  """Test the UnitFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(UnitFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert UnitFilter.title == 'unit name'
    assert UnitFilter.parameter_name == 'unit__name'
