"""ItemScraperConfig model."""

from django.db import models
from utilities.models.bases.base_model import BaseModel


class ItemScraperConfig(
    BaseModel,
):
  item = models.ForeignKey(
      'items.Item',
      on_delete=models.PROTECT,
  )
  scraper_config = models.ForeignKey(
      'scrapers.ScraperConfig',
      on_delete=models.PROTECT,
  )

  def __str__(self) -> str:
    return f"{self.item.name} - {self.scraper_config}"
