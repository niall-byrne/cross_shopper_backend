"""Test the PriceGroup admin model list display."""

from items.admin.list_displays.price_group import (
    price_group_list_display,
)
from utilities.admin.list_displays.columns import (
    ColumnLinkConfig,
    ColumnObjectConfig,
)
from utilities.testing.comparisons.instance import InstanceOfClass


class TestGroupAdminListDisplay:

  def test_list_display(self) -> None:
    assert price_group_list_display == (
        "name",
        "quantity",
        InstanceOfClass(
            base=ColumnLinkConfig,
            attributes={
                "method_name": "group__unit",
                "description": "Comparison Unit",
                "reverse_url_name": "admin:items_packagingunit_change",
                "obj_id_lookup": "unit.pk",
                "obj_name_lookup": "unit.name",
                "obj_order": "unit.name",
            }
        ),
        InstanceOfClass(
            base=ColumnObjectConfig,
            attributes={
                "method_name": "group__has_items",
                "description": "In Use",
                "obj_lookup": "has_item",
                "is_boolean": True,
                "obj_order": None,
            }
        ),
    )
