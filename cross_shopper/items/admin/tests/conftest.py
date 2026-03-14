"""Test fixtures for the items app model admins."""

from unittest import mock

import pytest
from django.contrib import admin
from items.admin import (
    attribute,
    brand,
    item,
    item_attribute,
    item_scraper_config,
    packaging,
    packaging_container,
    packaging_unit,
    price_group,
    price_group_attribute,
)


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
def mocked_price_group_members_mixin() -> mock.Mock:
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
def attribute_admin(
    mocked_admin_site: mock.Mock,
    mocked_model: mock.Mock,
) -> attribute.AttributeAdmin:
  return attribute.AttributeAdmin(
      model=mocked_model,
      admin_site=mocked_admin_site,
  )


@pytest.fixture
def brand_admin(
    mocked_admin_site: mock.Mock,
    mocked_model: mock.Mock,
) -> brand.BrandAdmin:
  return brand.BrandAdmin(
      model=mocked_model,
      admin_site=mocked_admin_site,
  )


@pytest.fixture
def item_admin(
    mocked_admin_site: mock.Mock,
    mocked_formfield_for_foreignkey: mock.Mock,
    mocked_model: mock.Mock,
    mocked_model_manager: mock.Mock,
    mocked_price_group_members_mixin: mock.Mock,
    mocked_report_manger: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> item.ItemAdmin:
  monkeypatch.setattr(
      admin.ModelAdmin,
      "formfield_for_foreignkey",
      mocked_formfield_for_foreignkey,
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
  monkeypatch.setattr(
      item.PriceGroupMembersAdminMixin,
      "members",
      mocked_price_group_members_mixin,
  )
  monkeypatch.setattr(
      item.Report,
      "objects",
      mocked_report_manger,
  )

  return item.ItemAdmin(
      model=mocked_model,
      admin_site=mocked_admin_site,
  )


@pytest.fixture
def item_attribute_admin(
    mocked_admin_site: mock.Mock,
    mocked_model: mock.Mock,
) -> item_attribute.ItemAttributeAdmin:
  return item_attribute.ItemAttributeAdmin(
      model=mocked_model,
      admin_site=mocked_admin_site,
  )


@pytest.fixture
def item_scraper_config_admin(
    mocked_admin_site: mock.Mock,
    mocked_model: mock.Mock,
) -> item_scraper_config.ItemScraperConfigAdmin:
  return item_scraper_config.ItemScraperConfigAdmin(
      model=mocked_model,
      admin_site=mocked_admin_site,
  )


@pytest.fixture
def packaging_admin(
    mocked_admin_site: mock.Mock,
    mocked_model: mock.Mock,
) -> packaging.PackagingAdmin:
  return packaging.PackagingAdmin(
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


@pytest.fixture
def price_group_admin(
    mocked_admin_site: mock.Mock,
    mocked_model: mock.Mock,
) -> price_group.PriceGroupAdmin:
  return price_group.PriceGroupAdmin(
      model=mocked_model,
      admin_site=mocked_admin_site,
  )


@pytest.fixture
def price_group_attribute_admin(
    mocked_admin_site: mock.Mock,
    mocked_model: mock.Mock,
) -> price_group_attribute.PriceGroupAttributeAdmin:
  return price_group_attribute.PriceGroupAttributeAdmin(
      model=mocked_model,
      admin_site=mocked_admin_site,
  )
