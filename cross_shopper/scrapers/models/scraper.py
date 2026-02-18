"""Scraper model."""

from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from utilities.models.bases.model_base import ModelBase
from utilities.models.fields.title import TitleField
from utilities.models.validators.regex_with_n_capture_groups import (
    create_validator_regex_with_n_capture_groups,
)

CONSTRAINT_NAMES = {"name": "Scraper name must be unique"}


class Scraper(
    ModelBase,
):
  """Scraper model."""

  class Meta:
    constraints = [
        UniqueConstraint(
            Lower("name"),
            name=CONSTRAINT_NAMES["name"],
        ),
    ]

  name = TitleField(
      max_length=80,
      blank=False,
  )
  url_validation_regex = models.CharField(
      max_length=250,
      blank=False,
      validators=[create_validator_regex_with_n_capture_groups(2)],
  )

  def __str__(self) -> str:
    return str(self.name)
