"""Test fixtures for the items app model admins."""

from unittest import mock

import pytest
from django.contrib import admin
from items.admin import item, packaging_container, packaging_unit


@pytest.fixture
def mocked_admin_site() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_db_field() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_form() -> mock.Mock:
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
def mocked_report_manger() -> mock.Mock:
  instance = mock.Mock()
  instance.filter.return_value = [mock.Mock(), mock.Mock(), mock.Mock()]
  return instance


@pytest.fixture
def mocked_request() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def item_admin(
    mocked_admin_site: mock.Mock,
    mocked_formfield_for_foreignkey: mock.Mock,
    mocked_model: mock.Mock,
    mocked_model_manager: mock.Mock,
    mocked_report_manger: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> item.ItemAdmin:
  monkeypatch.setattr(
      admin.ModelAdmin,
      "formfield_for_foreignkey",
      mocked_formfield_for_foreignkey,
  )
  monkeypatch.setattr(
      item.Report,
      "objects",
      mocked_report_manger,
  )
  monkeypatch.setattr(
      item.Brand,
      "objects",
      mocked_model_manager,
  )
  monkeypatch.setattr(
      item.Packaging,
      "objects",
      mocked_model_manager,
  )

  return item.ItemAdmin(
      model=mocked_model,
      admin_site=mocked_admin_site,
  )


@pytest.fixture
def packaging_container_admin(
    mocked_admin_site: mock.Mock,
    mocked_model: mock.Mock,
) -> packaging_container.PackagingContainerAdmin:

  return packaging_container.PackagingContainerAdmin(
      model=mocked_model,
      admin_site=mocked_admin_site,
  )


@pytest.fixture
def packaging_unit_admin(
    mocked_admin_site: mock.Mock,
    mocked_model: mock.Mock,
) -> packaging_unit.PackagingUnitAdmin:

  return packaging_unit.PackagingUnitAdmin(
      model=mocked_model,
      admin_site=mocked_admin_site,
  )
