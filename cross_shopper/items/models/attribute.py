"""Attribute model."""

from typing import TYPE_CHECKING, cast

from django.apps import apps
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from utilities.models.bases.model_base import ModelBase
from utilities.models.fields.blonde import BlondeCharField
from utilities.models.validators.restricted_values import (
    create_restricted_values_validator,
)

if TYPE_CHECKING:  # no cover
  from items.models import ItemAttribute

CONSTRAINT_NAMES = {'name': 'Attribute name must be unique'}


class Attribute(
    ModelBase,
):

  class Meta:
    constraints = [
        UniqueConstraint(Lower('name'), name=CONSTRAINT_NAMES['name']),
    ]

  name = BlondeCharField(
      max_length=80,
      blank=False,
      validators=[create_restricted_values_validator(frozenset({','}))],
  )

  @property
  def has_item(self) -> bool:
    """Return a boolean if an item is associated with this instance."""
    ItemAttributeModel = cast(
        "ItemAttribute",
        apps.get_model('items', 'ItemAttribute'),
    )
    return ItemAttributeModel.associations.get_items([self]).count() != 0

  def __str__(self) -> str:
    return str(self.name)
