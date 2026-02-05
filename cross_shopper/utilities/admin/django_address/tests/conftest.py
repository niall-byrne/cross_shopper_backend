"""Test fixtures for the django-address app's custom model admins."""

from unittest import mock

import pytest
from utilities.admin.django_address import address, locality, state


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


@pytest.fixture
def locality_admin(
    mocked_admin_site: mock.Mock,
    mocked_model: mock.Mock,
) -> locality.LocalityAdmin:

  return locality.LocalityAdmin(
      model=mocked_model,
      admin_site=mocked_admin_site,
  )


@pytest.fixture
def state_admin(
    mocked_admin_site: mock.Mock,
    mocked_model: mock.Mock,
) -> state.StateAdmin:

  return state.StateAdmin(
      model=mocked_model,
      admin_site=mocked_admin_site,
  )
