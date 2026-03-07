"""Item admin model inlines."""

from typing import TYPE_CHECKING

from .item_attribute import ItemAttributeInline
from .item_scraper_config import ItemScraperConfigInline

if TYPE_CHECKING:  # no cover
  from typing import Any, List, Type

  from django.contrib.admin.options import InlineModelAdmin
  AliasAdminModelInlines = List[Type[InlineModelAdmin[Any, Any]]]

item_inlines: "AliasAdminModelInlines" = [
    ItemAttributeInline,
    ItemScraperConfigInline,
]
