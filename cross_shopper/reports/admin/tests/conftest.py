"""Test fixtures for the reports app model admins."""

from unittest import mock

import pytest
from reports.admin import ReportAdmin, ReportStoreAdmin


@pytest.fixture
def mocked_admin_site() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_model() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def report_admin(
    mocked_admin_site: mock.Mock,
    mocked_model: mock.Mock,
) -> ReportAdmin:
  return ReportAdmin(
      model=mocked_model,
      admin_site=mocked_admin_site,
  )


@pytest.fixture
def report_store_admin(
    mocked_admin_site: mock.Mock,
    mocked_model: mock.Mock,
) -> ReportStoreAdmin:
  return ReportStoreAdmin(
      model=mocked_model,
      admin_site=mocked_admin_site,
  )
