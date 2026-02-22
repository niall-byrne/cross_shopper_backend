"""ScraperConfig admin model list display."""

from utilities.admin.list_displays.columns import (
    ColumnLinkConfig,
    ColumnObjectConfig,
)

item_scraper_config_list_display = (
    ColumnObjectConfig(
        method_name="item_scraper_config",
        description="Item Scraper Config",
        obj_lookup="",
        obj_order=None,
    ),
    ColumnLinkConfig(
        method_name="item_scraper_config__item",
        description="Item",
        reverse_url_name="admin:items_item_change",
        obj_id_lookup="item.pk",
        obj_name_lookup="item",
        obj_order="item.name",
    ),
    ColumnLinkConfig(
        method_name="item_scraper_config__scraper_config",
        description="Scraper Config",
        reverse_url_name="admin:scrapers_scraperconfig_change",
        obj_id_lookup="scraper_config.pk",
        obj_name_lookup="scraper_config",
    ),
    ColumnObjectConfig(
        method_name="item_scraper_config__scraper_config__is_active",
        description="Is Active",
        obj_lookup="scraper_config.is_active",
        is_boolean=True,
    ),
)
