"""PackagingUnit model."""

from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from utilities.models.bases.base_model import BaseModel
from utilities.models.fields.blonde import BlondeCharField

CONSTRAINT_NAMES = {'name': 'PackagingUnit name must be unique'}


class PackagingUnit(
    BaseModel,
):

  class Meta:
    constraints = [
        UniqueConstraint(
            Lower('name'),
            name=CONSTRAINT_NAMES['name'],
        ),
    ]

  name = BlondeCharField(
      max_length=80,
      blank=False,
  )

  def __str__(self) -> str:
    return str(self.name)
