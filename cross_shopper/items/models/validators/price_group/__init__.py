"""PriceGroup model validators."""

from items.models.validators.price_group.member import (
    PriceGroupMemberValidator,
)

model_level_validators = (
    PriceGroupMemberValidator(
        model_fields=("is_organic",),
        related_field="is_organic",
        item_attribute="organic certification",
        price_group_attribute="organic certification",
    ),
    PriceGroupMemberValidator(
        model_fields=("is_non_gmo",),
        related_field="is_non_gmo",
        item_attribute="non-gmo certification",
        price_group_attribute="non-gmo certification",
    ),
    PriceGroupMemberValidator(
        model_fields=("unit",),
        related_field="packaging__unit",
        item_attribute="packaging unit",
        price_group_attribute="comparison unit",
    ),
)
