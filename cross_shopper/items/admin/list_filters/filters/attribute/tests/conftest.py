"""Test fixtures for the Attribute app model admin list filters."""

from unittest import mock

import pytest


@pytest.fixture
def mocked_model() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_model_admin() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_request() -> mock.Mock:
  return mock.Mock()
