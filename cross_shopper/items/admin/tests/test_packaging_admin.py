"""Test the admin for the Packaging model."""
from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import admin
from items.admin.list_filters.packaging import packaging_list_filter

if TYPE_CHECKING:
  from items.admin.packaging import PackagingAdmin


class TestPackagingAdmin:

  def test_instantiate__inheritance(
      self,
      packaging_admin: PackagingAdmin,
  ) -> None:
    assert isinstance(packaging_admin, admin.ModelAdmin)

  def test_instantiate__has_correct_list_filter(
      self,
      packaging_admin: PackagingAdmin,
  ) -> None:
    assert packaging_admin.list_filter == packaging_list_filter

  def test_instantiate__has_correct_ordering(
      self,
      packaging_admin: PackagingAdmin,
  ) -> None:
    assert packaging_admin.ordering == ("container__name", "unit__name")
