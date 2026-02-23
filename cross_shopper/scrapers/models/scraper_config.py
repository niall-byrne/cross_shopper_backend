"""ScraperConfig model."""

import re
from typing import Optional

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property
from items.models import Item, ItemScraperConfig
from utilities.models.bases.base_model import BaseModel


class ScraperConfig(
    BaseModel,
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
  is_active = models.BooleanField(default=True)

  objects = models.Manager()

  @property
  def has_item(self) -> bool:
    """Return a boolean if an item is associated with this instance."""
    return self.associated_item is not None

  @cached_property
  def associated_item(self) -> Optional[Item]:
    """Return any item associated with this instance."""
    return ItemScraperConfig.associations.get_item(self)

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
