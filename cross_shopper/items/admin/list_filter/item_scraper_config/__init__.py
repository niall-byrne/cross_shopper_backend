"""ItemScraperConfig model list filter."""

from .item_filter import ItemFilter
from .scraper_filter import ScraperFilter
from .scraper_is_active_filter import ScraperIsActiveFilter

item_scraper_config_filter = (ScraperIsActiveFilter, ScraperFilter, ItemFilter)
