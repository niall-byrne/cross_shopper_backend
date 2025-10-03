"""Test the admin for the PackagingContainer model."""

from django.contrib import admin
from items.admin.packaging_container import PackagingContainerAdmin


class TestPackagingContainerAdmin:

  def test_instantiate__inheritance(
      self,
      packaging_container_admin: PackagingContainerAdmin,
  ) -> None:
    assert isinstance(packaging_container_admin, admin.ModelAdmin)

  def test_instantiate__has_correct_ordering(
      self,
      packaging_container_admin: PackagingContainerAdmin,
  ) -> None:
    assert packaging_container_admin.ordering == ("name",)
