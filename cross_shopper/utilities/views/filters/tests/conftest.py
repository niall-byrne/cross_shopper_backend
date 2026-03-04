"""Test fixtures for the utilities app filters."""

from unittest.mock import Mock

import pytest
from django.http import QueryDict
from utilities.views.filters import passthrough


@pytest.fixture
def mocked_field() -> Mock:
  field = Mock()
  field.verbose_name = "Mock model"
  return field


@pytest.fixture
def mocked_model(mocked_field: Mock) -> Mock:
  model = Mock()
  model._meta.get_field.return_value = mocked_field
  return model


@pytest.fixture
def mocked_queryset() -> Mock:
  return Mock()


@pytest.fixture
def mocked_request_with_query_params() -> Mock:
  request = Mock()
  request.GET = QueryDict('', mutable=True)
  request.GET.update({'param': 'value'})
  return request


@pytest.fixture
def passthrough_filter(
    monkeypatch: pytest.MonkeyPatch,
    mocked_request_with_query_params: Mock,
) -> passthrough.PassThroughFilter:
  monkeypatch.setattr(
      passthrough.QuerySetRequestMixin,
      'get_request',
      Mock(return_value=mocked_request_with_query_params),
  )

  return passthrough.PassThroughFilter(field_name='test_field')
