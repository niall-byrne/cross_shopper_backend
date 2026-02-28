"""Tests for the SerializerContextField."""

from typing import Any, Dict

import pytest
from rest_framework import serializers

from ..context import SerializerContextField


class TestSerializerContextField:
  """Tests for the SerializerContextField."""

  class MockSerializer(serializers.Serializer):
    """A mock serializer for testing the field."""
    field = SerializerContextField(context_field="test_key")

  class MockDefaultSerializer(serializers.Serializer):
    """A mock serializer with a default value for the field."""
    field = SerializerContextField(
        context_field="test_key",
        default_value=lambda: "default",
    )

  def test_serialize__with_context_value__returns_value(self) -> None:
    serializer = self.MockSerializer(
        instance={},
        context={"test_key": "expected_value"},
    )
    assert serializer.data["field"] == "expected_value"

  def test_serialize__without_context_value__returns_none(self) -> None:
    serializer = self.MockSerializer(
        instance={},
        context={},
    )
    assert serializer.data["field"] is None

  def test_serialize__with_default_value__returns_default(self) -> None:
    serializer = self.MockDefaultSerializer(
        instance={},
        context={},
    )
    assert serializer.data["field"] == "default"

  def test_serialize__with_context_and_default__prefers_context(self) -> None:
    serializer = self.MockDefaultSerializer(
        instance={},
        context={"test_key": "context_value"},
    )
    assert serializer.data["field"] == "context_value"

  def test_serialize__missing_context_field__raises_exception(self) -> None:
    class InvalidSerializer(serializers.Serializer):
      field = SerializerContextField()

    serializer = InvalidSerializer(instance={})
    with pytest.raises(
        Exception, match=SerializerContextField.Messages.no_context_field
    ):
      _ = serializer.data["field"]
