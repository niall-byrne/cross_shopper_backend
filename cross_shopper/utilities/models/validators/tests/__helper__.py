"""Helper for testing MultiFieldValidator."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

from utilities.models.validators.multi_field_validator import MultiFieldValidator

if TYPE_CHECKING:
  from django.db.models import Model


@dataclass
class ConcreteMultiFieldValidator(MultiFieldValidator["Model"]):
  """Concrete implementation of MultiFieldValidator for testing."""

  def is_model_valid(self, instance: "Model") -> bool:
    """Evaluate the model validation."""
    return getattr(instance, "is_valid", True)
