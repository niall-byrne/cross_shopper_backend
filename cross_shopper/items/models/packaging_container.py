"""PackagingContainer model."""

from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from utilities.models.bases.model_base import ModelBase
from utilities.models.fields.title import TitleField

CONSTRAINT_NAMES = {'name': 'PackagingContainer name must be unique'}


class PackagingContainer(
    ModelBase,
):

  class Meta:

    constraints = [
        UniqueConstraint(
            Lower('name'),
            name=CONSTRAINT_NAMES['name'],
        ),
    ]

  name = TitleField(
      max_length=80,
      blank=False,
  )

  def __str__(self) -> str:
    return str(self.name)
