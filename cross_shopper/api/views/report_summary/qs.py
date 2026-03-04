"""Querysets for the report summary views."""

from typing import TYPE_CHECKING

from items.models import Item

if TYPE_CHECKING:  # no cover
  from django.db.models import QuerySet

REPORT_ITEM_ORDERING = (
    "name",
    "brand__name",
    "is_organic",
    "packaging__container",
    "packaging__quantity",
)


def qs_item() -> "QuerySet[Item]":
  """Return a queryset for Item models in the report summary."""
  return Item.objects.all().order_by(*REPORT_ITEM_ORDERING)
