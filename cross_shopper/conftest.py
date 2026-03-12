"""Shared test fixtures for the cross_shopper project."""

# pylint: disable=redefined-outer-name

pytest_plugins = [
    "api.models.fixtures.client",
    "api.models.fixtures.user",
    "errors.models.fixtures.error",
    "errors.models.fixtures.error_type",
    "items.models.fixtures.attribute",
    "items.models.fixtures.brand",
    "items.models.fixtures.item",
    "items.models.fixtures.item_attribute",
    "items.models.fixtures.item_scraper_config",
    "items.models.fixtures.packaging",
    "items.models.fixtures.price_group",
    "pricing.models.fixtures.pricing",
    "reports.models.fixtures.report",
    "reports.models.fixtures.report_summary",
    "stores.models.fixtures.address",
    "stores.models.fixtures.franchise",
    "stores.models.fixtures.store",
    "scrapers.models.fixtures.scraper",
    "scrapers.models.fixtures.scraper_config",
]
