"""Test the admin for the Error model."""
from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import admin
from errors.admin.list_filters.error import error_list_filter

if TYPE_CHECKING:
  from unittest import mock

  from errors.admin.error import ErrorAdmin


class TestErrorAdmin:

  def test_instantiate__inheritance(
      self,
      error_admin: ErrorAdmin,
  ) -> None:
    assert isinstance(error_admin, admin.ModelAdmin)

  def test_instantiate__has_correct_actions(
      self,
      error_admin: ErrorAdmin,
  ) -> None:
    assert error_admin.actions == (
        "action_mark_as_reoccurring",
        "action_mark_as_non_reoccurring",
        "action_reset_error_count",
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

  def test_action_mark_as_reoccurring__updates_selected(
      self,
      error_admin: ErrorAdmin,
      mocked_model: mock.Mock,
      mocked_request: mock.Mock,
  ) -> None:
    error_admin.action_mark_as_reoccurring(mocked_request, mocked_model)

    mocked_model.update.assert_called_once_with(is_reoccurring=True)

  def test_action_mark_as_reoccurring__notifies_user(
      self,
      error_admin: ErrorAdmin,
      mocked_model: mock.Mock,
      mocked_request: mock.Mock,
  ) -> None:
    error_admin.action_mark_as_reoccurring(mocked_request, mocked_model)

    mocked_request._messages.add.assert_called_once_with(  # noqa: SLF001
      20,
      f"{mocked_model.update.return_value} errors were successfully "
      f"marked as reoccurring.",
      "",
    )

  def test_action_mark_as_non_reoccurring__updates_selected(
      self,
      error_admin: ErrorAdmin,
      mocked_model: mock.Mock,
      mocked_request: mock.Mock,
  ) -> None:
    error_admin.action_mark_as_non_reoccurring(mocked_request, mocked_model)

    mocked_model.update.assert_called_once_with(is_reoccurring=False)

  def test_action_mark_as_non_reoccurring__notifies_user(
      self,
      error_admin: ErrorAdmin,
      mocked_model: mock.Mock,
      mocked_request: mock.Mock,
  ) -> None:
    error_admin.action_mark_as_non_reoccurring(mocked_request, mocked_model)

    mocked_request._messages.add.assert_called_once_with(  # noqa: SLF001
      20,
      f"{mocked_model.update.return_value} errors were successfully "
      f"marked as non-reoccurring.",
      "",
    )

  def test_action_reset_error_count__updates_selected(
      self,
      error_admin: ErrorAdmin,
      mocked_model: mock.Mock,
      mocked_request: mock.Mock,
  ) -> None:
    error_admin.action_reset_error_count(mocked_request, mocked_model)

    mocked_model.update.assert_called_once_with(count=0)

  def test_action_reset_error_count__notifies_user(
      self,
      error_admin: ErrorAdmin,
      mocked_model: mock.Mock,
      mocked_request: mock.Mock,
  ) -> None:
    error_admin.action_reset_error_count(mocked_request, mocked_model)

    mocked_request._messages.add.assert_called_once_with(  # noqa: SLF001
      20,
      f"{mocked_model.update.return_value} error counts were successfully "
      "reset.",
      "",
    )
