"""Test the admin for the Brand model."""

from typing import TYPE_CHECKING

from django.contrib import admin

if TYPE_CHECKING:  # no cover
  from items.admin.brand import BrandAdmin


class TestBrandAdmin:

  def test_instantiate__inheritance(
      self,
      brand_admin: "BrandAdmin",
  ) -> None:
    assert isinstance(brand_admin, admin.ModelAdmin)

  def test_instantiate__has_correct_ordering(
      self,
      brand_admin: "BrandAdmin",
  ) -> None:
    assert brand_admin.ordering == ("name",)
