"""ScraperConfig model list display."""

from utilities.admin.list_display.columns import (
    ColumnLinkConfig,
    ColumnObjectConfig,
)

scraper_config_list_display = (
    ColumnObjectConfig(
        method_name="scraper_config__url",
        description="Scraper Config",
        obj_lookup="url",
    ),
    ColumnLinkConfig(
        method_name="scraper_config__scraper__name",
        description="Scraper",
        reverse_url_name="admin:scrapers_scraper_change",
        obj_id_lookup="scraper.id",
        obj_name_lookup="scraper.name",
    ),
    ColumnObjectConfig(
        method_name="scraper_config__has_item",
        description="Has Item",
        obj_lookup="has_item",
        is_boolean=True,
        obj_order=None,
    ),
    ColumnLinkConfig(
        method_name="scraper_config__associated_item",
        description="Associated Item",
        reverse_url_name="admin:items_item_change",
        obj_id_lookup="associated_item.id",
        obj_name_lookup="associated_item",
        obj_order=None,
    )
)
