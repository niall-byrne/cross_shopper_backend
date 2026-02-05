"""ItemScraperConfig admin model list filter."""

from utilities.admin.list_filters import GenericListFilter

item_scraper_config_list_filter = (
    GenericListFilter.create(
        title="scraper",
        parameter_name="scraper_config__scraper__name",
    ),
    GenericListFilter.create(
        title="item",
        parameter_name="item__name",
    ),
)
