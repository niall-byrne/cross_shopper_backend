"""Test the ItemAttribute admin model list display."""

from items.admin.list_displays.item_attribute import (
    item_attribute_list_display,
)
from utilities.admin.list_displays.columns import (
    ColumnLinkConfig,
    ColumnObjectConfig,
)
from utilities.testing.comparisons.instance import InstanceOfClass


class TestItemAttributeAdminListDisplay:

  def test_list_display(self) -> None:
    assert item_attribute_list_display == (
        InstanceOfClass(
            base=ColumnObjectConfig,
            attributes={
                "method_name": "item_attribute",
                "description": "Item Attribute",
                "obj_lookup": "",
                "obj_order": None,
            },
        ),
        InstanceOfClass(
            base=ColumnLinkConfig,
            attributes={
                "method_name": "item_attribute__item",
                "description": "Item",
                "reverse_url_name": "admin:items_item_change",
                "obj_id_lookup": "item.pk",
                "obj_name_lookup": "item",
                "obj_order": "item.name",
            },
        ),
        InstanceOfClass(
            base=ColumnLinkConfig,
            attributes={
                "method_name": "item_attribute__attribute",
                "description": "Attribute",
                "reverse_url_name": "admin:items_attribute_change",
                "obj_id_lookup": "attribute.pk",
                "obj_name_lookup": "attribute.name",
            },
        ),
    )
