"""PriceGroup admin model PriceGroupAttribute inline."""

from django.contrib import admin
from items.models import (
    PriceGroupAttribute,
)


class PriceGroupAttributeInline(
    admin.TabularInline[PriceGroupAttribute, PriceGroupAttribute],
):
  extra = 0
  ordering = ('attribute__name',)
  model = PriceGroupAttribute
  verbose_name = 'Attributes'
  verbose_name_plural = 'Attributes'
