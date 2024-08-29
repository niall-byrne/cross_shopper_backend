"""Scraper model."""

from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from utilities.models.bases.model_base import ModelBase
from utilities.models.fields.title import TitleField
from utilities.models.validators.regex import validator_regex

CONSTRAINT_NAMES = {'name': 'Scraper name must be unique'}


class Scraper(
    ModelBase,
):
  """Scraper model."""

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
  pricing_selector = models.CharField(
      max_length=250,
      blank=False,
  )
  pricing_regex = models.CharField(
      max_length=250,
      blank=False,
      validators=[validator_regex],
  )
  pricing_bulk_selector = models.CharField(
      max_length=250,
      blank=False,
  )
  pricing_bulk_regex = models.CharField(
      max_length=250,
      blank=False,
      validators=[validator_regex],
  )
  url_validation_regex = models.CharField(
      max_length=250,
      blank=False,
      validators=[validator_regex],
  )

  def __str__(self) -> str:
    return str(self.name)
