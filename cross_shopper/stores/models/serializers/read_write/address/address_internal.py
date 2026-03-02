"""Serializer for internal representations of Address model instance."""

from address.models import Address
from rest_framework import serializers
from .locality import LocalitySerializer


class AddressSerializerInternal(serializers.ModelSerializer):
  locality = LocalitySerializer()

  class Meta:
    model = Address
    fields = ('street_number', 'route', 'locality')
    read_only = fields
