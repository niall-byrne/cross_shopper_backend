"""Test the admin for the Locality model."""

from typing import TYPE_CHECKING

from django.contrib import admin

if TYPE_CHECKING:  # no cover
  from utilities.admin.django_address.locality import LocalityAdmin


class TestLocalityAdmin:

  def test_instantiate__inheritance(
      self,
      locality_admin: "LocalityAdmin",
  ) -> None:
    assert isinstance(locality_admin, admin.ModelAdmin)

  def test_instantiate__has_correct_list_filter(
      self,
      locality_admin: "LocalityAdmin",
  ) -> None:
    assert locality_admin.list_filter == (
        "state__name",
        "state__country",
    )

  def test_instantiate__has_correct_ordering(
      self,
      locality_admin: "LocalityAdmin",
  ) -> None:
    assert locality_admin.ordering == (
        "state__country",
        "state__name",
    )
