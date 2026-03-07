"""ItemAttribute admin model list display."""

from utilities.admin.list_displays.columns import (
    ColumnLinkConfig,
    ColumnObjectConfig,
)

item_attribute_list_display = (
    ColumnObjectConfig(
        method_name="item_attribute",
        description="Item Attribute",
        obj_lookup="",
        obj_order=None,
    ),
    ColumnLinkConfig(
        method_name="item_attribute__item",
        description="Item",
        reverse_url_name="admin:items_item_change",
        obj_id_lookup="item.pk",
        obj_name_lookup="item",
        obj_order="item.name",
    ),
    ColumnLinkConfig(
        method_name="item_attribute__attribute",
        description="Attribute",
        reverse_url_name="admin:items_attribute_change",
        obj_id_lookup="attribute.pk",
        obj_name_lookup="attribute.name",
    ),
)
