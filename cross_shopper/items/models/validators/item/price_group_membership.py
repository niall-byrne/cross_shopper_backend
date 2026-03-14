"""Validate Item instances against their PriceGroup membership."""

from dataclasses import dataclass
from functools import reduce
from operator import attrgetter
from typing import TYPE_CHECKING

from django.db.models import Model
from utilities.models.validators.multi_field_validator import (
    MultiFieldValidator,
)

if TYPE_CHECKING:  # no cover
  from typing import Any, Mapping, Tuple, Union

  from items.models import Item


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
    attr1 = attrgetter(self.comparison[0])(item)
    attr2 = attrgetter(self.comparison[1])(item)

    return bool(attr1 != attr2)

  def is_serializer_valid(self, serializer_data: "Mapping[str, Any]") -> bool:
    """Evaluate the serializer data validation."""
    serializer_data_value1 = reduce(
        self._serialize,
        self.comparison[0].split('.'),
        serializer_data,
    )
    serializer_data_value2 = reduce(
        self._serialize,
        self.comparison[1].split('.'),
        serializer_data,
    )

    return serializer_data_value1 == serializer_data_value2

  def _serialize(
      self,
      obj: "Union[Model, Mapping[str, Any]]",
      b: "str",
  ) -> "Any":
    if isinstance(obj, Model):
      obj = obj.__dict__
    return obj[b]
