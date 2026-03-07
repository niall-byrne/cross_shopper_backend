"""Test fixtures for the utilities app serializer fields."""

from typing import Any
from unittest import mock

import pytest
from rest_framework import serializers
from utilities.models.serializers.fields import (
    blonde,
    context,
    lowercase,
    title,
)


@pytest.fixture
def mocked_input_value() -> str:
  return "mocked_input_value"


@pytest.fixture
def mocked_model() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_sanitize() -> mock.Mock:
  return mock.Mock(return_value="sanitized_value")


@pytest.fixture
def blonde_field_serializer(
    mocked_sanitize: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> type[serializers.Serializer[Any]]:
  monkeypatch.setattr(
      blonde.PeroxideFieldMixin,
      "sanitize",
      mocked_sanitize,
  )

  class TestSerializer(serializers.Serializer[Any]):
    field = blonde.BlondeCharField(allow_null=True)

  return TestSerializer


@pytest.fixture
def context_field_serializer() -> type[serializers.Serializer[Any]]:

  class TestSerializer(serializers.Serializer[Any]):
    field = context.ContextField(context_key="context1")
    field_with_default = context.ContextField(
        context_key="context2",
        default_value=lambda: "default_value",
    )

  return TestSerializer


@pytest.fixture
def lowercase_field_serializer() -> type[serializers.Serializer[Any]]:

  class TestSerializer(serializers.Serializer[Any]):
    field = lowercase.LowerCaseField()

  return TestSerializer


@pytest.fixture
def title_field_serializer() -> type[serializers.Serializer[Any]]:

  class TestSerializer(serializers.Serializer[Any]):
    field = title.TitleField()

  return TestSerializer
