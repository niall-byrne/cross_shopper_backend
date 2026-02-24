"""ScraperConfig model list filter."""

from .has_items_filter import HasItemsFilter
from .scraper_filter import ScraperFilter

scraper_config_filter = ("is_active", ScraperFilter, HasItemsFilter)
