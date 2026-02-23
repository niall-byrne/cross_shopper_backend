"""Shared test fixtures for the cross_shopper project."""

# pylint: disable=redefined-outer-name

pytest_plugins = [
    "api.views.fixtures.client",
    "api.views.fixtures.user",
    "errors.models.fixtures.error",
    "errors.models.fixtures.error_type",
    "items.models.fixtures.brand",
    "items.models.fixtures.item",
    "items.models.fixtures.item_scraper_config",
    "items.models.fixtures.packaging",
    "pricing.models.fixtures.pricing",
    "reports.models.fixtures.report",
    "stores.models.fixtures.address",
    "stores.models.fixtures.franchise",
    "stores.models.fixtures.store",
    "scrapers.models.fixtures.scraper",
    "scrapers.models.fixtures.scraper_config",
]
