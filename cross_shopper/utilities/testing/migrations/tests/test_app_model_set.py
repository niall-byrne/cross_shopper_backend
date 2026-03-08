"""Tests for the AppModelSet utility."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generator

import pytest
from .scenarios import app_model_set_kwargs_scenarios, app_model_set_scenarios

if TYPE_CHECKING:
  from django_test_migrations.migrator import Migrator


class TestAppModelSet:

  @pytest.fixture(scope="function", autouse=True)
  def reset(self, migrator: Migrator) -> Generator[None, None, None]:
    yield
    migrator.reset()

  @app_model_set_scenarios
  def test_create__returns_app_model_set_with_correct_attributes(
      self,
      migrator: Migrator,
      scenario: dict[str, Any],
  ) -> None:
    klass = scenario["klass"]
    state = migrator.apply_initial_migration(
        (
            klass.module,
            scenario["migration"],
        )
    )

    model_set = klass.create(state)

    for model_name, expected_factory in scenario["models"].items():
      assert hasattr(model_set, model_name)
      assert hasattr(model_set, f"{model_name}Factory")
      assert getattr(model_set, f"{model_name}Factory") == expected_factory

  @app_model_set_scenarios
  def test_instance__returns_correct_model_instance(
      self,
      migrator: Migrator,
      scenario: dict[str, Any],
  ) -> None:
    klass = scenario["klass"]
    state = migrator.apply_initial_migration(
        (
            klass.module,
            scenario["migration"],
        )
    )

    model_set = klass.create(state)

    for model_name, expected_factory in scenario["models"].items():
      instance = model_set.instance(model_name)
      assert instance.__class__.__name__ == model_name
      assert instance._meta.model_name == (
          expected_factory._meta.model._meta.model_name
      )

  @app_model_set_kwargs_scenarios
  def test_instance__kwargs__passes_kwargs_to_instance(
      self,
      migrator: Migrator,
      scenario: dict[str, Any],
      kwargs: dict[str, Any],
  ) -> None:
    klass = scenario["klass"]
    state = migrator.apply_initial_migration(
        (
            klass.module,
            scenario["migration"],
        )
    )

    model_set = klass.create(state)
    instance = model_set.instance(scenario["model"], **kwargs)

    for attribute_name, value in kwargs.items():
      assert getattr(instance, attribute_name) == value

  @app_model_set_scenarios
  def test_instance__unique__returns_unique_model_instances(
      self,
      migrator: Migrator,
      scenario: dict[str, Any],
  ) -> None:
    klass = scenario["klass"]
    state = migrator.apply_initial_migration(
        (
            klass.module,
            scenario["migration"],
        )
    )

    model_set = klass.create(state)

    for model_name in scenario["models"].keys():
      unique_names = []
      instance = model_set.instance(model_name, name=model_set.unique)
      assert instance.name == (
          f"{model_name}.name.{model_set._sequence_counter}"
      )
      unique_names.append(instance.name)

    assert len(unique_names) == len(set(unique_names))
