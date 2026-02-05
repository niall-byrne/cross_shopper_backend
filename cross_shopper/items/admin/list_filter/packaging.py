"""Packaging admin model list filter."""

from utilities.admin.list_filter import GenericListFilter

packaging_list_filter = (
    GenericListFilter.create(
        title='container',
        parameter_name='container__name',
    ),
    GenericListFilter.create(
        title='unit',
        parameter_name='unit__name',
    ),
)
