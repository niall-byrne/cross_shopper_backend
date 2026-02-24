"""Test the ErrorTypeFilter class."""

import pytest
from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)
from errors.admin.list_filter.error.error_type_filter import ErrorTypeFilter


class TestErrorTypeFilter:
  """Test the ErrorTypeFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(ErrorTypeFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert ErrorTypeFilter.title == 'type'
    assert ErrorTypeFilter.parameter_name == 'type__name'
