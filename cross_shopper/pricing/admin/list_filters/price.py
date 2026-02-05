"""Price admin model list filter."""

from utilities.admin.list_filters import GenericListFilter

price_list_filter = (
    GenericListFilter.create(
        title='item',
        parameter_name='item__name',
    ),
    GenericListFilter.create(
        title='brand',
        parameter_name='item__brand__name',
    ),
    GenericListFilter.create(
        title='franchise',
        parameter_name='store__franchise__name',
    ),
    GenericListFilter.create(
        title='location',
        parameter_name='store__address__locality__name',
    ),
    GenericListFilter.create(
        title='year',
        parameter_name='year',
        is_reversed=True,
    ),
    'week',
)
