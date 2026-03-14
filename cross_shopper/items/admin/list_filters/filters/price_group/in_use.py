"""A list filter for tracking Item models related to PriceGroup models."""

from typing import TYPE_CHECKING

from items.models import Item
from utilities.admin.list_filters import GenericListFilter

if TYPE_CHECKING:  # no cover
  from django.db import models
  from django.http import HttpRequest
  from items.models import PriceGroup


class InUseFilter(GenericListFilter):
  title = "in use"
  parameter_name = "has_item"
  is_boolean = True

  def queryset(
      self,
      request: "HttpRequest",
      queryset: "models.QuerySet[PriceGroup]",
  ) -> "models.QuerySet[PriceGroup]":
    """Generate a list of filter tuples from the configured query set."""
    if self.value() == "True":
      item_ids = Item.objects.exclude(price_group=None).values_list(
          "price_group__pk",
          flat=True,
      )
      queryset = queryset.filter(pk__in=item_ids)
    if self.value() == "False":
      item_ids = Item.objects.exclude(price_group=None).values_list(
          "price_group__pk",
          flat=True,
      )
      queryset = queryset.exclude(pk__in=item_ids)
    return queryset
