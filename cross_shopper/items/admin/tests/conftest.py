"""Test fixtures for the items app model admins."""

from unittest import mock

import pytest
from django.contrib import admin
from items.admin.item import Brand, ItemAdmin, Packaging


@pytest.fixture
def mocked_admin_site() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_db_field() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_formfield_for_foreignkey() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_model() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_model_manager() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_request() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def item_admin(
    mocked_admin_site: mock.Mock, mocked_formfield_for_foreignkey: mock.Mock,
    mocked_model: mock.Mock, mocked_model_manager: mock.Mock,
    monkeypatch: pytest.MonkeyPatch
) -> ItemAdmin:
  monkeypatch.setattr(
      admin.ModelAdmin,
      "formfield_for_foreignkey",
      mocked_formfield_for_foreignkey,
  )
  monkeypatch.setattr(
      Brand,
      "objects",
      mocked_model_manager,
  )
  monkeypatch.setattr(
      Packaging,
      "objects",
      mocked_model_manager,
  )

  return ItemAdmin(
      model=mocked_model,
      admin_site=mocked_admin_site,
  )
