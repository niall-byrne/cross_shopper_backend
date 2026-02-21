"""Test fixtures for the errors app model admins."""

from unittest import mock

import pytest
from errors.admin import error, error_type


@pytest.fixture
def mocked_admin_site() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_model() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_scraper_config(monkeypatch: pytest.MonkeyPatch) -> mock.Mock:
  instance = mock.Mock(return_value=[mock.Mock(), mock.Mock()])
  monkeypatch.setattr(error, "ScraperConfig", instance)
  return instance


@pytest.fixture
def mocked_request() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def error_admin(
    mocked_admin_site: mock.Mock,
    mocked_model: mock.Mock,
) -> error.ErrorAdmin:
  return error.ErrorAdmin(
      model=mocked_model,
      admin_site=mocked_admin_site,
  )


@pytest.fixture
def error_type_admin(
    mocked_admin_site: mock.Mock,
    mocked_model: mock.Mock,
) -> error_type.ErrorTypeAdmin:
  return error_type.ErrorTypeAdmin(
      model=mocked_model,
      admin_site=mocked_admin_site,
  )
