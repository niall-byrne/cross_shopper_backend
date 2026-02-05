"""Test the admin for the Franchise model."""

from django.contrib import admin
from stores.admin.franchise import FranchiseAdmin


class TestFranchiseAdmin:
  """Test the FranchiseAdmin class."""

  def test_instantiate__inheritance(
      self, franchise_admin: FranchiseAdmin
  ) -> None:
    assert isinstance(franchise_admin, admin.ModelAdmin)

  def test_instantiate__ordering(self, franchise_admin: FranchiseAdmin) -> None:
    assert franchise_admin.ordering == ('name',)
