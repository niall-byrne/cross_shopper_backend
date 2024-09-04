"""TransformCharFieldBase class."""

import abc
from abc import ABC

from rest_framework.fields import CharField


class TransformCharFieldBase(CharField, ABC):

  def to_internal_value(self, data: str) -> str:
    """Transform the field data internally using the 'transform' method."""
    data = self.transform(data)
    return super().to_internal_value(data)

  @abc.abstractmethod
  def transform(self, value: str) -> str:
    """Transform the field value into a new form."""
