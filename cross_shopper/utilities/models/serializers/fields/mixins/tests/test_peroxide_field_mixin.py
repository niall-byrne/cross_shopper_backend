"""Tests for the PeroxideFieldMixin class."""
from __future__ import annotations

import pytest
from django.test import override_settings
from utilities.models.serializers.fields.mixins.peroxide import (
    PeroxideFieldMixin,
)


class TestPeroxideFieldMixin:

  @pytest.mark.parametrize(
      "bleach_scenario", [
          {
              "clean": "simple string",
              "dirty": "simple string"
          },
          {
              "clean": "simple string",
              "dirty": "simple <a>string</a>"
          },
          {
              "clean": "simple &amp; string",
              "dirty": "simple & string"
          },
          {
              "clean": "",
              "dirty": None,
          },
      ]
  )
  @override_settings(**{PeroxideFieldMixin.CONFIG_KEY: {}})
  def test_sanitize__vary_data__no_overrides__cleans_input_data(
      self,
      peroxide_field_mixin: PeroxideFieldMixin,
      bleach_scenario: dict[str, str | None],
  ) -> None:
    sanitized_value = peroxide_field_mixin.sanitize(bleach_scenario["dirty"])

    assert sanitized_value == bleach_scenario["clean"]

  @pytest.mark.parametrize(
      "bleach_scenario", [
          {
              "clean": "simple string",
              "dirty": "simple string"
          },
          {
              "clean": "simple string",
              "dirty": "simple <a>string</a>"
          },
          {
              "clean": "simple & string",
              "dirty": "simple & string"
          },
          {
              "clean": "",
              "dirty": None,
          },
      ]
  )
  @override_settings(**{PeroxideFieldMixin.CONFIG_KEY: {"&amp;": "&"}})
  def test_sanitize__vary_data__with_overrides__cleans_input_data(
      self,
      peroxide_field_mixin: PeroxideFieldMixin,
      bleach_scenario: dict[str, str | None],
  ) -> None:
    sanitized_value = peroxide_field_mixin.sanitize(bleach_scenario["dirty"])

    assert sanitized_value == bleach_scenario["clean"]
