"""Item admin model inlines."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .item_attribute import ItemAttributeInline
from .item_scraper_config import ItemScraperConfigInline

if TYPE_CHECKING:
  from django.contrib.admin.options import InlineModelAdmin
  AliasAdminModelInlines = list[type[InlineModelAdmin[Any, Any]]]

item_inlines: AliasAdminModelInlines = [
    ItemAttributeInline,
    ItemScraperConfigInline,
]
