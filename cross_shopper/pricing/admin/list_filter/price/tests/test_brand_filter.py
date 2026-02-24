"""Test the BrandFilter class."""

import pytest
from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)
from pricing.admin.list_filter.price.brand_filter import BrandFilter


class TestBrandFilter:
  """Test the BrandFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(BrandFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert BrandFilter.title == 'brand'
    assert BrandFilter.parameter_name == 'item__brand__name'
