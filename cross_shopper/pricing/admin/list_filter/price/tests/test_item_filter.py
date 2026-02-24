"""Test the ItemFilter class."""

import pytest
from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)
from pricing.admin.list_filter.price.item_filter import ItemFilter


@pytest.mark.django_db
class TestItemFilter:
  """Test the ItemFilter class."""

  def test_inheritance(self) -> None:
    """Test that ItemFilter inherits from AdminListFilterBase."""
    assert issubclass(ItemFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    """Test the ItemFilter attributes."""
    assert ItemFilter.title == 'item'
    assert ItemFilter.parameter_name == 'item__name'
