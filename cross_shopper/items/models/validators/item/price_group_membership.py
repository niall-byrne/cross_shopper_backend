"""Validate Item instances against their PriceGroup membership."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

from django.db.models import Model
from utilities.models.validators.multi_field_validator import (
    MultiFieldValidator,
)

if TYPE_CHECKING:  # no cover
  from typing import Any, Callable, Mapping, Tuple, Union

  from items.models import Item
  AliasOperation = Callable[[Any, str], Any]
  AliasModelOrAttr = Union[Model, Mapping[str, Any]]


@dataclass(kw_only=True)
class ItemPriceGroupMembershipValidator(MultiFieldValidator["Item"]):
  """Validate Item instances against their PriceGroup membership."""

  comparison: "Tuple[str, str]"
  item_attribute: "str"
  price_group_attribute: "str"

  error_message: str = (
      'The price group {price_group_attribute} must match the '
      'item {item_attribute}.'
  )

  def is_model_valid(self, item: "Item") -> bool:
    """Evaluate the validation."""
    attr1 = self.model_get(
        self.comparison[0],
        item,
    )
    attr2 = self.model_get(
        self.comparison[1],
        item,
    )

    return bool(attr1 == attr2)

  def is_serializer_valid(self, serializer_data: "Mapping[str, Any]") -> bool:
    """Evaluate the serializer data validation."""
    value1 = self.deserialized_model_get(
        self.comparison[0],
        serializer_data,
    )
    value2 = self.deserialized_model_get(
        self.comparison[1],
        serializer_data,
    )

    return bool(value1 == value2)
