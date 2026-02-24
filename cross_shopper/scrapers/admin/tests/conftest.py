"""Test fixtures for the scrapers app model admins."""

from unittest import mock

import pytest
from scrapers.admin import scraper, scraper_config


@pytest.fixture
def mocked_request() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_admin_site() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_model() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def scraper_admin(
    mocked_admin_site: mock.Mock,
    mocked_model: mock.Mock,
) -> scraper.ScraperAdmin:

  return scraper.ScraperAdmin(
      model=mocked_model,
      admin_site=mocked_admin_site,
  )


@pytest.fixture
def scraper_config_admin(
    mocked_admin_site: mock.Mock,
    mocked_model: mock.Mock,
) -> scraper_config.ScraperConfigAdmin:

  return scraper_config.ScraperConfigAdmin(
      model=mocked_model,
      admin_site=mocked_admin_site,
  )
