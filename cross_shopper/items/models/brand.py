"""Brand model."""

from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from utilities.models.bases.model_base import ModelBase
from utilities.models.fields.blonde import BlondeCharField

CONSTRAINT_NAMES = {'name': 'Brand name must be unique'}


class Brand(
    ModelBase,
):

  class Meta:
    constraints = [
        UniqueConstraint(Lower('name'), name=CONSTRAINT_NAMES['name']),
    ]

  name = BlondeCharField(
      max_length=80,
      blank=False,
  )

  def __str__(self) -> str:
    return str(self.name)
