"""Test fixtures for the Utilities viewset mixin classes."""

from unittest import mock

import pytest
from rest_framework.test import APIRequestFactory
from rest_framework.viewsets import ModelViewSet
from utilities.views.viewsets.mixins.upsert import UpsertModelMixin


@pytest.fixture
def api_factory() -> APIRequestFactory:
  return APIRequestFactory()


@pytest.fixture
def mocked_query_set() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_serializer() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def concrete_upsert_view_set(
    mocked_query_set: mock.Mock,
    mocked_serializer: type[mock.Mock],
) -> type[ModelViewSet[mock.Mock]]:

  class ConcreteViewSet(
      UpsertModelMixin[mock.Mock],
      ModelViewSet[mock.Mock],
  ):

    queryset = mocked_query_set
    serializer_class = mocked_serializer
    permission_classes = ()

  return ConcreteViewSet
