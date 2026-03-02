"""Serializer to retrieve, list, create or update Addresses."""

from typing import TYPE_CHECKING, Dict, Union

from address.models import Address, Country, Locality, State
from rest_framework import serializers
from utilities.models.serializers.fields.blonde import BlondeCharField
from .address_internal import AddressSerializerInternal

if TYPE_CHECKING:  # no cover
  from django.db import models


class AddressSerializerRW(serializers.ModelSerializer[Address]):
  """Serializer to retrieve, list, create or update Addresses."""

  street_number = serializers.IntegerField()
  street_name = BlondeCharField()
  city = BlondeCharField()
  state = BlondeCharField()
  postal_code = BlondeCharField()
  country = BlondeCharField()

  class Meta:
    model = Address
    fields = (
        "street_number",
        "street_name",
        "city",
        "state",
        "postal_code",
        "country",
    )
    read_only = fields

  def to_representation(self, instance: Address) -> Dict[str, str]:
    """Object instance -> Dict of primitive datatypes."""
    representation = AddressSerializerInternal(instance).data

    return {
        "street_number": representation["street_number"],
        "street_name": representation["route"],
        "city": representation["locality"]["name"],
        "state": representation["locality"]["state"]["name"],
        "postal_code": representation["locality"]["postal_code"],
        "country": representation["locality"]["state"]["country"]["name"],
    }

  def create(
      self,
      validated_data: Dict[str, Union[str, "models.Model"]],
  ) -> Address:
    """Create a new instance and all sub instances as needed."""
    country = Country.objects.get_or_create(name=validated_data["country"])[0]
    state = State.objects.get_or_create(
        name=validated_data["state"],
        country=country,
    )[0]
    locality = Locality.objects.get_or_create(
        name=validated_data["city"],
        postal_code=validated_data["postal_code"],
        state=state,
    )[0]
    address = {
        "street_number": validated_data["street_number"],
        "route": validated_data["street_name"],
        "locality": locality
    }
    return Address.objects.get_or_create(**address)[0]
