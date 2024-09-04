"""Test the AddressSerializer class."""

from typing import TYPE_CHECKING

import pytest
from rest_framework.exceptions import ErrorDetail, ValidationError
from stores.models.serializers.address import AddressSerializer

if TYPE_CHECKING:  # no cover
  from address.models import Address


@pytest.mark.django_db
class TestAddressSerializer:

  def test_serialization__correct_representation(
      self,
      address: "Address",
  ) -> None:
    serialized = AddressSerializer(address)

    assert serialized.data == {
        "street_number": str(address.street_number),
        "street_name": address.route,
        "city": address.locality.name,
        "state": address.locality.state.name,
        "postal_code": address.locality.postal_code,
        "country": address.locality.state.country.name,
    }

  def test_deserialization__valid_input__no_existing_components__correct_model(
      self,
  ) -> None:
    address_data = {
        "street_number": 1,
        "street_name": "mocked street",
        "city": "mocked city",
        "state": "mocked state",
        "postal_code": "mocked postal_code",
        "country": "mocked country",
    }

    serialized = AddressSerializer(data=address_data)
    serialized.is_valid(raise_exception=True)
    instance = serialized.save()

    assert instance.street_number == address_data["street_number"]
    assert instance.route == address_data["street_name"]
    assert instance.locality.name == address_data["city"]
    assert instance.locality.state.name == address_data["state"]
    assert instance.locality.postal_code == address_data["postal_code"]
    assert instance.locality.state.country.name == address_data["country"]

  def test_deserialization__valid_input__existing_components__correct_model(
      self,
      address: "Address",
  ) -> None:
    address_data = {
        "street_number": 1,
        "street_name": "mocked street",
        "city": address.locality.name,
        "state": address.locality.state.name,
        "postal_code": "mocked postal_code",
        "country": address.locality.state.country.name,
    }

    serialized = AddressSerializer(data=address_data)
    serialized.is_valid(raise_exception=True)
    instance = serialized.save()

    assert instance.street_number == address_data["street_number"]
    assert instance.route == address_data["street_name"]
    assert instance.locality.name == address_data["city"]
    assert instance.locality.state == address.locality.state
    assert instance.locality.postal_code == address_data["postal_code"]
    assert instance.locality.state.country == address.locality.state.country

  def test_deserialization__invalid_input__raises_exception(self) -> None:
    address_data = {
        "street_number": "1",
        "street_name": "mocked street",
        "city": "mocked locality",
        "state": "mocked state",
        "postal_code": "mocked postal code",
    }

    with pytest.raises(ValidationError) as exc:
      serialized = AddressSerializer(data=address_data)
      serialized.is_valid(raise_exception=True)

    assert str(exc.value) == str(
        {
            "country":
                [
                    ErrorDetail(
                        string="This field is required.", code="required"
                    )
                ]
        }
    )
