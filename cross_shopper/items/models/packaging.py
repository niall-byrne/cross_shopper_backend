"""Packaging model."""

from django.core.exceptions import ValidationError
from django.db import models
from items import constants
from rest_framework import serializers
from utilities.models.bases.model_base import ModelBase
from utilities.models.validators.greater_than_zero import (
    validator_greater_than_zero,
)


class Packaging(
    ModelBase,
):

  class Meta:
    verbose_name_plural = "Packaging"
    unique_together = ("quantity", "container", "unit")

  quantity = models.DecimalField(
      blank=True,
      null=True,
      decimal_places=2,
      max_digits=11,
      validators=[
          validator_greater_than_zero,
      ],
  )
  container = models.ForeignKey(
      "items.PackagingContainer",
      on_delete=models.PROTECT,
      blank=True,
      null=True,
  )
  unit = models.ForeignKey(
      "items.PackagingUnit",
      on_delete=models.PROTECT,
  )

  def clean(self) -> None:
    """Pre-save verification."""
    if self.quantity is None and (self.container is not None):
      raise ValidationError(
          {
              "quantity":
                  [str(serializers.Field.default_error_messages["required"])],
          }
      )
    if self.container is None and (self.quantity is not None):
      raise ValidationError(
          {
              "container":
                  [str(serializers.Field.default_error_messages["required"])],
          }
      )

  def __str__(self) -> str:
    if self.quantity is None and self.container is None:
      return (
          f"{constants.PACKAGING_CONTAINER_NAME_FOR_BULK_PACKAGING} per "
          f"{str(self.unit)}"
      )
    return (
        f"{str(self.container)}: "
        f"{str(self.quantity).replace('.00', '')} "
        f"{str(self.unit)}"
    )
