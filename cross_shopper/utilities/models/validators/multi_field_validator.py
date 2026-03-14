"""Model level multi-field validation."""

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING, Generic, TypeVar

from django.core import exceptions
from rest_framework import exceptions as rest_framwork_exceptions

if TYPE_CHECKING:  # no cover
  from typing import TYPE_CHECKING, Sequence

  from django.db.models import Model

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
