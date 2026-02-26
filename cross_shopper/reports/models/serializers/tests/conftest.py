"""Test fixtures for the report models serializers."""

from typing import Callable, Dict
from unittest import mock

import pytest
from django.http import HttpRequest
from pricing.models import Price
from rest_framework import request

AliasCreateMockedRequest = Callable[[Dict[str, str]], request.Request]


@pytest.fixture
def create_mocked_request() -> AliasCreateMockedRequest:

  def create(query_param: Dict[str, str]) -> request.Request:
    http_request = HttpRequest()
    http_request.GET.update(query_param)
    return request.Request(http_request)

  return create


@pytest.fixture
def mocked_aggregate_last_52_weeks_manager(
    monkeypatch: pytest.MonkeyPatch,
) -> mock.Mock:
  manager_mock = mock.Mock()
  monkeypatch.setattr(Price, "aggregate_last_52_weeks", manager_mock)

  return manager_mock
