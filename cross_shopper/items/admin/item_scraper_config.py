"""Admin for the item scraper config model."""

from typing import TYPE_CHECKING

from django.contrib import admin
from items.admin.list_filter.item_scraper_config import item_scraper_config_list_filter
from scrapers.admin.mixins.scraper_config_actions import (
    ScraperConfigActionsAdminMixin,
)
from utilities.admin.list_display.column_generator import (
    ColumnLinkConfig,
    ColumnObjectConfig,
    list_display_column_generator,
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
  list_display = (
      "item_scraper_config",
      "item_scraper_config__scraper_config__is_active",
      "item_scraper_config__item",
      "item_scraper_config__scraper_config",
  )
  list_filter = item_scraper_config_list_filter
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


list_display_column_generator(ItemScraperConfigAdmin)(
    config=[
        ColumnObjectConfig(
            method_name="item_scraper_config",
            description="Item Scraper Config",
            obj_lookup="",
        ),
        ColumnLinkConfig(
            method_name="item_scraper_config__item",
            description="Item",
            reverse_url_name="admin:items_item_change",
            obj_id_lookup="item.id",
            obj_name_lookup="item",
        ),
        ColumnLinkConfig(
            method_name="item_scraper_config__scraper_config",
            description="Scraper Config",
            reverse_url_name="admin:scrapers_scraperconfig_change",
            obj_id_lookup="scraper_config.id",
            obj_name_lookup="scraper_config",
        ),
        ColumnObjectConfig(
            method_name="item_scraper_config__scraper_config__is_active",
            description="Is Active",
            obj_lookup="scraper_config.is_active",
            is_boolean=True,
        ),
    ]
)
