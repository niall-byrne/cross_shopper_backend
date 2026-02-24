"""Test the ItemFilter class."""

import pytest
from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)
from pricing.admin.list_filter.price.item_filter import ItemFilter


class TestItemFilter:
  """Test the ItemFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(ItemFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert ItemFilter.title == 'item'
    assert ItemFilter.parameter_name == 'item__name'
