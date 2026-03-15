"""Validate Item instances against their PriceGroup membership."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

from utilities.models.validators.multi_field_validator import (
    MultiFieldValidator,
)

if TYPE_CHECKING:  # no cover
  from typing import Any, Callable, Mapping, Tuple, Union

  from django.db.models import Model
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
    attr1 = self.get_attr(
        item,
        self.comparison[0],
    )
    attr2 = self.get_attr(
        item,
        self.comparison[1],
    )

    return bool(attr1 == attr2)

  def is_serializer_valid(self, serialized_data: "Mapping[str, Any]") -> bool:
    """Evaluate the serializer data validation."""
    value1 = self.get_attr(
        serialized_data,
        self.comparison[0],
    )
    value2 = self.get_attr(
        serialized_data,
        self.comparison[1],
    )

    return bool(value1 == value2)
