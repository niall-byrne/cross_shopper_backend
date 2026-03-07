"""Attribute admin model list display."""

from utilities.admin.list_displays.columns import (
    ColumnObjectConfig,
)

attribute_list_display = (
    "name",
    ColumnObjectConfig(
        method_name="attribute__has_item",
        description="In Use",
        obj_lookup="has_item",
        is_boolean=True,
        obj_order=None,
    ),
)
