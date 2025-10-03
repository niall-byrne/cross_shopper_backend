"""Test the admin for the PackagingContainer model."""

from unittest import mock

from items.admin.packaging_container import PackagingContainerAdmin


class TestIPackagingContainer:
  """Test the PackagingContainer class."""

  def test_get_ordering__returns_correct_field_order(
      self,
      packaging_container_admin: PackagingContainerAdmin,
      mocked_request: mock.Mock,
  ) -> None:
    field_order = packaging_container_admin.get_ordering(mocked_request)

    assert field_order == ('name',)
