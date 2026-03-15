"""Generate batches of models with unique constraints."""
from typing import (
  TYPE_CHECKING,
  Any,
  Callable,
  Dict,
  List,
  Tuple,
  Type,
  TypedDict,
  TypeVar,
)

from django.db.models import Model

if TYPE_CHECKING:  # no cover
  from factory.django import DjangoModelFactory

ModelType = TypeVar('ModelType', bound=Model)


class ConstraintDefinition(TypedDict):
  field_name: str
  fn: Callable[[Any], Any]


class UniqueTogetherModelBatchFactory:
  """Creates a batch of model instances with unique together constraints."""

  def __init__(
      self,
      model_factory: Type['DjangoModelFactory[ModelType]'],
      unique_together_constraint: Tuple[ConstraintDefinition, ...],
      **kwargs: Any,
  ) -> None:
    self.factory = model_factory
    self.constraints = unique_together_constraint
    self.creation_keywords = kwargs

  def create_batch(
      self,
      batch_size: int,
      **kwargs: Any,
  ) -> List['ModelType']:
    """Create a batch of constrained models with the given batch size."""
    value_sets: List[Dict[Any, Any]] = []
    batch: List['ModelType'] = []

    while len(batch) < batch_size:
      generated_value_set: Dict[Any, Any] = {}

      left_most_constraint_value = self.constraints[0]['fn'](len(batch))
      generated_value_set[self.constraints[0]['field_name']] = \
          left_most_constraint_value

      for constraint_definition in self.constraints[1:]:
        next_constraint_value = constraint_definition['fn'](len(batch))
        generated_value_set[constraint_definition['field_name']] = \
            next_constraint_value

      if generated_value_set not in value_sets:
        value_sets.append(generated_value_set)
        batch.append(
            self.factory.create(
                **self.creation_keywords,
                **kwargs,
                **generated_value_set,
            )
        )

    return batch
