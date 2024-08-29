"""Item admin model inlines."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .report_store import ReportStoreInline

if TYPE_CHECKING:
  from django.contrib.admin.options import InlineModelAdmin
  AliasAdminModelInlines = list[type[InlineModelAdmin[Any, Any]]]

report_inlines: AliasAdminModelInlines = [
    ReportStoreInline,
]
