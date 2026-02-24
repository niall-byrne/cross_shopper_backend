"""Test the ContainerFilter class."""

import pytest
from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)
from items.admin.list_filter.packaging.container_filter import ContainerFilter


class TestContainerFilter:
  """Test the ContainerFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(ContainerFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert ContainerFilter.title == 'container name'
    assert ContainerFilter.parameter_name == 'container__name'
