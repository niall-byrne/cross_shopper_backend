"""Admin for the item scraper config model."""

from django.contrib import admin
from items.models import ItemScraperConfig
from scrapers.admin.mixins.scraper_config_actions import (
    ScraperConfigActionsAdminMixin,
)
from scrapers.models import ScraperConfig
from utilities.admin.list_display_column import (
    ColumnLinkConfig,
    ColumnObjectConfig,
    column_generator,
)


class ScraperConfigAdminActions(ScraperConfigActionsAdminMixin[ScraperConfig]):
  scraper_config_is_related_model = True


class ItemScraperConfigAdmin(
    ScraperConfigAdminActions,
    admin.ModelAdmin[ItemScraperConfig],
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
  list_display = (
      "item_scraper_config",
      "item_scraper_config__scraper_config__is_active",
      "item_scraper_config__scraper_config",
  )


column_generator(ItemScraperConfigAdmin)(
    config=[
        ColumnObjectConfig(
            method_name="item_scraper_config",
            description="Item Scraper Config",
            obj_lookup="item.name",
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
