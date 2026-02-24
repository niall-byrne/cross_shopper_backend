"""Test the LocationFilter class."""

import pytest
from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)
from reports.admin.list_filter.report.location_filter import LocationFilter


@pytest.mark.django_db
class TestLocationFilter:
  """Test the LocationFilter class."""

  def test_inheritance(self) -> None:
    """Test that LocationFilter inherits from AdminListFilterBase."""
    assert issubclass(LocationFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    """Test the LocationFilter attributes."""
    assert LocationFilter.title == 'location'
    assert LocationFilter.parameter_name == 'store__address__locality__name'
