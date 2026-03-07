"""ItemAttribute admin model list filter."""

from utilities.admin.list_filters import GenericListFilter

item_attribute_list_filter = (
    GenericListFilter.create(
        title='attribute',
        parameter_name='attribute__name',
    ),
    GenericListFilter.create(
        title='item',
        parameter_name='item__name',
    ),
)
