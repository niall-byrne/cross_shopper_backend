"""Validate PriceGroup instances against their Item instance members."""

from dataclasses import dataclass
from functools import reduce
from operator import getitem
from typing import TYPE_CHECKING

from utilities.models.validators.multi_field_validator import (
    MultiFieldValidator,
)

if TYPE_CHECKING:  # no cover
  from typing import Any, Dict, Tuple

  from items.models import PriceGroup


@dataclass(kw_only=True)
class PriceGroupMemberValidator(MultiFieldValidator["PriceGroup"]):
  """Validate PriceGroup instances against their Item instance members."""

  model_fields: "Tuple[str]"
  related_field: "str"
  item_attribute: "str"
  price_group_attribute: "str"

  error_message: str = (
      'The price group {price_group_attribute} must match the item '
      '{item_attribute}.'
  )

  def is_model_valid(self, price_group: "PriceGroup") -> bool:
    """Evaluate the model validation."""
    return price_group.items.exclude(
        **{
            self.related_field: getattr(price_group, self.model_fields[0]),
        }
    ).count() == 0

  def is_serializer_valid(self, serializer_data: "Dict[str, Any]") -> bool:
    """Evaluate the serializer data validation."""
    serializer_data_value1 = reduce(
        getitem,
        ["price_group", self.model_fields[0]],
        serializer_data,
    )
    serializer_data_value2 = reduce(
        getitem,
        self.related_field.split('__'),
        serializer_data,
    )

    return serializer_data_value1 == serializer_data_value2
