"""Admin for the item scraper config model."""

from typing import TYPE_CHECKING

from django.contrib import admin
from items.admin.list_filters.item_scraper_config import (
    item_scraper_config_list_filter,
)
from scrapers.admin.mixins.scraper_config_actions import (
    ScraperConfigActionsAdminMixin,
)

if TYPE_CHECKING:
  from items.models import ItemScraperConfig  # noqa: F401


class ItemScraperConfigAdmin(
    ScraperConfigActionsAdminMixin["ItemScraperConfig"],
    admin.ModelAdmin["ItemScraperConfig"],
):
  scraper_config_is_related_model = True

  actions = (
      "action_activate_scraper_configs",
      "action_deactivate_scraper_configs",
  )
  list_filter = item_scraper_config_list_filter
  ordering = (
      "item__name",
      "scraper_config__scraper__name",
      "scraper_config__url",
  )
  search_fields = (
      "scraper_config__scraper__name",
      "scraper_config__url",
      "item__name",
  )
