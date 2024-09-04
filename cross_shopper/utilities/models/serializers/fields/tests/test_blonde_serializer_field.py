"""Test the BlondeCharField serializer field."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest
from django.test import override_settings
from utilities.models.serializers.fields.blonde import BlondeCharField

if TYPE_CHECKING:
  from rest_framework import serializers


class TestBlondeCharField:

  def test_deserialize__none__returns_none(
      self,
      blonde_field_serializer: type[serializers.Serializer[Any]],
  ) -> None:
    serializer = blonde_field_serializer(data={
        "field": None,
    })
    serializer.is_valid(raise_exception=True)

    assert serializer.data["field"] is None

  @pytest.mark.parametrize(
      "clean,dirty", [
          ("simple string", "simple string"),
          ("simple string", "simple <a>string</a>"),
          ("simple &amp; string", "simple & string"),
      ]
  )
  @override_settings(**{BlondeCharField.CONFIG_KEY: {}})
  def test_deserialize__no_overrides__cleans_data(
      self,
      blonde_field_serializer: type[serializers.Serializer[Any]],
      clean: str,
      dirty: str,
  ) -> None:
    serializer = blonde_field_serializer(data={
        "field": dirty,
    })
    serializer.is_valid(raise_exception=True)

    assert serializer.data["field"] == clean

  @pytest.mark.parametrize(
      "clean,dirty", [
          ("simple string", "simple string"),
          ("simple string", "simple <a>string</a>"),
          ("simple & string", "simple & string"),
      ]
  )
  @override_settings(**{BlondeCharField.CONFIG_KEY: {"&amp;": "&"}})
  def test_deserialize__with_overrides__cleans_data(
      self,
      blonde_field_serializer: type[serializers.Serializer[Any]],
      clean: str,
      dirty: str,
  ) -> None:
    serializer = blonde_field_serializer(data={
        "field": dirty,
    })
    serializer.is_valid(raise_exception=True)

    assert serializer.data["field"] == clean
