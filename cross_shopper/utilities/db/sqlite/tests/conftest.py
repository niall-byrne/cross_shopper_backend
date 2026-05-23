"""Test fixtures for the utilities app custom SQLite database wrapper."""

from unittest import mock

import pytest
from utilities.db.sqlite import base


@pytest.fixture
def mocked_cursor_creator() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def sqlite_wrapper_instance(
    mocked_cursor_creator: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> base.DatabaseWrapper:
  instance = base.DatabaseWrapper({})
  monkeypatch.setattr(instance, "cursor", mocked_cursor_creator)
  return instance
