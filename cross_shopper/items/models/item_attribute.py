"""ItemAttribute model."""

from django.db import models
from items.models.managers.item_attribute.association import Associations
from utilities.models.bases.model_base import ModelBase


class ItemAttribute(
    ModelBase,
):
  item = models.ForeignKey(
      'items.Item',
      on_delete=models.CASCADE,
  )
  attribute = models.ForeignKey(
      'items.Attribute',
      on_delete=models.CASCADE,
  )

  associations = Associations()
  objects = models.Manager()

  class Meta:
    unique_together = ('item', 'attribute')

  def __str__(self) -> str:
    return f"{self.item.name} - {self.attribute}"
