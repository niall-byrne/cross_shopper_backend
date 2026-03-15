"""Model level multi-field validation."""

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from functools import reduce
from typing import TYPE_CHECKING, Generic, TypeVar

from django.core import exceptions
from django.db.models import Model
from rest_framework import exceptions as rest_framwork_exceptions

if TYPE_CHECKING:  # no cover
  from typing import (
      TYPE_CHECKING,
      Any,
      Callable,
      Mapping,
      Sequence,
      Union,
  )

  AliasOperation = Callable[[Any, str], Any]
  AliasModelOrAttr = Union[Model, Mapping[str, Any]]

ModelType = TypeVar('ModelType', bound='Model')


@dataclass
class MultiFieldValidator(ABC, Generic[ModelType]):
  """Model level multi-field validation."""

  model_fields: "Sequence[str]"

  error_message: str

  @abstractmethod
  def is_model_valid(self, instance: "ModelType") -> bool:
    """Evaluate the model validation."""

  def generate_model_error(self) -> exceptions.ValidationError:
    """Generate the interpolated validation error."""
    return exceptions.ValidationError(
        {
            field: [self.error_message.format(**asdict(self))]
            for field in self.model_fields
        }
    )

  def generate_serializer_error(
      self
  ) -> rest_framwork_exceptions.ValidationError:
    """Generate the interpolated validation error."""
    return rest_framwork_exceptions.ValidationError(
        {
            field: [self.error_message.format(**asdict(self))]
            for field in self.model_fields
        }
    )

  def model_get(
      self,
      path: str,
      model: "Model",
      path_split: str = ".",
  ) -> "Any":
    """Extract a property from a model."""
    return reduce(getattr, path.split(path_split), model)

  def deserialized_model_get(
      self,
      path: str,
      serializer_data: "Mapping[str, Any]",
      path_split: str = ".",
  ) -> "Any":
    """Extract a property from a fully or partially deserialized model."""
    return reduce(self._deserialize, path.split(path_split), serializer_data)

  def _deserialize(
      self,
      obj: "AliasModelOrAttr",
      b: "str",
  ) -> "Any":
    if isinstance(obj, Model):
      obj = obj.__dict__
    return obj[b]
