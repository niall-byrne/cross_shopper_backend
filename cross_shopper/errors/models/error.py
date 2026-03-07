"""Error model."""

from django.db import models
from utilities.models.bases.model_base import ModelBase


class Error(
    ModelBase,
):
  is_reoccurring = models.BooleanField(default=False)

  type = models.ForeignKey("errors.ErrorType", on_delete=models.CASCADE)
  item = models.ForeignKey("items.Item", on_delete=models.CASCADE)
  scraper_config = models.ForeignKey(
      "scrapers.ScraperConfig",
      on_delete=models.CASCADE,
  )
  store = models.ForeignKey("stores.Store", on_delete=models.CASCADE)
  count = models.PositiveIntegerField(default=1)

  class Meta:
    unique_together = ("type", "item", "scraper_config", "store")

  def __str__(self) -> str:
    return " ".join(
        [
            str(self.type) + ":",
            str(self.item.name_full),
            "-",
            str(self.store),
        ]
    )
