"""Tests fixtures for the scraper models admin mixins."""

from typing import Type
from unittest import mock

import pytest
from django.contrib import admin
from scrapers.admin.mixins import scraper_config_actions


@pytest.fixture
def mocked_admin_site() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_model() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_scraper_config(monkeypatch: pytest.MonkeyPatch) -> mock.Mock:
  instance = mock.Mock(return_value=[mock.Mock(), mock.Mock()])
  monkeypatch.setattr(scraper_config_actions, "ScraperConfig", instance)
  return instance


@pytest.fixture
def mocked_request() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def concrete_action_admin() -> Type[admin.ModelAdmin[mock.Mock]]:

  class ConcreteActionAdmin(
      scraper_config_actions.ScraperConfigActionsAdminMixin[mock.Mock],
      admin.ModelAdmin[mock.Mock],
  ):
    actions = ("activate_scraper_configs", "deactivate_scraper_configs")

  return ConcreteActionAdmin


@pytest.fixture
def action_admin(
    concrete_action_admin: Type[admin.ModelAdmin[mock.Mock]],
    mocked_admin_site: mock.Mock,
    mocked_model: mock.Mock,
) -> admin.ModelAdmin[mock.Mock]:
  return concrete_action_admin(
      model=mocked_model,
      admin_site=mocked_admin_site,
  )


@pytest.fixture
def related_action_admin(
    action_admin: scraper_config_actions.ScraperConfigActionsAdminMixin,
) -> scraper_config_actions.ScraperConfigActionsAdminMixin:
  action_admin.scraper_config_is_related_model = True
  return action_admin
