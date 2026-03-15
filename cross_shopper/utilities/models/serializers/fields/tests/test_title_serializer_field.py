"""Test the TitleField serializer field."""

from typing import TYPE_CHECKING, Any, Type

import pytest
from django.test import override_settings
from utilities.models.serializers.fields.title import TitleField
from utilities.strings.tests.scenarios import title_string_scenarios

if TYPE_CHECKING:  # no cover
  from rest_framework import serializers


class TestTitleField:

  @title_string_scenarios
  def test_deserialize__transforms_to_title_value(
      self,
      title_field_serializer: Type["serializers.Serializer[Any]"],
      input_string: str,
      expected_string: str,
  ) -> None:
    serializer = title_field_serializer(data={
        "field": input_string,
    })
    serializer.is_valid(raise_exception=True)

    assert serializer.data["field"] == expected_string.strip()

  @pytest.mark.parametrize(
      "clean,dirty", [
          ("Simple STRING", "simple STRING"),
          ("SIMPLE STRING", "SIMPLE <a>STRING</a>"),
          ("SIMPLE &amp; String", "SIMPLE & String"),
      ]
  )
  @override_settings(**{TitleField.CONFIG_KEY: {}})
  def test_deserialize__no_overrides__transforms_and_cleans_data(
      self,
      title_field_serializer: Type["serializers.Serializer[Any]"],
      clean: str,
      dirty: str,
  ) -> None:
    serializer = title_field_serializer(data={
        "field": dirty,
    })
    serializer.is_valid(raise_exception=True)

    assert serializer.data["field"] == clean

  @pytest.mark.parametrize(
      "clean,dirty", [
          ("Simple STRING", "simple STRING"),
          ("SIMPLE STRING", "SIMPLE <a>STRING</a>"),
          ("SIMPLE & String", "SIMPLE & string"),
      ]
  )
  @override_settings(**{TitleField.CONFIG_KEY: {"&amp;": "&"}})
  def test_deserialize__with_overrides__transforms_and_cleans_data(
      self,
      title_field_serializer: Type["serializers.Serializer[Any]"],
      clean: str,
      dirty: str,
  ) -> None:
    serializer = title_field_serializer(data={
        "field": dirty,
    })
    serializer.is_valid(raise_exception=True)

    assert serializer.data["field"] == clean
