"""Test the admin for the PackagingUnit model."""

from items.admin.packaging_unit import PackagingUnitAdmin


class TestIPackagingUnit:
  """Test the PackagingUnit class."""

  def test_instantiate__ordering(
      self,
      packaging_unit_admin: PackagingUnitAdmin,
  ) -> None:
    assert packaging_unit_admin.ordering == ('name',)
