"""ItemScraperConfig model."""

from django.db import models
from django.db.models import UniqueConstraint
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

  class Meta:
    unique_together = ('item', 'scraper_config')
    constraints = [
        UniqueConstraint(
            fields=['scraper_config'],
            name='unique_scraper_config',
        )
    ]

  def __str__(self) -> str:
    return f"{self.item.name} - {self.scraper_config}"
