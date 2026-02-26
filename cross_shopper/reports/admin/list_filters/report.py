"""Report admin model list filter."""

from utilities.admin.list_filters import GenericListFilter

report_list_filter = (
    'is_testing',
    GenericListFilter.create(
        title='has franchise',
        parameter_name='store__franchise__name',
    ),
    GenericListFilter.create(
        title='has store in',
        parameter_name='store__address__locality__name',
    )
)
