"""Item admin model ItemAttribute inline."""

from django.contrib import admin
from items.models import (
    ItemAttribute,
)


class ItemAttributeInline(
    admin.TabularInline[ItemAttribute, ItemAttribute],
):
  extra = 0
  ordering = ('attribute__name',)
  model = ItemAttribute
  verbose_name = 'Attributes'
  verbose_name_plural = 'Attributes'
