"""Test fixtures for the admin filter bases."""

from unittest import mock

import pytest
from utilities.admin.list_filters.generic_list_filter import GenericListFilter


class ConcreteGenericListFilter(GenericListFilter):
  title = "test_title"
  parameter_name = "test_param"


@pytest.fixture
def mocked_request() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_model_admin() -> mock.Mock:
  instance = mock.Mock()
  instance.get_queryset.return_value.values_list.return_value.distinct.return_value.order_by.return_value = []
  return instance


@pytest.fixture
def mocked_queryset() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def generic_list_filter(
    mocked_request: mock.Mock,
    mocked_model_admin: mock.Mock,
) -> GenericListFilter:
  return ConcreteGenericListFilter(
      request=mocked_request,
      params={},
      model=mock.Mock(),
      model_admin=mocked_model_admin,
  )
