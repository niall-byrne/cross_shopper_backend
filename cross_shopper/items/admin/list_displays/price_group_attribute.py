"""PriceGroupAttribute admin model list display."""

from utilities.admin.list_displays.columns import (
    ColumnLinkConfig,
    ColumnObjectConfig,
)

price_group_attribute_list_display = (
    ColumnObjectConfig(
        method_name="price_group_attribute",
        description="Price Group Attribute",
        obj_lookup="",
        obj_order=None,
    ),
    ColumnLinkConfig(
        method_name="price_group_attribute__item",
        description="Price Group",
        reverse_url_name="admin:items_pricegroup_change",
        obj_id_lookup="price_group.pk",
        obj_name_lookup="price_group",
        obj_order="price_group.name",
    ),
    ColumnLinkConfig(
        method_name="price_group_attribute__attribute",
        description="Attribute",
        reverse_url_name="admin:items_attribute_change",
        obj_id_lookup="attribute.pk",
        obj_name_lookup="attribute.name",
    ),
)
