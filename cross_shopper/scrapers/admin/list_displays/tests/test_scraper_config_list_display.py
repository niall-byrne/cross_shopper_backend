"""Test the ScaperConfig admin model list display."""

from scrapers.admin.list_displays.scraper_config import (
    scraper_config_list_display,
)
from utilities.admin.list_displays.columns import (
    ColumnLinkConfig,
    ColumnObjectConfig,
)
from utilities.testing.comparisons.instance import InstanceOfClass


class TestScraperConfigAdminListDisplay:

  def test_list_display(self) -> None:
    assert scraper_config_list_display == (
        InstanceOfClass(
            base=ColumnObjectConfig,
            attributes={
                "method_name": "scraper_config__url",
                "description": "Scraper Config",
                "obj_lookup": "url",
            },
        ),
        InstanceOfClass(
            base=ColumnLinkConfig,
            attributes={
                "method_name": "scraper_config__scraper__name",
                "description": "Scraper",
                "reverse_url_name": "admin:scrapers_scraper_change",
                "obj_id_lookup": "scraper.pk",
                "obj_name_lookup": "scraper.name",
            },
        ),
        InstanceOfClass(
            base=ColumnObjectConfig,
            attributes={
                "method_name": "scraper_config__has_item",
                "description": "Has Item",
                "obj_lookup": "has_item",
                "is_boolean": True,
                "obj_order": None,
            },
        ),
        InstanceOfClass(
            base=ColumnLinkConfig,
            attributes={
                "method_name": "scraper_config__associated_item",
                "description": "Associated Item",
                "reverse_url_name": "admin:items_item_change",
                "obj_id_lookup": "associated_item.pk",
                "obj_name_lookup": "associated_item",
                "obj_order": None,
            },
        ),
    )
