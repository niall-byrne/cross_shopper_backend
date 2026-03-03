"""Test fixtures for the utilities model base classes."""

from unittest import mock

import pytest
from django.db import models
from utilities.models.bases.model_base import ModelBase


class ConcreteModel(ModelBase):
  pass

  class Meta:
    managed = False


@pytest.fixture
def mocked_full_clean() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_save() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def concrete_model(
    mocked_full_clean: mock.Mock,
    mocked_save: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> ModelBase:
  monkeypatch.setattr(models.Model, "full_clean", mocked_full_clean)
  monkeypatch.setattr(models.Model, "save", mocked_save)

  return ConcreteModel()
