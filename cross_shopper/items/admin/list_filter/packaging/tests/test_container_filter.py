"""Test the ContainerFilter class."""

import pytest
from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)
from items.admin.list_filter.packaging.container_filter import ContainerFilter


@pytest.mark.django_db
class TestContainerFilter:
  """Test the ContainerFilter class."""

  def test_inheritance(self) -> None:
    """Test that ContainerFilter inherits from AdminListFilterBase."""
    assert issubclass(ContainerFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    """Test the ContainerFilter attributes."""
    assert ContainerFilter.title == 'container name'
    assert ContainerFilter.parameter_name == 'container__name'
