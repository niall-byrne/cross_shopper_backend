"""Validate PriceGroup instances against their Item instance members."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

from utilities.models.validators.multi_field_validator import (
    MultiFieldValidator,
)

if TYPE_CHECKING:  # no cover
  from typing import Tuple

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
            self.related_field:
                self.model_get(
                    self.model_fields[0],
                    price_group,
                ),
        }
    ).count() == 0
