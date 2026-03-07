"""Test the Price admin model list display."""

from pricing.admin.list_displays.price import (
    price_list_display,
)
from utilities.admin.list_displays.columns import (
    ColumnLinkConfig,
    ColumnObjectConfig,
)
from utilities.testing.comparisons.instance import InstanceOfClass


class TestPriceAdminListDisplay:

  def test_list_display(self) -> None:
    assert price_list_display == (
        InstanceOfClass(
            base=ColumnObjectConfig,
            attributes={
                "method_name": "price__amount",
                "description": "Price",
                "obj_lookup": "amount",
            },
        ),
        InstanceOfClass(
            base=ColumnLinkConfig,
            attributes={
                "method_name": "price__item",
                "description": "Item",
                "reverse_url_name": "admin:items_item_change",
                "obj_id_lookup": "item.pk",
                "obj_name_lookup": "item.name_full",
                "obj_order": "item.name",
            },
        ),
        InstanceOfClass(
            base=ColumnLinkConfig,
            attributes={
                "method_name": "price__franchise",
                "description": "Franchise",
                "reverse_url_name": "admin:stores_franchise_change",
                "obj_id_lookup": "store.franchise.pk",
                "obj_name_lookup": "store.franchise.name",
                "obj_order": "store.franchise.name",
            },
        ),
        InstanceOfClass(
            base=ColumnLinkConfig,
            attributes={
                "method_name": "price__store",
                "description": "Store",
                "reverse_url_name": "admin:stores_store_change",
                "obj_id_lookup": "store.pk",
                "obj_name_lookup": "store.address",
            },
        ),
    )
