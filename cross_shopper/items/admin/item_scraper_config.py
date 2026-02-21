"""Admin for the item scraper config model."""

from django.contrib import admin
from items.models import ItemScraperConfig
from scrapers.admin.mixins.scraper_config_actions import (
    ScraperConfigActionsAdminMixin,
)
from scrapers.models import ScraperConfig


class ScraperConfigAdminActions(ScraperConfigActionsAdminMixin[ScraperConfig]):
  scraper_config_is_related_model = True


class ItemScraperConfigAdmin(
    ScraperConfigAdminActions, admin.ModelAdmin[ItemScraperConfig]
):
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
  actions = (
      "activate_scraper_configs",
      "deactivate_scraper_configs",
  )
