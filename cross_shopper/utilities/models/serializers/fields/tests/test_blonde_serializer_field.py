"""Test the BlondeCharField serializer field."""

from typing import Any, Type
from unittest import mock

from rest_framework import serializers
from utilities.models.serializers.fields.bases.transform_base import (
    TransformCharFieldBase,
)
from utilities.models.serializers.fields.blonde import BlondeCharField
from utilities.models.serializers.fields.mixins.peroxide import (
    PeroxideFieldMixin,
)


class TestBlondeCharField:

  def test_instantiate__inheritance(self) -> None:
    assert issubclass(BlondeCharField, PeroxideFieldMixin)
    assert issubclass(BlondeCharField, TransformCharFieldBase)

  def test_deserialize__none__returns_none(
      self,
      blonde_field_serializer: Type[serializers.Serializer[Any]],
  ) -> None:
    serializer = blonde_field_serializer(data={
        "field": None,
    })
    serializer.is_valid(raise_exception=True)

    assert serializer.data["field"] is None

  def test_deserialize__sanitizes_input_data(
      self,
      blonde_field_serializer: Type[serializers.Serializer[Any]],
      mocked_input_value: str,
      mocked_sanitize: mock.Mock,
  ) -> None:
    serializer = blonde_field_serializer(data={
        "field": mocked_input_value,
    })
    serializer.is_valid(raise_exception=True)

    mocked_sanitize.assert_called_once_with(mocked_input_value)

  def test_deserialize__returns_sanitized_data(
      self,
      blonde_field_serializer: Type[serializers.Serializer[Any]],
      mocked_input_value: str,
      mocked_sanitize: mock.Mock,
  ) -> None:
    serializer = blonde_field_serializer(data={
        "field": mocked_input_value,
    })
    serializer.is_valid(raise_exception=True)

    assert serializer.data["field"] == mocked_sanitize.return_value
