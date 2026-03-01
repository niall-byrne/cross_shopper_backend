"""Tests for the SerializerContextField."""

from typing import Any, Dict, Optional

import pytest
from rest_framework import serializers

from ..context import SerializerContextField


class TestSerializerContextField:
  """Tests for the SerializerContextField."""

  class MockSerializer(serializers.Serializer):
    """A mock serializer for testing the SerializerContextField."""
    field = SerializerContextField(context_field="test_key")
    field_with_default = SerializerContextField(
        context_field="missing_key",
        default_value=lambda: "default_val",
    )

  def test_to_representation__with_context_value(self) -> None:
    """Test that the field correctly extracts a value from the context."""
    serializer = self.MockSerializer(
        data={},
        context={"test_key": "expected_value"},
    )
    assert serializer.fields["field"].to_representation(None) == "expected_value"

  def test_to_representation__with_default_value(self) -> None:
    """Test that the field returns the default value if context key is missing."""
    serializer = self.MockSerializer(
        data={},
        context={},
    )
    assert serializer.fields["field_with_default"].to_representation(
        None
    ) == "default_val"

  def test_to_representation__no_context_field_raises_exception(self) -> None:
    """Test that an exception is raised if context_field is not specified."""
    field = SerializerContextField()
    with pytest.raises(Exception) as excinfo:
      field.to_representation(None)
    assert str(excinfo.value) == SerializerContextField.Messages.no_context_field

  def test_to_representation__missing_context_no_default(self) -> None:
    """Test that the field returns None if context is missing and no default."""
    serializer = self.MockSerializer(
        data={},
        context={},
    )
    assert serializer.fields["field"].to_representation(None) is None
