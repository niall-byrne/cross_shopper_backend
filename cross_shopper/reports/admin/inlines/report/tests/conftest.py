"""Test fixtures for the items app model admins."""

from unittest import mock

import pytest
from reports.admin.inlines.report import report_store


@pytest.fixture
def mocked_admin_site() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_model() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def item_scraper_config_inline(
    mocked_admin_site: mock.Mock,
    mocked_model: mock.Mock,
) -> report_store.ReportStoreInline:
  return report_store.ReportStoreInline(
      parent_model=mocked_model,
      admin_site=mocked_admin_site,
  )
