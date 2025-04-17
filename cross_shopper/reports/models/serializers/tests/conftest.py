"""Test fixtures for the report models serializers."""

from unittest import mock

import pytest
from pricing.models import Price


@pytest.fixture
def mocked_aggregate_last_52_weeks_manager(
    monkeypatch: pytest.MonkeyPatch,
) -> mock.Mock:
  manager_mock = mock.Mock()
  monkeypatch.setattr(Price, "aggregate_last_52_weeks", manager_mock)

  return manager_mock
