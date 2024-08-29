"""ItemScraperConfig model."""

from django.db import models
from utilities.models.bases.model_base import ModelBase


class ItemScraperConfig(
    ModelBase,
):
  item = models.ForeignKey(
      'items.Item',
      on_delete=models.CASCADE,
  )
  scraper_config = models.ForeignKey(
      'scrapers.ScraperConfig',
      on_delete=models.CASCADE,
  )

  def __str__(self) -> str:
    return f"{self.item.name} - {self.scraper_config}"
