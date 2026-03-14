"""PriceGroup admin model PriceGroupAttribute inline."""

from django.contrib import admin
from items.models import PriceGroupAttribute
from items.models.price_group import PriceGroup


class PriceGroupAttributeInline(
    admin.TabularInline[PriceGroupAttribute, PriceGroup],
):
  extra = 0
  ordering = ("attribute__name",)
  model = PriceGroupAttribute
  verbose_name = "Attribute"
  verbose_name_plural = "Attributes"
