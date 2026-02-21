"""Error model list filter."""

from utilities.admin.list_filter.generic_list_filter import (
    GenericListFilter,
)

error_list_filter = (
    GenericListFilter.create(
        title="type",
        parameter_name="type__name",
    ),
    GenericListFilter.create(
        title="franchise",
        parameter_name="store__franchise__name",
    ),
    GenericListFilter.create(
        title="item",
        parameter_name="item__name",
    ),
    GenericListFilter.create(
        title="scraper",
        parameter_name="scraper_config__scraper__name",
    ),
)
