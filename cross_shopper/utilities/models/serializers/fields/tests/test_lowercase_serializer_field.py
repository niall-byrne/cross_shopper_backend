"""Test the LowerCaseField serializer field."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest
from django.test import override_settings
from utilities.models.serializers.fields.lowercase import LowerCaseField

if TYPE_CHECKING:
  from rest_framework import serializers


class TestLowerCaseField:

  @pytest.mark.parametrize(
      "clean,dirty", [
          ("simple string", "simple STRING"),
          ("simple string", "SIMPLE <a>STRING</a>"),
          ("simple &amp; string", "SIMPLE & string"),
      ]
  )
  @override_settings(**{LowerCaseField.CONFIG_KEY: {}})
  def test_deserialize__no_overrides__transforms_and_cleans_data(
      self,
      lowercase_field_serializer: type[serializers.Serializer[Any]],
      clean: str,
      dirty: str,
  ) -> None:
    serializer = lowercase_field_serializer(data={
        "field": dirty,
    })
    serializer.is_valid(raise_exception=True)

    assert serializer.data["field"] == clean

  @pytest.mark.parametrize(
      "clean,dirty", [
          ("simple string", "simple STRING"),
          ("simple string", "SIMPLE <a>STRING</a>"),
          ("simple & string", "SIMPLE & string"),
      ]
  )
  @override_settings(**{LowerCaseField.CONFIG_KEY: {"&amp;": "&"}})
  def test_deserialize__with_overrides__transforms_and_cleans_data(
      self,
      lowercase_field_serializer: type[serializers.Serializer[Any]],
      clean: str,
      dirty: str,
  ) -> None:
    serializer = lowercase_field_serializer(data={
        "field": dirty,
    })
    serializer.is_valid(raise_exception=True)

    assert serializer.data["field"] == clean
