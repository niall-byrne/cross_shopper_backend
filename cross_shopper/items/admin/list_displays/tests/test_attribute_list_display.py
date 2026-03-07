"""Test the Attribute admin model list display."""

from items.admin.list_displays.attribute import (
    attribute_list_display,
)
from utilities.admin.list_displays.columns import (
    ColumnObjectConfig,
)
from utilities.testing.comparisons.instance import InstanceOfClass


class TestAttributeAdminListDisplay:

  def test_list_display(self) -> None:
    assert attribute_list_display == (
        "name",
        InstanceOfClass(
            base=ColumnObjectConfig,
            attributes={
                "method_name": "attribute__has_item",
                "description": "In Use",
                "obj_lookup": "has_item",
                "is_boolean": True,
                "obj_order": None,
            }
        ),
    )
