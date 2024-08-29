"""Item admin model inlines."""

from typing import TYPE_CHECKING

from .report_store import ReportStoreInline

if TYPE_CHECKING:  # no cover
  from typing import Any, List, Type

  from django.contrib.admin.options import InlineModelAdmin

  AliasAdminModelInlines = List[Type[InlineModelAdmin[Any, Any]]]

report_inlines: "AliasAdminModelInlines" = [
    ReportStoreInline,
]
