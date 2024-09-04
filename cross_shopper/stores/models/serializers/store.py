"""Serializer for the Store model."""

from typing import Any, Dict

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator
from stores.models import Franchise, Store
from utilities.models.serializers.fields.blonde import BlondeCharField
from .address import AddressSerializer
from .franchise import FranchiseSerializer


class StoreSerializer(serializers.ModelSerializer):
  """Serializer for the Store model."""

  address = AddressSerializer()
  franchise = FranchiseSerializer()
  franchise_location = BlondeCharField(max_length=80, allow_blank=False)

  class Meta:
    model = Store
    fields = ('id', 'address', 'franchise', 'franchise_location')
    validators = [
        UniqueTogetherValidator(
            queryset=Store.objects.all(),
            fields=['franchise', 'franchise_location']
        )
    ]

  def create(self, validated_data) -> "Store":
    """Create a new instance."""
    franchise = validated_data.pop('franchise')
    address = AddressSerializer().create(validated_data.pop('address'))

    return Store.objects.create(
        **validated_data,
        address=address,
        franchise=franchise,
    )

  def validate_franchise(self, attrs: Dict[str, Any]) -> "Franchise":
    """Perform franchise field validation."""
    try:
      return Franchise.objects.get(**attrs)
    except ObjectDoesNotExist as exc:
      raise ValidationError(exc.args, code="does_not_exist")
