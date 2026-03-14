"""PriceGroup admin model inlines."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .item import PriceGroupItemInline
from .price_group_attribute import PriceGroupAttributeInline

if TYPE_CHECKING:
  from django.contrib.admin.options import InlineModelAdmin
  AliasAdminModelInlines = list[type[InlineModelAdmin[Any, Any]]]

price_group_inlines: AliasAdminModelInlines = [
    PriceGroupAttributeInline,
    PriceGroupItemInline,
]
