"""Test fixtures for the admin template context processors."""

import pytest
from django.http import HttpRequest


@pytest.fixture
def mocked_request() -> HttpRequest:
  return HttpRequest()
