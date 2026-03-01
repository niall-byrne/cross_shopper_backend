"""Test fixtures for the utilities app filters."""

from unittest.mock import Mock

import pytest
from django.http import QueryDict
from utilities.views.filters.pass_through import PassThroughFilter


@pytest.fixture
def pass_through_filter() -> PassThroughFilter:
  return PassThroughFilter(field_name='test_field')


@pytest.fixture
def request_with_query_params() -> Mock:
  request = Mock()
  request.GET = QueryDict('', mutable=True)
  request.GET.update({'existing': 'value'})
  return request
