"""Test the admin for the Store model."""

from typing import TYPE_CHECKING

from django.contrib import admin
from stores.admin.list_filters.store import store_list_filter

if TYPE_CHECKING:  # no cover
  from stores.admin.store import StoreAdmin


class TestStoreAdmin:

  def test_instantiate__inheritance(
      self,
      store_admin: "StoreAdmin",
  ) -> None:
    assert isinstance(store_admin, admin.ModelAdmin)

  def test_instantiate__has_correct_list_filter(
      self,
      store_admin: "StoreAdmin",
  ) -> None:
    assert store_admin.list_filter == store_list_filter

  def test_instantiate__has_correct_ordering(
      self,
      store_admin: "StoreAdmin",
  ) -> None:
    assert store_admin.ordering == ("franchise__name", "franchise_location")
