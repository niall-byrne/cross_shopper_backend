"""Test fixtures for scraper_config list filters."""

from unittest import mock
import pytest

@pytest.fixture
def mocked_request() -> mock.Mock:
  return mock.Mock()
