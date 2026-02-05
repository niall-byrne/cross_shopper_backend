"""Franchise admin model list filter."""

from utilities.admin.list_filters import GenericListFilter

franchise_list_filter = (
    GenericListFilter.create(
        title='scraper',
        parameter_name='scraper__name',
    ),
)
