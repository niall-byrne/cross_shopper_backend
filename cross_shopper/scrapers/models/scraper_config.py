"""ScraperConfig model."""

import re

from django.core.exceptions import ValidationError
from django.db import models
from utilities.models.bases.model_base import ModelBase


class ScraperConfig(
    ModelBase,
):
  """ScraperConfig model."""

  scraper = models.ForeignKey(
      "scrapers.Scraper",
      on_delete=models.PROTECT,
  )
  url = models.CharField(
      max_length=250,
      blank=False,
  )

  def clean(self) -> None:
    """Pre-save verification."""
    match = re.match(self.scraper.url_validation_regex, self.url, re.DOTALL)
    if not match:
      raise ValidationError(
          {
              'url': [
                  f'Invalid url for the {str(self.scraper.name)} scraper.',
              ],
          }
      )
    self.url = match.group(2)

  def __str__(self) -> str:
    return f'{self.scraper.name}: {self.url}'
