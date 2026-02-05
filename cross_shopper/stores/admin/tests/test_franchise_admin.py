"""Test the admin for the Franchise model."""

from django.contrib import admin
from stores.admin.franchise import FranchiseAdmin
from stores.admin.list_filter.franchise import franchise_list_filter


class TestFranchiseAdmin:
  """Test the FranchiseAdmin class."""

  def test_instantiate__inheritance(
      self,
      franchise_admin: FranchiseAdmin,
  ) -> None:
    assert isinstance(franchise_admin, admin.ModelAdmin)

  def test_instantiate__has_correct_list_filter(
      self,
      franchise_admin: FranchiseAdmin,
  ) -> None:
    assert franchise_admin.list_filter == franchise_list_filter

  def test_instantiate__has_correct_ordering(
      self,
      franchise_admin: FranchiseAdmin,
  ) -> None:
    assert franchise_admin.ordering == ('name',)
