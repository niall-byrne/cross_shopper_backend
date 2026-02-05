"""Test the admin for the Packaging model."""

from django.contrib import admin
from items.admin.packaging import PackagingAdmin


class TestPackagingAdmin:
  """Test the PackagingAdmin class."""

  def test_instantiate__inheritance(
      self, packaging_admin: PackagingAdmin
  ) -> None:
    assert isinstance(packaging_admin, admin.ModelAdmin)

  def test_instantiate__ordering(self, packaging_admin: PackagingAdmin) -> None:
    assert packaging_admin.ordering == ('container__name', 'unit__name')
