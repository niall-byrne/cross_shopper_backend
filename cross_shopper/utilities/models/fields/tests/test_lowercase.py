"""Test the LowerCaseField custom field."""

import pytest
from django.db import models
from django.test import override_settings
from ..blonde import BlondeCharField
from ..lowercase import LowerCaseField
from .conftest import AliasSetupMockModel


class TestLowerCaseField:

  def test_inheritance(
      self,
      lower_case_field_instance: LowerCaseField[str, str],
  ) -> None:
    assert isinstance(lower_case_field_instance, LowerCaseField)
    assert isinstance(lower_case_field_instance, BlondeCharField)
    assert isinstance(lower_case_field_instance, models.CharField)

  @override_settings(**{BlondeCharField.CONFIG_KEY: {}})
  @pytest.mark.parametrize("value", ["STRING1", "string2"])
  def test_pre_save__string__converts_to_lowercase(
      self,
      lower_case_field_instance: LowerCaseField[str, str],
      setup_mock_model: AliasSetupMockModel,
      value: str,
  ) -> None:

    model = setup_mock_model("field_name", value)
    lower_case_field_instance.attname = "field_name"
    lower_case_field_instance.pre_save(model, True)

    assert model.field_name == value.lower()

  @override_settings(**{BlondeCharField.CONFIG_KEY: {}})
  @pytest.mark.parametrize("value,expected", [("STRING&", "string&amp;")])
  def test_pre_save__string__converts_to_sanitized(
      self,
      lower_case_field_instance: LowerCaseField[str, str],
      setup_mock_model: AliasSetupMockModel,
      value: str,
      expected: str,
  ) -> None:

    model = setup_mock_model("field_name", value)
    lower_case_field_instance.attname = "field_name"
    lower_case_field_instance.pre_save(model, True)

    assert model.field_name == expected

  def test_pre_save__none__returns_none(
      self,
      lower_case_field_instance: LowerCaseField[None, None],
      setup_mock_model: AliasSetupMockModel,
  ) -> None:

    model = setup_mock_model("field_name", None)
    lower_case_field_instance.attname = "field_name"
    lower_case_field_instance.pre_save(model, True)

    assert model.field_name is None
