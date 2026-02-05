"""Test the admin for the PackagingContainer model."""

from items.admin.packaging_container import PackagingContainerAdmin


class TestIPackagingContainer:
  """Test the PackagingContainer class."""

  def test_instantiate__ordering(
      self,
      packaging_container_admin: PackagingContainerAdmin,
  ) -> None:
    assert packaging_container_admin.ordering == ('name',)
