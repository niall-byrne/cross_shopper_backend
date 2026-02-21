"""Admin for the item scraper config model."""

from typing import TYPE_CHECKING

from django.contrib import admin
from items.admin.filters.item_scraper_config import item_scraper_config_filter
from scrapers.admin.mixins.scraper_config_actions import (
    ScraperConfigActionsAdminMixin,
)

if TYPE_CHECKING:  # no cover
  from items.models import ItemScraperConfig  # noqa: F401


class ItemScraperConfigAdmin(
    ScraperConfigActionsAdminMixin["ItemScraperConfig"],
    admin.ModelAdmin["ItemScraperConfig"],
):
  scraper_config_is_related_model = True

  actions = (
      "activate_scraper_configs",
      "deactivate_scraper_configs",
  )
  list_filter = item_scraper_config_filter
  ordering = (
      'item__name',
      'scraper_config__scraper__name',
      'scraper_config__url',
  )
  search_fields = (
      'scraper_config__scraper__name',
      'scraper_config__url',
      'item__name',
  )
