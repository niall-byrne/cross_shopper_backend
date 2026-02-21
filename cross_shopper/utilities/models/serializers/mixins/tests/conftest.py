"""Test fixtures for the utilities app serializer mixins."""

from typing import Callable, Dict
from unittest import mock

import pytest
from django.http import HttpRequest
from rest_framework import request

AliasCreateMockedRequest = Callable[[Dict[str, str]], request.Request]


@pytest.fixture
def mocked_model() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def create_mocked_request() -> AliasCreateMockedRequest:

  def create(query_param: Dict[str, str]) -> request.Request:
    http_request = HttpRequest()
    http_request.GET.update(query_param)
    return request.Request(http_request)

  return create
