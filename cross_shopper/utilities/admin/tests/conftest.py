"""Test fixtures for the utilities app model admins."""

from unittest import mock

import pytest
from utilities.admin import address


@pytest.fixture
def mocked_admin_site() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_model() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def address_admin(
    mocked_admin_site: mock.Mock,
    mocked_model: mock.Mock,
) -> address.AddressAdmin:

  return address.AddressAdmin(
      model=mocked_model,
      admin_site=mocked_admin_site,
  )
