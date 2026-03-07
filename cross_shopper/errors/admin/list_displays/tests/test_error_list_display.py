"""Test the Error admin model list display."""

from errors.admin.list_displays.error import error_list_display
from utilities.admin.list_displays.columns import (
    ColumnLinkConfig,
    ColumnObjectConfig,
)
from utilities.testing.comparisons.instance import InstanceOfClass


class TestErrorAdminListDisplay:

  def test_list_display(self) -> None:
    assert error_list_display == (
        InstanceOfClass(
            base=ColumnObjectConfig,
            attributes={
                "method_name": "error",
                "description": "Error",
                "obj_lookup": "type.name",
            },
        ),
        "count",
        "is_reoccurring",
        InstanceOfClass(
            base=ColumnLinkConfig,
            attributes={
                "method_name": "error__store__franchise",
                "description": "Franchise",
                "reverse_url_name": "admin:stores_franchise_change",
                "obj_id_lookup": "store.franchise.pk",
                "obj_name_lookup": "store.franchise.name",
            },
        ),
        InstanceOfClass(
            base=ColumnLinkConfig,
            attributes={
                "method_name": "error__item",
                "description": "Item",
                "reverse_url_name": "admin:items_item_change",
                "obj_id_lookup": "item.pk",
                "obj_name_lookup": "item.name_full",
                "obj_order": "item.name",
            },
        ),
        InstanceOfClass(
            base=ColumnLinkConfig,
            attributes={
                "method_name": "error__scraper_config__url",
                "description": "Scraper",
                "reverse_url_name": "admin:scrapers_scraperconfig_change",
                "obj_id_lookup": "scraper_config.pk",
                "obj_name_lookup": "scraper_config.url",
            },
        ),
        InstanceOfClass(
            base=ColumnObjectConfig,
            attributes={
                "method_name": "error__scraper_config__is_active",
                "description": "Is Active",
                "obj_lookup": "scraper_config.is_active",
                "is_boolean": True,
            },
        ),
        InstanceOfClass(
            base=ColumnLinkConfig,
            attributes={
                "method_name": "error__store",
                "description": "Store",
                "reverse_url_name": "admin:stores_store_change",
                "obj_id_lookup": "store.pk",
                "obj_name_lookup": "store.address",
            },
        ),
    )
