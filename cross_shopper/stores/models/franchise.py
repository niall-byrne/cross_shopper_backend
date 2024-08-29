"""Franchise model."""

from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from utilities.models.bases.base_model import BaseModel
from utilities.models.fields.blonde import BlondeCharField

CONSTRAINT_NAMES = {'name': 'Franchise name must be unique'}


class Franchise(
    BaseModel,
):
  """Franchise model."""

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
  scraper = models.ForeignKey(
      'scrapers.Scraper',
      on_delete=models.PROTECT,
  )

  def __str__(self) -> str:
    return str(self.name)
