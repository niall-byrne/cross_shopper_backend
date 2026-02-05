"""ReportStore admin model list filter."""

from utilities.admin.list_filters import GenericListFilter

report_store_list_filter = (
    GenericListFilter.create(
        title='report',
        parameter_name='report__name',
    ),
    GenericListFilter.create(
        title='franchise',
        parameter_name='store__franchise__name',
    ),
    GenericListFilter.create(
        title='location',
        parameter_name='store__address__locality__name',
    ),
)
