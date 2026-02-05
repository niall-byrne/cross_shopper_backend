"""Store admin model list filter."""

from utilities.admin.list_filters import GenericListFilter

store_list_filter = (
    GenericListFilter.create(
        title='franchise',
        parameter_name='franchise__name',
    ),
    GenericListFilter.create(
        title='location',
        parameter_name='address__locality__name',
    )
)
