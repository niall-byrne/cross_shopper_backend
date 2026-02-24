"""Test the ItemFilter class."""

import pytest
from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)
from items.admin.list_filter.item_scraper_config.item_filter import ItemFilter


class TestItemFilter:
  """Test the ItemFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(ItemFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert ItemFilter.title == 'item name'
    assert ItemFilter.parameter_name == 'item__name'
