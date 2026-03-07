"""A model manager for attribute assocations with items."""

from typing import TYPE_CHECKING

from django.db import models
from items.models import Item

if TYPE_CHECKING:  # no cover
  from typing import Sequence, Union

  from items.models import Attribute, ItemAttribute  # noqa: F401


class Associations(models.Manager["ItemAttribute"]):
  """A model manager for attribute assocations with items."""

  def get_items(
      self,
      attributes: "Union[models.QuerySet[Attribute], Sequence[Attribute]]",
  ) -> models.QuerySet["Item"]:
    """Return Item instances associated with the given instances."""
    attributes_ids = [attribute.pk for attribute in attributes]
    item_ids = self.get_queryset().filter(attribute__id__in=attributes_ids
                                         ).values_list("item__id", flat=True)
    return Item.objects.filter(id__in=item_ids)

  def with_items(
      self,
      attributes: models.QuerySet["Attribute"],
  ) -> models.QuerySet["Attribute"]:
    """Filter ItemAttribute instances to those associated with items."""
    item_attribute_ids = self.get_queryset().values_list(
        "attribute__id",
        flat=True,
    )
    return attributes.filter(id__in=item_attribute_ids)

  def with_no_items(
      self,
      attributes: models.QuerySet["Attribute"],
  ) -> models.QuerySet["Attribute"]:
    """Filter ItemAttribute instances to those associated with no items."""
    item_attribute_ids = self.get_queryset().values_list(
        "attribute__id",
        flat=True,
    )
    return attributes.exclude(id__in=item_attribute_ids)
