"""Test the IsReoccurringFilter class."""

import pytest
from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)
from errors.admin.list_filter.error.is_reoccurring_filter import (
    IsReoccurringFilter,
)


class TestIsReoccurringFilter:
  """Test the IsReoccurringFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(IsReoccurringFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert IsReoccurringFilter.title == 'is_reoccurring'
    assert IsReoccurringFilter.parameter_name == 'is_reoccurring'
    assert IsReoccurringFilter.is_boolean is True
