"""Test fixtures for the utilities app serializer fields."""

from typing import Any, Type
from unittest import mock

import pytest
from rest_framework import serializers
from utilities.models.serializers.fields import (
    blonde,
    context,
    lowercase,
    slug_related_field,
    title,
)


@pytest.fixture
def mocked_input_value() -> str:
  return "mocked_input_value"


@pytest.fixture
def mocked_model() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_model_alternate() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_related_model(mocked_model: mock.Mock) -> mock.Mock:
  instance = mock.Mock(
      **{"get.return_value": mocked_model},
      **{"create.return_value": mocked_model}
  )
  instance.__deepcopy__ = lambda *_args: instance
  return instance


@pytest.fixture
def mocked_related_model_alternate(
    mocked_model_alternate: mock.Mock,
) -> mock.Mock:
  instance = mock.Mock(
      **{"get.return_value": mocked_model_alternate},
      **{"create.return_value": mocked_model_alternate},
  )
  instance.__deepcopy__ = lambda *_args: instance
  return instance


@pytest.fixture
def mocked_sanitize() -> mock.Mock:
  return mock.Mock(return_value="sanitized_value")


@pytest.fixture
def mocked_slug_field() -> str:
  return "mocked_related_field"


@pytest.fixture
def mocked_slug_field_alternate() -> str:
  return "mocked_related_field_alternate"


@pytest.fixture
def blonde_field_serializer(
    mocked_sanitize: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> Type[serializers.Serializer[Any]]:
  monkeypatch.setattr(
      blonde.PeroxideFieldMixin,
      "sanitize",
      mocked_sanitize,
  )

  class TestSerializer(serializers.Serializer[Any]):
    field = blonde.BlondeCharField(allow_null=True)

  return TestSerializer


@pytest.fixture
def context_field_serializer() -> Type[serializers.Serializer[Any]]:

  class TestSerializer(serializers.Serializer[Any]):
    field = context.ContextField(context_key="context1")
    field_with_default = context.ContextField(
        context_key="context2",
        default_value=lambda: "default_value",
    )

  return TestSerializer


@pytest.fixture
def lowercase_field_serializer() -> Type[serializers.Serializer[Any]]:

  class TestSerializer(serializers.Serializer[Any]):
    field = lowercase.LowerCaseField()

  return TestSerializer


@pytest.fixture
def creatable_slug_related_field_serializer(
    mocked_related_model: mock.Mock,
    mocked_related_model_alternate: mock.Mock,
    mocked_sanitize: mock.Mock,
    mocked_slug_field: str,
    mocked_slug_field_alternate: str,
    monkeypatch: pytest.MonkeyPatch,
) -> Type[serializers.Serializer[Any]]:
  monkeypatch.setattr(
      slug_related_field.PeroxideFieldMixin,
      "sanitize",
      mocked_sanitize,
  )

  class TestSerializer(serializers.Serializer[Any]):
    case_sensitive = slug_related_field.CreatableSlugRelatedField(
        case_sensitive=True,
        queryset=mocked_related_model,
        slug_field=mocked_slug_field,
        required=False,
    )
    case_insensitive = slug_related_field.CreatableSlugRelatedField(
        case_sensitive=False,
        queryset=mocked_related_model_alternate,
        slug_field=mocked_slug_field_alternate,
        required=False,
    )
    default_sensitivity = slug_related_field.CreatableSlugRelatedField(
        queryset=mocked_related_model,
        slug_field=mocked_slug_field,
        required=False,
    )

  return TestSerializer


@pytest.fixture
def title_field_serializer() -> Type[serializers.Serializer[Any]]:

  class TestSerializer(serializers.Serializer[Any]):
    field = title.TitleField()

  return TestSerializer
