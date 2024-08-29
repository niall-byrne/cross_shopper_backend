"""Test fixtures for the utilities model fields."""

from typing import Callable
from unittest import mock

import pytest
from utilities.models.fields.blonde import BlondeCharField
from utilities.models.fields.lowercase import LowerCaseField
from utilities.models.fields.title import TitleField

AliasSetupMockModel = Callable[[str, str | None], mock.Mock]


@pytest.fixture
def setup_mock_model() -> AliasSetupMockModel:

  def setup(
      field_name: str,
      field_value: str | None,
  ) -> mock.Mock:
    instance = mock.Mock()
    setattr(instance, field_name, field_value)
    return instance

  return setup


@pytest.fixture
def blonde_char_field_instance() -> BlondeCharField[str, str]:
  return BlondeCharField()


@pytest.fixture
def lower_case_field_instance() -> LowerCaseField[str, str]:
  return LowerCaseField()


@pytest.fixture
def title_field_instance() -> TitleField[str, str]:
  return TitleField()
