"""Test the PriceGroupAttribute admin model list display."""

from items.admin.list_displays.price_group_attribute import (
    price_group_attribute_list_display,
)
from utilities.admin.list_displays.columns import (
    ColumnLinkConfig,
    ColumnObjectConfig,
)
from utilities.testing.comparisons.instance import InstanceOfClass


class TestPriceGroupAttributeListDisplay:

  def test_list_display(self) -> None:
    assert price_group_attribute_list_display == (
        InstanceOfClass(
            base=ColumnObjectConfig,
            attributes={
                "method_name": "price_group_attribute",
                "description": "Price Group Attribute",
                "obj_lookup": "",
                "obj_order": None,
            },
        ),
        InstanceOfClass(
            base=ColumnLinkConfig,
            attributes={
                "method_name": "price_group_attribute__item",
                "description": "Price Group",
                "reverse_url_name": "admin:items_pricegroup_change",
                "obj_id_lookup": "price_group.pk",
                "obj_name_lookup": "price_group",
                "obj_order": "price_group.name",
            },
        ),
        InstanceOfClass(
            base=ColumnLinkConfig,
            attributes={
                "method_name": "price_group_attribute__attribute",
                "description": "Attribute",
                "reverse_url_name": "admin:items_attribute_change",
                "obj_id_lookup": "attribute.pk",
                "obj_name_lookup": "attribute.name",
            },
        ),
    )
