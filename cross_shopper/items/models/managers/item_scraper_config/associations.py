"""A model manager for scraper configs assocations with items."""

from typing import TYPE_CHECKING, Optional

from django.db import models
from items.models import Item

if TYPE_CHECKING:  # no cover
  from items.models import ItemScraperConfig  # noqa: F401
  from scrapers.models import ScraperConfig


class Associations(models.Manager["ItemScraperConfig"]):
  """A model manager for scraper configs assocations with items."""

  def get_item(
      self,
      scraper_config: "ScraperConfig",
  ) -> Optional["Item"]:
    """Return Item instances associated with the given instance."""
    obj = self.get_queryset().filter(scraper_config=scraper_config).first()
    if obj:
      return obj.item
    return None

  def get_items(
      self,
      scraper_configs: models.QuerySet["ScraperConfig"],
  ) -> models.QuerySet["Item"]:
    """Return Item instances associated with the current queryset."""
    scraper_configs_ids = scraper_configs.values_list("id", flat=True)
    item_ids = self.get_queryset().filter(
        scraper_config__id__in=scraper_configs_ids
    ).values_list("item__id", flat=True)
    return Item.objects.filter(id__in=item_ids)

  def with_items(
      self,
      scraper_configs: models.QuerySet["ScraperConfig"],
  ) -> models.QuerySet["ScraperConfig"]:
    """Filter ScraperConfig instances to those associated with items."""
    item_scraper_config_ids = self.get_queryset().values_list(
        "scraper_config__id",
        flat=True,
    )
    return scraper_configs.filter(id__in=item_scraper_config_ids)

  def with_no_items(
      self,
      scraper_configs: models.QuerySet["ScraperConfig"],
  ) -> models.QuerySet["ScraperConfig"]:
    """Filter ScraperConfig instances to those associated with no items."""
    item_scraper_config_ids = self.get_queryset().values_list(
        "scraper_config__id",
        flat=True,
    )
    return scraper_configs.exclude(id__in=item_scraper_config_ids)
