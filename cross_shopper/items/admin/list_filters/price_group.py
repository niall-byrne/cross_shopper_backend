"""PriceGroup admin model list filter."""

from items.admin.list_filters.filters.price_group.in_use import (
    InUseFilter,
)
from utilities.admin.list_filters.generic_list_filter import GenericListFilter

price_group_list_filter = (
    InUseFilter,
    GenericListFilter.create(
        title='name',
        parameter_name='name',
    ),
    GenericListFilter.create(
        title='unit',
        parameter_name='unit__name',
    ),
    GenericListFilter.create(
        title='attribute',
        parameter_name='attribute__name',
    ),
)
