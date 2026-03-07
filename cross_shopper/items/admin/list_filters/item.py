"""Item model admin list filter."""

from utilities.admin.list_filters import GenericListFilter

item_list_filter = (
    GenericListFilter.create(
        title='brand',
        parameter_name='brand__name',
    ),
    'is_non_gmo',
    'is_organic',
    GenericListFilter.create(
        title='packaging',
        parameter_name='packaging__container__name',
    ),
    GenericListFilter.create(
        title='attribute',
        parameter_name='attribute__name',
    ),
    'name',
)
