"""Test the BlondeCharField custom field."""

from typing import TYPE_CHECKING

import pytest
from django.test import override_settings
from django_bleach.models import BleachField
from utilities.models.fields.blonde import BlondeCharField

if TYPE_CHECKING:  # no cover
  from .conftest import AliasSetupMockModel


class TestBlondeCharField:

  def test_inheritance(
      self,
      blonde_char_field_instance: BlondeCharField[str, str],
  ) -> None:
    assert isinstance(blonde_char_field_instance, BlondeCharField)
    assert isinstance(blonde_char_field_instance, BleachField)

  @override_settings(**{BlondeCharField.CONFIG_KEY: {}})
  @pytest.mark.parametrize(
      "value,expected", [
          ("Initial&Value", "Initial&amp;Value"),
      ]
  )
  def test_pre_save__string__no_restore_config__converts_to_sanitized(
      self,
      blonde_char_field_instance: BlondeCharField[str, str],
      setup_mock_model: "AliasSetupMockModel",
      value: str,
      expected: str,
  ) -> None:

    model = setup_mock_model("field_name", value)
    blonde_char_field_instance.attname = "field_name"
    blonde_char_field_instance.pre_save(model, True)

    assert model.field_name == expected

  @override_settings(**{BlondeCharField.CONFIG_KEY: {"&amp;": "&"}})
  @pytest.mark.parametrize(
      "value,expected", [
          ("Initial&Value", "Initial&Value"),
      ]
  )
  def test_pre_save__string__with_restore_config__restores_sanitized_value(
      self,
      blonde_char_field_instance: BlondeCharField[str, str],
      setup_mock_model: "AliasSetupMockModel",
      value: str,
      expected: str,
  ) -> None:

    model = setup_mock_model("field_name", value)
    blonde_char_field_instance.attname = "field_name"
    blonde_char_field_instance.pre_save(model, True)

    assert model.field_name == expected

  def test_pre_save__none__returns_none(
      self,
      setup_mock_model: "AliasSetupMockModel",
      blonde_char_field_instance: BlondeCharField[None, None],
  ) -> None:

    model = setup_mock_model("field_name", None)
    blonde_char_field_instance.attname = "field_name"
    blonde_char_field_instance.pre_save(model, True)

    assert model.field_name is None
