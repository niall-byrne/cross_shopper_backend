"""Tests for the ContextField serializer field."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest
from rest_framework import serializers
from utilities.models.serializers.fields.context import ContextField

if TYPE_CHECKING:
  from unittest import mock


class TestContextField:

  def test_instantiate__without_context_field__raises_exception(self) -> None:

    with pytest.raises(Exception) as exc:

      class MalformedContextFieldSerializer(serializers.Serializer[Any]):
        field = ContextField()

    assert str(exc.value) == ContextField.Messages.no_context_key

  def test_deserialize__with_full_context__returns_context_values(
      self,
      context_field_serializer: type[serializers.Serializer[Any]],
  ) -> None:
    serializer = context_field_serializer(
        data={},
        context={
            "context1": "expected_value1",
            "context2": "expected_value2"
        },
    )

    serializer.is_valid(raise_exception=True)

    assert serializer.data["field"] == "expected_value1"
    assert serializer.data["field_with_default"] == "expected_value2"

  def test_serialize__with_full_context__returns_instance(
      self,
      context_field_serializer: type[serializers.Serializer[Any]],
      mocked_model: mock.Mock,
  ) -> None:
    serializer = context_field_serializer(
        mocked_model,
        context={
            "context1": "expected_value1",
            "context2": "expected_value2"
        },
    )

    assert serializer.instance == mocked_model

  def test_deserialize__partial_context__returns_context_value_and_default(
      self,
      context_field_serializer: type[serializers.Serializer[Any]],
  ) -> None:
    serializer = context_field_serializer(
        data={},
        context={"context1": "expected_value1"},
    )

    serializer.is_valid(raise_exception=True)

    assert serializer.data["field"] == "expected_value1"
    assert serializer.data["field_with_default"] == "default_value"

  def test_deserialize__partial_context__returns_instance(
      self,
      context_field_serializer: type[serializers.Serializer[Any]],
      mocked_model: mock.Mock,
  ) -> None:
    serializer = context_field_serializer(
        mocked_model,
        context={"context1": "expected_value1"},
    )

    assert serializer.instance == mocked_model

  def test_deserialize__missing_context__returns_none_and_default(
      self,
      context_field_serializer: type[serializers.Serializer[Any]],
  ) -> None:
    serializer = context_field_serializer(
        data={},
        context={},
    )

    serializer.is_valid(raise_exception=True)

    assert serializer.data["field"] is None
    assert serializer.data["field_with_default"] == "default_value"

  def test_deserialize__missing_context__returns_instance(
      self,
      context_field_serializer: type[serializers.Serializer[Any]],
      mocked_model: mock.Mock,
  ) -> None:
    serializer = context_field_serializer(
        mocked_model,
        context={},
    )

    assert serializer.instance == mocked_model
