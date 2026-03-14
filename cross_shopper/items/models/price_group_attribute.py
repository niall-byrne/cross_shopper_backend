"""PriceGroupAttribute model."""

from django.db import models
from items.models.managers.price_group_attribute.association import Associations
from utilities.models.bases.model_base import ModelBase


class PriceGroupAttribute(
    ModelBase,
):
  price_group = models.ForeignKey(
      'items.PriceGroup',
      on_delete=models.CASCADE,
  )
  attribute = models.ForeignKey(
      'items.Attribute',
      on_delete=models.CASCADE,
  )

  associations = Associations()
  objects = models.Manager()

  class Meta:
    unique_together = ('price_group', 'attribute')

  def __str__(self) -> str:
    return f"{self.price_group.name} - {self.attribute}"
