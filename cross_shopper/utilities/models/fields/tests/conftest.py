"""Test fixtures for the utilities model fields."""

from typing import Callable, Optional
from unittest import mock

import pytest
from ..blonde import BlondeCharField
from ..lowercase import LowerCaseField
from ..title import TitleField

AliasSetupMockModel = Callable[[str, Optional[str]], mock.Mock]


@pytest.fixture
def setup_mock_model() -> AliasSetupMockModel:

  def setup(
      field_name: str,
      field_value: Optional[str],
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
