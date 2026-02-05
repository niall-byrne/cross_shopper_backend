"""Test fixtures for the stores app model admins."""

from unittest import mock

import pytest
from stores.admin import franchise, store


@pytest.fixture
def mocked_admin_site() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_model() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def franchise_admin(
    mocked_admin_site: mock.Mock,
    mocked_model: mock.Mock,
) -> franchise.FranchiseAdmin:

  return franchise.FranchiseAdmin(
      model=mocked_model,
      admin_site=mocked_admin_site,
  )


@pytest.fixture
def store_admin(
    mocked_admin_site: mock.Mock,
    mocked_model: mock.Mock,
) -> store.StoreAdmin:

  return store.StoreAdmin(
      model=mocked_model,
      admin_site=mocked_admin_site,
  )
