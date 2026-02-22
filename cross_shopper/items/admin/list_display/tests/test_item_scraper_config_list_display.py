"""Test the ItemScraperConfig admin model list display."""

from items.admin.list_display.item_scraper_config import (
    item_scraper_config_list_display,
)
from utilities.admin.list_display.columns import (
    ColumnLinkConfig,
    ColumnObjectConfig,
)
from utilities.testing.comparisons.instance import InstanceOfClass


class TestItemScraperConfigAdminListDisplay:

  def test_list_display(self) -> None:
    assert item_scraper_config_list_display == (
        InstanceOfClass(
            base=ColumnObjectConfig,
            attributes={
                "method_name": "item_scraper_config",
                "description": "Item Scraper Config",
                "obj_lookup": "",
                "obj_order": None,
            }
        ),
        InstanceOfClass(
            base=ColumnLinkConfig,
            attributes={
                "method_name": "item_scraper_config__item",
                "description": "Item",
                "reverse_url_name": "admin:items_item_change",
                "obj_id_lookup": "item.id",
                "obj_name_lookup": "item",
                "obj_order": "item.name",
            }
        ),
        InstanceOfClass(
            base=ColumnLinkConfig,
            attributes={
                "method_name": "item_scraper_config__scraper_config",
                "description": "Scraper Config",
                "reverse_url_name": "admin:scrapers_scraperconfig_change",
                "obj_id_lookup": "scraper_config.id",
                "obj_name_lookup": "scraper_config",
            }
        ),
        InstanceOfClass(
            base=ColumnObjectConfig,
            attributes={
                "method_name": "item_scraper_config__scraper_config__is_active",
                "description": "Is Active",
                "obj_lookup": "scraper_config.is_active",
                "is_boolean": True,
            }
        ),
    )
