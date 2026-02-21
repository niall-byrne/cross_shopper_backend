"""ScraperConfig admin model list filter."""

from utilities.admin.list_filters import GenericListFilter

scraper_config_list_filter = (
    "is_active",
    GenericListFilter.create(
        title='scraper',
        parameter_name='scraper__name',
    ),
)
