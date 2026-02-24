"""Test the NameFilter class."""

import pytest
from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)
from items.admin.list_filter.item.name_filter import NameFilter


class TestNameFilter:
  """Test the NameFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(NameFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert NameFilter.title == 'name'
    assert NameFilter.parameter_name == 'name'
