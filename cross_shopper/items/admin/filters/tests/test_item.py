"""Test the item model list filters."""

from utilities.admin.filters.bases.base_admin_list_filter import (
    AdminListFilterBase,
)
from items.admin.filters.item import (
    BrandFilter,
    ContainerFilter,
    NameFilter,
)


class TestContainerFilter:
  """Test the ContainerFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(ContainerFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert ContainerFilter.title == 'packaging'
    assert ContainerFilter.parameter_name == 'packaging__container__name'


class TestBrandFilter:
  """Test the BrandFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(BrandFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert BrandFilter.title == 'brand'
    assert BrandFilter.parameter_name == 'brand__name'


class TestNameFilter:
  """Test the NameFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(NameFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert NameFilter.title == 'name'
    assert NameFilter.parameter_name == 'name'
