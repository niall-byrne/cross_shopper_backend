"""Test the admin for the Store model."""

from django.contrib import admin
from stores.admin.store import StoreAdmin


class TestStoreAdmin:
  """Test the StoreAdmin class."""

  def test_instantiate__inheritance(self, store_admin: StoreAdmin) -> None:
    assert isinstance(store_admin, admin.ModelAdmin)

  def test_instantiate__ordering(self, store_admin: StoreAdmin) -> None:
    assert store_admin.ordering == ('franchise__name', 'franchise_location')
