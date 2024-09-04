"""Test the BlondeCharField serializer field."""

from typing import Type

import pytest
from django.test import override_settings
from rest_framework import serializers
from ..blonde import BlondeCharField


class TestBlondeCharField:

  def test_deserialize__none__returns_none(
      self,
      blonde_field_serializer: Type[serializers.Serializer],
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
      blonde_field_serializer: Type[serializers.Serializer],
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
      blonde_field_serializer: Type[serializers.Serializer],
      clean: str,
      dirty: str,
  ) -> None:
    serializer = blonde_field_serializer(data={
        "field": dirty,
    })
    serializer.is_valid(raise_exception=True)

    assert serializer.data["field"] == clean
