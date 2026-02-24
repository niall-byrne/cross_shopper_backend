"""Test the YearFilter class."""

import pytest
from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)
from pricing.admin.list_filter.price.year_filter import YearFilter


@pytest.mark.django_db
class TestYearFilter:
  """Test the YearFilter class."""

  def test_inheritance(self) -> None:
    """Test that YearFilter inherits from AdminListFilterBase."""
    assert issubclass(YearFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    """Test the YearFilter attributes."""
    assert YearFilter.title == 'year'
    assert YearFilter.parameter_name == 'year'
    assert YearFilter.is_reversed is True
