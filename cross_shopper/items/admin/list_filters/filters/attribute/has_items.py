"""A list filter for tracking Item models related to Attribute models."""

from typing import TYPE_CHECKING

from items.models import ItemAttribute
from utilities.admin.list_filters import GenericListFilter

if TYPE_CHECKING:  # no cover
  from django.db import models
  from django.http import HttpRequest
  from items.models import Attribute


class HasItemsFilter(GenericListFilter):
  title = 'has items'
  parameter_name = 'has_item'
  is_boolean = True

  def queryset(
      self,
      request: "HttpRequest",
      queryset: "models.QuerySet[Attribute]",
  ) -> "models.QuerySet[Attribute]":
    """Generate a list of filter tuples from the configured query set."""
    if self.value() == 'True':
      return ItemAttribute.associations.with_items(queryset)
    if self.value() == 'False':
      return ItemAttribute.associations.with_no_items(queryset)
    return queryset
