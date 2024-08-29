"""Test the TitleField custom field."""

from typing import TYPE_CHECKING

import pytest
from django.db import models
from django.test import override_settings
from utilities.models.fields.blonde import BlondeCharField
from utilities.models.fields.title import TitleField

if TYPE_CHECKING:  # no cover
  from .conftest import AliasSetupMockModel


class TestTitleField:

  def test_inheritance(
      self,
      title_field_instance: TitleField[str, str],
  ) -> None:
    assert isinstance(title_field_instance, TitleField)
    assert isinstance(title_field_instance, BlondeCharField)
    assert isinstance(title_field_instance, models.CharField)

  @override_settings(**{BlondeCharField.CONFIG_KEY: {}})
  @pytest.mark.parametrize("value", ["STRING1", "string2"])
  def test_pre_save__string__converts_to_title_case(
      self,
      title_field_instance: TitleField[str, str],
      setup_mock_model: "AliasSetupMockModel",
      value: str,
  ) -> None:

    model = setup_mock_model("field_name", value)
    title_field_instance.attname = "field_name"
    title_field_instance.pre_save(model, True)

    assert model.field_name == value.capitalize()

  @override_settings(**{BlondeCharField.CONFIG_KEY: {}})
  @pytest.mark.parametrize("value,expected", [("STRING&", "String&amp;")])
  def test_pre_save__string__converts_to_sanitized(
      self,
      title_field_instance: TitleField[str, str],
      setup_mock_model: "AliasSetupMockModel",
      value: str,
      expected: str,
  ) -> None:

    model = setup_mock_model("field_name", value)
    title_field_instance.attname = "field_name"
    title_field_instance.pre_save(model, True)

    assert model.field_name == expected

  def test_pre_save__none__returns_none(
      self,
      title_field_instance: TitleField[None, None],
      setup_mock_model: "AliasSetupMockModel",
  ) -> None:

    model = setup_mock_model("field_name", None)
    title_field_instance.attname = "field_name"
    title_field_instance.pre_save(model, True)

    assert model.field_name is None
