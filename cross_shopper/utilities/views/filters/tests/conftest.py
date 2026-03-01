"""Test fixtures for the utilities app filters."""

from unittest.mock import Mock

import pytest
from django.http import QueryDict
from utilities.views.filters.pass_through import PassThroughFilter


@pytest.fixture
def mock_field() -> Mock:
  field = Mock()
  field.verbose_name = "Mock model"
  return field


@pytest.fixture
def mock_model(mock_field: Mock) -> Mock:
  model = Mock()
  model._meta.get_field.return_value = mock_field
  return model


@pytest.fixture
def mock_queryset() -> Mock:
  return Mock()


@pytest.fixture
def pass_through_filter() -> PassThroughFilter:
  return PassThroughFilter(field_name='test_field')


@pytest.fixture
def request_with_query_params() -> Mock:
  request = Mock()
  request.GET = QueryDict('', mutable=True)
  request.GET.update({'existing': 'value'})
  return request
