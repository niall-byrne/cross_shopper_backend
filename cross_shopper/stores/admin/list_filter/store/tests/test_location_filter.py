"""Test the LocationFilter class."""

import pytest
from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)
from stores.admin.list_filter.store.location_filter import LocationFilter


class TestLocationFilter:
  """Test the LocationFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(LocationFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert LocationFilter.title == 'location'
    assert LocationFilter.parameter_name == 'address__locality__name'
