"""Test the admin for the PackagingUnit model."""

from items.admin.packaging_unit import PackagingUnitAdmin


class TestPackagingUnit:
  """Test the PackagingUnitAdmin class."""

  def test_instantiate__ordering(
      self,
      packaging_unit_admin: PackagingUnitAdmin,
  ) -> None:
    assert packaging_unit_admin.ordering == ('name',)
