"""A model manager for attribute assocations with price groups."""

from typing import TYPE_CHECKING

from django.db import models
from items.models.price_group import PriceGroup

if TYPE_CHECKING:  # no cover
  from typing import Sequence, Union

  from items.models import Attribute, PriceGroupAttribute  # noqa: F401


class Associations(models.Manager["PriceGroupAttribute"]):
  """A model manager for attribute assocations with price groups."""

  def get_price_groups(
      self,
      attributes: "Union[models.QuerySet[Attribute], Sequence[Attribute]]",
  ) -> models.QuerySet["PriceGroup"]:
    """Return PriceGroup instances associated with the given instances."""
    attributes_ids = [attribute.pk for attribute in attributes]
    pg_ids = (
        self.get_queryset().filter(attribute__id__in=attributes_ids
                                  ).values_list("price_group__id", flat=True)
    )
    return PriceGroup.objects.filter(id__in=pg_ids)

  def with_price_groups(
      self,
      attributes: models.QuerySet["Attribute"],
  ) -> models.QuerySet["Attribute"]:
    """Filter instances to those associated with PriceGroups."""
    pg_attribute_ids = self.get_queryset().values_list(
        "attribute__id",
        flat=True,
    )
    return attributes.filter(id__in=pg_attribute_ids)

  def with_no_price_groups(
      self,
      attributes: models.QuerySet["Attribute"],
  ) -> models.QuerySet["Attribute"]:
    """Filter instances to those associated with no PriceGroups."""
    pg_attribute_ids = self.get_queryset().values_list(
        "attribute__id",
        flat=True,
    )
    return attributes.exclude(id__in=pg_attribute_ids)
