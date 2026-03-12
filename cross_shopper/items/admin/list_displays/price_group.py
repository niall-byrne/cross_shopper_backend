"""PriceGroup admin model list display."""

from utilities.admin.list_displays.columns import (
    ColumnLinkConfig,
    ColumnObjectConfig,
)

price_group_list_display = (
    "name",
    "quantity",
    ColumnLinkConfig(
        method_name="group__unit",
        description="Comparison Unit",
        reverse_url_name="admin:items_packagingunit_change",
        obj_id_lookup="unit.pk",
        obj_name_lookup="unit.name",
        obj_order="unit.name",
    ),
    ColumnObjectConfig(
        method_name="group__has_items",
        description="In Use",
        obj_lookup="has_item",
        is_boolean=True,
        obj_order=None,
    ),
)
