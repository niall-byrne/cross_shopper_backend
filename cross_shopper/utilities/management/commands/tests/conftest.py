"""Test fixtures for the utilities management commands."""

import io
from unittest import mock

import pytest
from utilities.management.commands import autoadmin


@pytest.fixture
def mocked_create_superuser(monkeypatch: pytest.MonkeyPatch,) -> mock.Mock:
  instance = mock.Mock()
  monkeypatch.setattr(autoadmin, "create_superuser", instance)
  return instance


@pytest.fixture
def mocked_stderr() -> io.StringIO:
  return io.StringIO()


@pytest.fixture
def mocked_stdout() -> io.StringIO:
  return io.StringIO()
