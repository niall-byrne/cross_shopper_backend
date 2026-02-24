"""Test the ItemNameFilter class."""

import pytest
from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)
from errors.admin.list_filter.error.item_name_filter import ItemNameFilter


class TestItemNameFilter:
  """Test the ItemNameFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(ItemNameFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert ItemNameFilter.title == 'item'
    assert ItemNameFilter.parameter_name == 'item__name'
