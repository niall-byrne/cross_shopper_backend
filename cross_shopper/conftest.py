"""Shared test fixtures for the cross_shopper project."""

# pylint: disable=redefined-outer-name

pytest_plugins = [
    "items.models.fixtures.brand",
    "items.models.fixtures.item",
    "items.models.fixtures.item_scraper_config",
    "items.models.fixtures.packaging",
    "reports.models.fixtures.report",
    "stores.models.fixtures.address",
    "stores.models.fixtures.franchise",
    "stores.models.fixtures.store",
    "scrapers.models.fixtures.scraper",
    "scrapers.models.fixtures.scraper_config",
]
