"""Test the ScraperConfigActionsAdminMixin model."""

from typing import Any
from unittest import mock

from scrapers.admin.mixins.scraper_config_actions import (
    ScraperConfigActionsAdminMixin,
)


class TestScraperConfigActionsAsDirectField:

  def test_action_activate_scraper_configs__updates_selected(
      self,
      action_admin: ScraperConfigActionsAdminMixin[Any],
      mocked_model: mock.Mock,
      mocked_request: mock.Mock,
  ) -> None:
    action_admin.action_activate_scraper_configs(mocked_request, mocked_model)

    mocked_model.update.assert_called_once_with(is_active=True)

  def test_action_activate_scraper_configs__notifies_user(
      self,
      action_admin: ScraperConfigActionsAdminMixin[Any],
      mocked_model: mock.Mock,
      mocked_request: mock.Mock,
  ) -> None:
    action_admin.action_activate_scraper_configs(mocked_request, mocked_model)

    mocked_request._messages.add.assert_called_once_with(  # noqa: SLF001
      20,
      str(mocked_model.update.return_value) +
      " scraper configs were successfully activated.",
      "",
    )

  def test_action_deactivate_scraper_configs__updates_selected(
      self,
      action_admin: ScraperConfigActionsAdminMixin[Any],
      mocked_model: mock.Mock,
      mocked_request: mock.Mock,
  ) -> None:
    action_admin.action_deactivate_scraper_configs(mocked_request, mocked_model)

    mocked_model.update.assert_called_once_with(is_active=False)

  def test_action_deactivate_scraper_configs__notifies_user(
      self,
      action_admin: ScraperConfigActionsAdminMixin[Any],
      mocked_model: mock.Mock,
      mocked_request: mock.Mock,
  ) -> None:
    action_admin.action_deactivate_scraper_configs(mocked_request, mocked_model)

    mocked_request._messages.add.assert_called_once_with(  # noqa: SLF001
      20,
      str(mocked_model.update.return_value) +
      " scraper configs were successfully deactivated.",
      "",
    )


class TestScraperConfigActionsAsRelatedField:

  def test_action_activate_scraper_configs__updates_selected(
      self,
      related_action_admin: ScraperConfigActionsAdminMixin[Any],
      mocked_model: mock.Mock,
      mocked_request: mock.Mock,
      mocked_scraper_config: mock.Mock,
  ) -> None:
    related_action_admin.action_activate_scraper_configs(
        mocked_request,
        mocked_model,
    )

    mocked_scraper_config.objects.filter. \
      return_value.update.assert_called_once_with(is_active=True)

  def test_action_activate_scraper_configs__notifies_user(
      self,
      related_action_admin: ScraperConfigActionsAdminMixin[Any],
      mocked_model: mock.Mock,
      mocked_request: mock.Mock,
      mocked_scraper_config: mock.Mock,
  ) -> None:
    related_action_admin.action_activate_scraper_configs(
        mocked_request,
        mocked_model,
    )

    mocked_request._messages.add.assert_called_once_with(  # noqa: SLF001
      20,
      str(
        mocked_scraper_config.objects.filter.
        return_value.update.return_value
      ) + " related scraper configs were successfully activated.",
      "",
    )

  def test_action_deactivate_scraper_configs__updates_selected(
      self,
      related_action_admin: ScraperConfigActionsAdminMixin[Any],
      mocked_model: mock.Mock,
      mocked_request: mock.Mock,
      mocked_scraper_config: mock.Mock,
  ) -> None:
    related_action_admin.action_deactivate_scraper_configs(
        mocked_request,
        mocked_model,
    )

    mocked_scraper_config.objects.filter. \
      return_value.update.assert_called_once_with(is_active=False)

  def test_action_deactivate_scraper_configs__notifies_user(
      self,
      related_action_admin: ScraperConfigActionsAdminMixin[Any],
      mocked_model: mock.Mock,
      mocked_request: mock.Mock,
      mocked_scraper_config: mock.Mock,
  ) -> None:
    related_action_admin.action_deactivate_scraper_configs(
        mocked_request,
        mocked_model,
    )

    mocked_request._messages.add.assert_called_once_with(  # noqa: SLF001
      20,
      str(
        mocked_scraper_config.objects.filter.
        return_value.update.return_value
      ) + " related scraper configs were successfully deactivated.",
      "",
    )
