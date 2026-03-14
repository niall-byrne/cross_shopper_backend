"""PriceGroup admin model inlines."""

from typing import TYPE_CHECKING

from .price_group_attribute import PriceGroupAttributeInline

if TYPE_CHECKING:  # no cover
  from typing import Any, List, Type

  from django.contrib.admin.options import InlineModelAdmin
  AliasAdminModelInlines = List[Type[InlineModelAdmin[Any, Any]]]

price_group_inlines: "AliasAdminModelInlines" = [PriceGroupAttributeInline]
