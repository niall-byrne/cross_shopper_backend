"""PriceGroupAttribute admin model list filter."""

from utilities.admin.list_filters import GenericListFilter

price_group_attribute_list_filter = (
    GenericListFilter.create(
        title="attribute",
        parameter_name="attribute__name",
    ),
    GenericListFilter.create(
        title="price group",
        parameter_name="price_group__name",
    ),
)
