"""Helpers for the MultiFieldValidator tests."""

from dataclasses import dataclass

from django.db.models import Model
from cross_shopper.utilities.models.validators.multi_field_validator import (
    MultiFieldValidator,
)


@dataclass
class ConcreteMultiFieldValidator(MultiFieldValidator[Model]):
  """A concrete implementation of MultiFieldValidator for testing."""

  extra_info: str = "extra"

  def is_model_valid(self, instance: Model) -> bool:
    """Evaluate the model validation."""
    return True  # pragma: no cover
