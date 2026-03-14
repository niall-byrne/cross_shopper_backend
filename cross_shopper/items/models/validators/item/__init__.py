"""Item model validators."""

from items.models.validators.item.price_group_membership import (
    ItemPriceGroupMembershipValidator,
)

model_level_validators = (
    ItemPriceGroupMembershipValidator(
        comparison=("is_organic", "price_group.is_organic"),
        model_fields=["is_organic", "price_group"],
        item_attribute="organic certification",
        price_group_attribute="organic certification",
    ),
    ItemPriceGroupMembershipValidator(
        comparison=("is_non_gmo", "price_group.is_non_gmo"),
        model_fields=["is_non_gmo", "price_group"],
        item_attribute="non-gmo certification",
        price_group_attribute="non-gmo certification",
    ),
    ItemPriceGroupMembershipValidator(
        comparison=("packaging.unit.name", "price_group.unit.name"),
        model_fields=["packaging", "price_group"],
        item_attribute="packaging unit",
        price_group_attribute="comparison unit",
    ),
)
