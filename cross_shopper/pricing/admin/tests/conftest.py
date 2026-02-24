"""Test fixtures for the pricing app model admins."""

from unittest import mock

import pytest
from pricing.admin import PriceAdmin


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
def price_admin(
    mocked_admin_site: mock.Mock,
    mocked_model: mock.Mock,
) -> PriceAdmin:
  return PriceAdmin(
      model=mocked_model,
      admin_site=mocked_admin_site,
  )
