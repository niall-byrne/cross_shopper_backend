"""TransformCharFieldBase class."""

import abc
from abc import ABC
from typing import Any, TypeVar

from django.db import models

_ST = TypeVar("_ST")
_GT = TypeVar("_GT")


class TransformCharFieldBase(models.CharField[_ST, _GT], ABC):

  def pre_save(self, model_instance: models.Model, add: bool) -> Any:
    """Return field's value just before saving."""
    value = getattr(model_instance, self.attname)
    if isinstance(value, str):
      value = self.transform(value)
      setattr(model_instance, self.attname, value)
    return super().pre_save(model_instance, add)

  @abc.abstractmethod
  def transform(self, value: str) -> str:
    """Transform the field value into a new form."""
