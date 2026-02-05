"""Admin for the item scraper config model."""

from typing import TYPE_CHECKING

from django.contrib import admin
from items.admin.list_filters.item_scraper_config import (
    item_scraper_config_list_filter,
)

if TYPE_CHECKING:  # no cover
  from items.models import ItemScraperConfig  # noqa: F401


class ItemScraperConfigAdmin(
    admin.ModelAdmin["ItemScraperConfig"],
):
  list_filter = item_scraper_config_list_filter
  ordering = (
      "item__name",
      "scraper_config__scraper__name",
      "scraper_config__url",
  )
