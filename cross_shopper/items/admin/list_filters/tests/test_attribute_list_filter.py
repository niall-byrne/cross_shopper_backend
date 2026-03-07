"""Test the Attribute admin model list filter."""

from items.admin.list_filters.attribute import attribute_list_filter
from items.admin.list_filters.filters.attribute.has_items import (
    HasItemsFilter,
)


class TestAttributeListFilter:

  def test_list_filter(self) -> None:
    assert attribute_list_filter == (HasItemsFilter,)
