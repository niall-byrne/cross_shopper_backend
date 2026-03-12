"""PriceGroup model."""

from typing import TYPE_CHECKING, cast

from django.apps import apps
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.functions import Lower
from utilities.models.bases.model_base import ModelBase
from utilities.models.fields.blonde import BlondeCharField
from utilities.models.validators.greater_than_zero import (
    validator_greater_than_zero,
)

if TYPE_CHECKING:  # no cover
  from django.db.models import QuerySet
  from items.models import Item

CONSTRAINT_NAMES = {'name': 'PriceGroup name must be unique'}
VALIDATION_ERRORS = {
    'invalid_unit':
        {
            'unit':
                [
                    'The comparison unit must match the packaging unit of each '
                    'associated item.'
                ]
        }
}


class PriceGroup(
    ModelBase,
):

  class Meta:
    constraints = [
        models.UniqueConstraint(Lower('name'), name=CONSTRAINT_NAMES['name']),
    ]

  name = BlondeCharField(
      max_length=80,
      blank=False,
  )
  quantity = models.PositiveIntegerField(
      validators=[
          validator_greater_than_zero,
          MaxValueValidator(1000),
      ]
  )
  unit = models.ForeignKey(
      'items.PackagingUnit',
      on_delete=models.PROTECT,
  )

  def __str__(self) -> str:
    return str(self.name)

  def clean(self) -> None:
    """Pre-save verification."""
    if self.items.exclude(packaging__unit=self.unit).count() > 0:
      raise ValidationError(VALIDATION_ERRORS['invalid_unit'])

  @property
  def has_item(self) -> bool:
    """Return a boolean if an item is associated with this group."""
    return self.items.count() != 0

  @property
  def items(self) -> "QuerySet[Item]":
    """Return a the items associated with this instance."""
    ItemModel = cast(
        "Item",
        apps.get_model('items', 'Item'),
    )
    if self.pk:
      return ItemModel.objects.all().filter(price_group=self)
    return ItemModel.objects.none()
