"""Test the packaging model list filters."""

from items.admin.filters.packaging import (
    ContainerFilter,
    UnitFilter,
)
from utilities.admin.filters.bases.base_admin_list_filter import (
    AdminListFilterBase,
)


class TestContainerFilter:
  """Test the ContainerFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(ContainerFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert ContainerFilter.title == 'container name'
    assert ContainerFilter.parameter_name == 'container__name'


class TestUnitFilter:
  """Test the UnitFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(UnitFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert UnitFilter.title == 'unit name'
    assert UnitFilter.parameter_name == 'unit__name'
