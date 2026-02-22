"""Error model list display."""

from utilities.admin.list_display.columns import (
    ColumnLinkConfig,
    ColumnObjectConfig,
)

error_list_display = (
    ColumnObjectConfig(
        method_name="error",
        description="Error",
        obj_lookup="type.name",
    ),
    "count",
    "is_reoccurring",
    ColumnLinkConfig(
        method_name="error__store__franchise",
        description="Franchise",
        reverse_url_name="admin:stores_franchise_change",
        obj_id_lookup="store.franchise.id",
        obj_name_lookup="store.franchise.name",
    ),
    ColumnLinkConfig(
        method_name="error__item",
        description="Item",
        reverse_url_name="admin:items_item_change",
        obj_id_lookup="item.id",
        obj_name_lookup="item.full_name",
        obj_order="item.name",
    ),
    ColumnLinkConfig(
        method_name="error__scraper_config__url",
        description="Scraper",
        reverse_url_name="admin:scrapers_scraperconfig_change",
        obj_id_lookup="scraper_config.id",
        obj_name_lookup="scraper_config.url",
    ),
    ColumnObjectConfig(
        method_name="error__scraper_config__is_active",
        description="Is Active",
        obj_lookup="scraper_config.is_active",
        is_boolean=True,
    ),
    ColumnLinkConfig(
        method_name="error__store",
        description="Store",
        reverse_url_name="admin:stores_store_change",
        obj_id_lookup="store.id",
        obj_name_lookup="store.address",
    ),
)
