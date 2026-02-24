"""Error model list filter."""

from .error_type_filter import ErrorTypeFilter
from .franchise_name_filter import FranchiseNameFilter
from .is_reoccurring_filter import IsReoccurringFilter
from .item_name_filter import ItemNameFilter
from .scraper_config_is_active_filter import ScraperConfigIsActiveFilter
from .scraper_name_filter import ScraperNameFilter

error_filter = (
    ErrorTypeFilter,
    ItemNameFilter,
    IsReoccurringFilter,
    FranchiseNameFilter,
    ScraperConfigIsActiveFilter,
    ScraperNameFilter,
)
