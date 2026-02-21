"""Test the admin for the Error model."""

from unittest import mock

from django.contrib import admin
from errors.admin.error import ErrorAdmin
from errors.admin.list_filters.error import error_list_filter
from scrapers.admin.mixins.scraper_config_actions import (
    ScraperConfigActionsAdminMixin,
)


class TestErrorAdmin:
  """Test the ErrorAdmin class."""

  def test_instantiate__inheritance(
      self,
      error_admin: ErrorAdmin,
  ) -> None:
    assert isinstance(error_admin, admin.ModelAdmin)
    assert isinstance(error_admin, ScraperConfigActionsAdminMixin)

  def test_instantiate__has_correct_actions(
      self,
      error_admin: ErrorAdmin,
  ) -> None:
    assert error_admin.actions == (
        "mark_as_reoccurring",
        "mark_as_non_reoccurring",
        "activate_scraper_configs",
        "deactivate_scraper_configs",
    )

  def test_instantiate__has_correct_list_filter(
      self,
      error_admin: ErrorAdmin,
  ) -> None:
    assert error_admin.list_filter == error_list_filter

  def test_instantiate__has_correct_ordering(
      self,
      error_admin: ErrorAdmin,
  ) -> None:
    assert error_admin.ordering == (
        "type__name",
        "store__franchise__name",
        "item__name",
        "scraper_config__url",
    )

  def test_instantiate__has_correct_search_fields(
      self,
      error_admin: ErrorAdmin,
  ) -> None:
    assert error_admin.search_fields == (
        "store__franchise__name",
        "item__name",
        "scraper_config__url",
    )

  def test_mark_as_reoccurring__updates_selected(
      self,
      error_admin: ErrorAdmin,
      mocked_model: mock.Mock,
      mocked_request: mock.Mock,
  ) -> None:
    error_admin.mark_as_reoccurring(mocked_request, mocked_model)

    mocked_model.update.assert_called_once_with(is_reoccurring=True)

  def test_mark_as_reoccurring__notifies_user(
      self,
      error_admin: ErrorAdmin,
      mocked_model: mock.Mock,
      mocked_request: mock.Mock,
  ) -> None:
    error_admin.mark_as_reoccurring(mocked_request, mocked_model)

    mocked_request._messages.add.assert_called_once_with(  # noqa: SLF001
      20,
      f"{mocked_model.update.return_value} errors were successfully "
      f"marked as reoccurring.",
      "",
    )

  def test_mark_as_non_reoccurring__updates_selected(
      self,
      error_admin: ErrorAdmin,
      mocked_model: mock.Mock,
      mocked_request: mock.Mock,
  ) -> None:
    error_admin.mark_as_non_reoccurring(mocked_request, mocked_model)

    mocked_model.update.assert_called_once_with(is_reoccurring=False)

  def test_mark_as_non_reoccurring__notifies_user(
      self,
      error_admin: ErrorAdmin,
      mocked_model: mock.Mock,
      mocked_request: mock.Mock,
  ) -> None:
    error_admin.mark_as_non_reoccurring(mocked_request, mocked_model)

    mocked_request._messages.add.assert_called_once_with(  # noqa: SLF001
      20,
      f"{mocked_model.update.return_value} errors were successfully "
      f"marked as non-reoccurring.",
      "",
    )
