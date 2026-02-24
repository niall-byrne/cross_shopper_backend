"""Test the ItemNameFilter class."""

import pytest
from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)
from errors.admin.list_filter.error.item_name_filter import ItemNameFilter


@pytest.mark.django_db
class TestItemNameFilter:
  """Test the ItemNameFilter class."""

  def test_inheritance(self) -> None:
    """Test that ItemNameFilter inherits from AdminListFilterBase."""
    assert issubclass(ItemNameFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    """Test the ItemNameFilter attributes."""
    assert ItemNameFilter.title == 'item'
    assert ItemNameFilter.parameter_name == 'item__name'
