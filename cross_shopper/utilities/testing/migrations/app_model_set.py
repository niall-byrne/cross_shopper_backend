"""App model accessor set for migration tests."""

import importlib
import re
from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, ClassVar

import factory

if TYPE_CHECKING:
  from typing import Any, Dict, Type, TypeVar

  from django.db.migrations.state import ProjectState
  from django.db.models import Model
  AppModelSetType = TypeVar("AppModelSetType", bound="AppModelSet")


@dataclass
class AppModelSet:
  """A set of model accessors for a specific app during migration tests."""

  module: ClassVar[str]

  # Note: FactoryBoy sequences don't persist via the factory.create method.
  #       Use this counter and self.unique to manage this.
  _sequence_counter: int = field(init=False, repr=False, default=0)

  @classmethod
  def create(
      cls: "Type[AppModelSetType]",
      state: "ProjectState",
  ) -> "AppModelSetType":
    """Create an app model set for the specified state."""

    kwargs: "Dict[str, Any]" = {}
    for field in fields(cls):
      if field.name == '_sequence_counter':
        continue

      kwargs[field.name] = state.apps.get_model(
          cls.module,
          field.name,
      )

      factory_module = importlib.import_module(
          f"{cls.module}.models.factories.{cls._as_module_name(field.name)}"
      )

      setattr(
          cls,
          f"{field.name}Factory",
          getattr(factory_module, f"{field.name}Factory"),
      )

    return cls(**kwargs)

  @classmethod
  def _as_module_name(cls, class_name: str) -> str:
    dotted = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', class_name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', dotted).lower()

  def instance(self, model_name: "str", **kwargs: "Any") -> "Any":
    """Generates an instance of the specified model name."""

    for key, value in kwargs.items():
      if value == self.unique:
        kwargs[key] = f"{model_name}.{key}.{self.unique()}"

    factory_class = getattr(self, f"{model_name}Factory")

    return factory.create(
        getattr(self, model_name),
        FACTORY_CLASS=factory_class,
        **kwargs,
    )

  def unique(self) -> int:
    """Generates a unique identifier in lieu of FactoryBoy sequences."""

    self._sequence_counter += 1
    return self._sequence_counter
