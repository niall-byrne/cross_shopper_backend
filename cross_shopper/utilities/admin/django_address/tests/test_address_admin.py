"""Test the admin for the Address model."""

from django.contrib import admin
from utilities.admin.django_address.address import AddressAdmin


class TestAddressAdmin:
  """Test the AddressAdmin class."""

  def test_instantiate__inheritance(
      self,
      address_admin: AddressAdmin,
  ) -> None:
    assert isinstance(address_admin, admin.ModelAdmin)

  def test_instantiate__has_correct_list_filter(
      self,
      address_admin: AddressAdmin,
  ) -> None:
    assert address_admin.list_filter == (
        "locality__name",
        "locality__state",
        "locality__state__country",
    )

  def test_instantiate__has_correct_ordering(
      self,
      address_admin: AddressAdmin,
  ) -> None:
    assert address_admin.ordering == (
        "locality__state__country",
        "locality__state",
        "locality__name",
        "route",
        "street_number",
    )
