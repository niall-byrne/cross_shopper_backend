"""Validate Item instances against their PriceGroup membership."""

from dataclasses import dataclass
from operator import attrgetter
from typing import TYPE_CHECKING

from utilities.models.validators.multi_field_validator import (
    MultiFieldValidator,
)

if TYPE_CHECKING:  # no cover
  from typing import Tuple

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
