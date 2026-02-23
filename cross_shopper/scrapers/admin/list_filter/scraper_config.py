"""ScraperConfig admin model list filter."""

from scrapers.admin.list_filter.filters.scraper_config.has_items import (
    HasItemsFilter,
)
from utilities.admin.list_filter import GenericListFilter

scraper_config_list_filter = (
    "is_active",
    GenericListFilter.create(
        title='scraper',
        parameter_name='scraper__name',
    ),
    HasItemsFilter,
)
