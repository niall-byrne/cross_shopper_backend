"""Test the BrandFilter class."""

import pytest
from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)
from items.admin.list_filter.item.brand_filter import BrandFilter


class TestBrandFilter:
  """Test the BrandFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(BrandFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert BrandFilter.title == 'brand'
    assert BrandFilter.parameter_name == 'brand__name'
