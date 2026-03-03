"""Test the ModelBase class."""

from unittest import mock

import pytest
from utilities.models.bases.model_base import ModelBase


class TestModelbase:

  @pytest.mark.usefixtures("mocked_save")
  def test_initialize__save__calls_full_clean(
      self,
      concrete_model: ModelBase,
      mocked_full_clean: mock.Mock,
  ) -> None:
    concrete_model.save()

    mocked_full_clean.assert_called_once_with()

  def test_initialize__save__calls_base_class_save(
      self,
      concrete_model: ModelBase,
      mocked_save: mock.Mock,
  ) -> None:
    concrete_model.save()

    mocked_save.assert_called_once_with()

  @pytest.mark.parametrize("id", (1, 10, 100))
  def test_repr__creates_hashable_string(
      self,
      concrete_model: ModelBase,
      id: int,
  ) -> None:
    concrete_model.pk = id

    assert repr(
        concrete_model
    ) == f"{id}:{super(ModelBase, concrete_model).__repr__()}"
