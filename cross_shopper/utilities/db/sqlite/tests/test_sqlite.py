"""Test the custom SQLite database wrapper."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.backends.sqlite3 import base

if TYPE_CHECKING:
  from unittest import mock

  from utilities.db.sqlite import base as sqlite_base


class TestDatabaseWrapper:

  def test_instantiate__inheritance(
      self,
      sqlite_wrapper_instance: sqlite_base.DatabaseWrapper,
  ) -> None:
    assert isinstance(sqlite_wrapper_instance, base.DatabaseWrapper)

  def test_start_transaction_under_autocommit__uses_begin_immediate_keyword(
      self,
      mocked_cursor_creator: mock.Mock,
      sqlite_wrapper_instance: sqlite_base.DatabaseWrapper,
  ) -> None:
    sqlite_wrapper_instance._start_transaction_under_autocommit()

    mocked_cursor_creator.return_value.execute.assert_called_once_with(
        "BEGIN IMMEDIATE"
    )
