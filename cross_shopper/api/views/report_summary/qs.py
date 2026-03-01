"""Querysets for the report summary views."""

from django.db.models import QuerySet
from items.models import Item

ITEM_FIELD_ORDERING = (
    'name',
    'brand__name',
    'is_organic',
    'packaging__container',
    'packaging__quantity',
)


def qs_item() -> QuerySet[Item]:
  """Return a queryset for Item models in the report summary."""
  return Item.objects.all().order_by(*ITEM_FIELD_ORDERING)
