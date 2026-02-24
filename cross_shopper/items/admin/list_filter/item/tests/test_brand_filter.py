"""Test the BrandFilter class."""

import pytest
from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)
from items.admin.list_filter.item.brand_filter import BrandFilter


@pytest.mark.django_db
class TestBrandFilter:
  """Test the BrandFilter class."""

  def test_inheritance(self) -> None:
    """Test that BrandFilter inherits from AdminListFilterBase."""
    assert issubclass(BrandFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    """Test the BrandFilter attributes."""
    assert BrandFilter.title == 'brand'
    assert BrandFilter.parameter_name == 'brand__name'
