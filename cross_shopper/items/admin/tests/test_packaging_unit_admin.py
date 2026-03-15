"""Test the admin for the PackagingUnit model."""

from typing import TYPE_CHECKING

from django.contrib import admin

if TYPE_CHECKING:  # no cover
  from items.admin.packaging_unit import PackagingUnitAdmin


class TestPackagingUnitAdmin:

  def test_instantiate__inheritance(
      self,
      packaging_unit_admin: "PackagingUnitAdmin",
  ) -> None:
    assert isinstance(packaging_unit_admin, admin.ModelAdmin)

  def test_instantiate__has_correct_ordering(
      self,
      packaging_unit_admin: "PackagingUnitAdmin",
  ) -> None:
    assert packaging_unit_admin.ordering == ("name",)
