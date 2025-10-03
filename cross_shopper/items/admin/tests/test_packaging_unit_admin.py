"""Test the admin for the PackagingUnit model."""

from django.contrib import admin
from items.admin.packaging_unit import PackagingUnitAdmin


class TestPackagingUnitAdmin:
  """Test the PackagingUnitAdmin class."""

  def test_instantiate__inheritance(
      self,
      packaging_unit_admin: PackagingUnitAdmin,
  ) -> None:
    assert isinstance(packaging_unit_admin, admin.ModelAdmin)

  def test_instantiate__has_correct_ordering(
      self,
      packaging_unit_admin: PackagingUnitAdmin,
  ) -> None:
    assert packaging_unit_admin.ordering == ("name",)
