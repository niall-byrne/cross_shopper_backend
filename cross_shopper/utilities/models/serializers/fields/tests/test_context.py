"""Tests for the SerializerContextField."""

from typing import Type

import pytest
from rest_framework import serializers
from utilities.models.serializers.fields.context import SerializerContextField


class TestSerializerContextField:
  """Tests for the SerializerContextField."""

  def test_to_representation__context_key_exists__no_default__returns_context_value(
      self,
      serializer_with_context_fields: Type[serializers.Serializer],
  ) -> None:
    serializer = serializer_with_context_fields(
        data={},
        context={"test_key": "expected_value"},
    )

    assert serializer.fields["field"].to_representation(None) == "expected_value"

  def test_to_representation__context_key_exists__with_default__returns_context_value(
      self,
      serializer_with_context_fields: Type[serializers.Serializer],
  ) -> None:
    serializer = serializer_with_context_fields(
        data={},
        context={"missing_key": "provided_value"},
    )

    assert serializer.fields["field_with_default"].to_representation(
        None
    ) == "provided_value"

  def test_to_representation__missing_context_key__no_default__returns_none(
      self,
      serializer_with_context_fields: Type[serializers.Serializer],
  ) -> None:
    serializer = serializer_with_context_fields(
        data={},
        context={},
    )

    assert serializer.fields["field"].to_representation(None) is None

  def test_to_representation__missing_context_key__with_default__returns_default_value(
      self,
      serializer_with_context_fields: Type[serializers.Serializer],
  ) -> None:
    serializer = serializer_with_context_fields(
        data={},
        context={},
    )

    assert serializer.fields["field_with_default"].to_representation(
        None
    ) == "default_value"

  def test_to_representation__no_context_field_set__raises_exception(
      self,
  ) -> None:
    field = SerializerContextField()

    with pytest.raises(Exception) as excinfo:
      field.to_representation(None)

    assert str(excinfo.value) == SerializerContextField.Messages.no_context_field
