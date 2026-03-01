"""Tests for the SerializerContextField."""

from typing import Type

import pytest
from rest_framework import serializers

from ..context import SerializerContextField


class TestSerializerContextField:
  """Tests for the SerializerContextField."""

  def test_to_representation__context_value_exists__correct_representation(
      self,
      context_field_serializer: Type[serializers.Serializer],
  ) -> None:
    serializer = context_field_serializer(
        data={},
        context={"test_key": "expected_value"},
    )

    assert serializer.fields["field"].to_representation(None) == "expected_value"

  def test_to_representation__missing_context__default_value_returned(
      self,
      context_field_serializer: Type[serializers.Serializer],
  ) -> None:
    serializer = context_field_serializer(
        data={},
        context={},
    )

    assert serializer.fields["field_with_default"].to_representation(
        None
    ) == "default_val"

  def test_to_representation__no_context_field__raises_exception(
      self,
  ) -> None:
    field = SerializerContextField()

    with pytest.raises(Exception) as excinfo:
      field.to_representation(None)

    assert str(excinfo.value) == SerializerContextField.Messages.no_context_field

  def test_to_representation__missing_context_no_default__none_returned(
      self,
      context_field_serializer: Type[serializers.Serializer],
  ) -> None:
    serializer = context_field_serializer(
        data={},
        context={},
    )

    assert serializer.fields["field"].to_representation(None) is None
