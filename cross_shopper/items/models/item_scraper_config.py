"""ItemScraperConfig model."""

from django.db import models
from utilities.models.bases.model_base import ModelBase


class ItemScraperConfig(
    ModelBase,
):
  item = models.ForeignKey(
      'items.Item',
      on_delete=models.PROTECT,
  )
  scraper_config = models.ForeignKey(
      'scrapers.ScraperConfig',
      on_delete=models.PROTECT,
  )

  class Meta:
    unique_together = ('item', 'scraper_config')
    constraints = [
        models.UniqueConstraint(
            fields=['scraper_config'],
            name='unique_scraper_config',
        )
    ]

  def __str__(self) -> str:
    return f"{self.item.name} - {self.scraper_config}"
