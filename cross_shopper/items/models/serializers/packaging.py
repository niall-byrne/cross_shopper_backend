"""Serializers for the Packaging model."""

from decimal import Decimal
from typing import Any

from items.models import Packaging, PackagingContainer, PackagingUnit
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from utilities.models.serializers.fields.blonde import BlondeCharField
from utilities.models.serializers.fields.title import TitleField
from .packaging_container import PackagingContainerSerializer
from .packaging_unit import PackagingUnitSerializer


class PackagingSerializerInternal(serializers.ModelSerializer[Packaging]):

  container = PackagingContainerSerializer()
  unit = PackagingUnitSerializer()

  class Meta:
    model = Packaging
    fields = ("quantity", "unit", "container")


class PackagingSerializer(serializers.ModelSerializer[Packaging]):
  ERROR_MESSAGE_QUANTITY_IS_NULL = (
      "This field cannot be null if a container is specified."
  )
  ERROR_MESSAGE_CONTAINER_IS_NULL = (
      "This field cannot be null if a quantity is specified."
  )

  quantity = serializers.DecimalField(
      min_value=Decimal(1),
      allow_null=True,
      max_digits=11,
      decimal_places=2,
  )
  unit = BlondeCharField(max_length=80, allow_blank=False)
  container = TitleField(max_length=80, allow_blank=False, allow_null=True)

  class Meta:
    model = Packaging
    fields = ("quantity", "unit", "container")
    read_only = fields

  def to_representation(self, instance: Packaging) -> dict[str, str]:
    """Object instance -> Dict of primitive datatypes."""
    representation = PackagingSerializerInternal(instance).data

    representation["unit"] = representation["unit"]["name"]

    if representation["container"] is not None:
      representation["container"] = representation["container"]["name"]

    return representation

  def create(
      self,
      validated_data: dict[str, Any],
  ) -> Packaging:
    """Create a new instance."""
    container = PackagingContainer.objects.get_or_create(
        name=validated_data.pop("container"),
    )[0]

    unit = PackagingUnit.objects.get_or_create(
        name=validated_data.pop("unit"),
    )[0]

    return Packaging.objects.get_or_create(
        **validated_data,
        container=container,
        unit=unit,
    )[0]

  def validate_quantity(self, value: int | None) -> int | None:
    """Perform quantity field validation."""
    if value is None and self.initial_data["container"] is not None:
      raise ValidationError(self.ERROR_MESSAGE_QUANTITY_IS_NULL)
    return value

  def validate_container(self, value: str | None) -> str | None:
    """Perform container field validation."""
    if value is None and self.initial_data["quantity"] is not None:
      raise ValidationError(self.ERROR_MESSAGE_CONTAINER_IS_NULL)
    return value
