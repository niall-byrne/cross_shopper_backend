"""Price admin model list display."""

from utilities.admin.list_displays.columns import (
    ColumnLinkConfig,
    ColumnObjectConfig,
)

price_list_display = (
    ColumnObjectConfig(
        method_name="price__amount",
        description="Price",
        obj_lookup="amount",
    ),
    ColumnLinkConfig(
        method_name="price__item",
        description="Item",
        reverse_url_name="admin:items_item_change",
        obj_id_lookup="item.pk",
        obj_name_lookup="item.name_full",
        obj_order="item.name",
    ),
    ColumnLinkConfig(
        method_name="price__franchise",
        description="Franchise",
        reverse_url_name="admin:stores_franchise_change",
        obj_id_lookup="store.franchise.pk",
        obj_name_lookup="store.franchise.name",
        obj_order="store.franchise.name",
    ),
    ColumnLinkConfig(
        method_name="price__store",
        description="Store",
        reverse_url_name="admin:stores_store_change",
        obj_id_lookup="store.pk",
        obj_name_lookup="store.address",
    ),
)
