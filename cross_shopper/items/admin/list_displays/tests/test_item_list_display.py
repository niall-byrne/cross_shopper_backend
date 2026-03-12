"""Test the Item admin model list display."""

from items.admin.list_displays.item import (
    item_list_display,
)
from utilities.admin.list_displays.columns import (
    ColumnLinkConfig,
    ColumnObjectConfig,
)
from utilities.testing.comparisons.instance import InstanceOfClass


class TestItemAdminListDisplay:

  def test_list_display(self) -> None:
    assert item_list_display == (
        InstanceOfClass(
            base=ColumnLinkConfig,
            attributes={
                "method_name": "item__name_full",
                "description": "Name",
                "reverse_url_name": "admin:items_item_change",
                "obj_id_lookup": "pk",
                "obj_name_lookup": "name_full",
                "obj_order": "name",
            }
        ),
        InstanceOfClass(
            base=ColumnLinkConfig,
            attributes={
                "method_name": "item__brand",
                "description": "Brand",
                "reverse_url_name": "admin:items_brand_change",
                "obj_id_lookup": "brand.pk",
                "obj_name_lookup": "brand",
                "obj_order": "brand.name",
            }
        ),
        InstanceOfClass(
            base=ColumnObjectConfig,
            attributes={
                "method_name": "item__is_non_gmo",
                "description": "Is Non-GMO",
                "obj_lookup": "is_non_gmo",
                "is_boolean": True,
                "obj_order": None,
            }
        ),
        InstanceOfClass(
            base=ColumnObjectConfig,
            attributes={
                "method_name": "item__is_organic",
                "description": "Is Organic",
                "obj_lookup": "is_organic",
                "is_boolean": True,
                "obj_order": None,
            }
        ),
        InstanceOfClass(
            base=ColumnLinkConfig,
            attributes={
                "method_name": "item__packaging",
                "description": "Packaging",
                "reverse_url_name": "admin:items_packaging_change",
                "obj_id_lookup": "packaging.pk",
                "obj_name_lookup": "packaging",
                "obj_order": "packaging.name",
            }
        ),
        InstanceOfClass(
            base=ColumnLinkConfig,
            attributes={
                "method_name": "item__price_group",
                "description": "Price Group",
                "reverse_url_name": "admin:items_pricegroup_change",
                "obj_id_lookup": "price_group.pk",
                "obj_name_lookup": "price_group",
                "obj_order": "price_group.name",
            }
        ),
    )
