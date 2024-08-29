"""Store model."""

from address.models import AddressField
from django.db import models
from utilities.models.bases.base_model import BaseModel
from utilities.models.fields.blonde import BlondeCharField


class Store(
    BaseModel,
):
  """Store model."""

  class Meta:
    unique_together = ('franchise', 'franchise_location')

  address = AddressField(on_delete=models.PROTECT)
  franchise = models.ForeignKey(
      'stores.Franchise',
      on_delete=models.PROTECT,
  )
  franchise_location = BlondeCharField(
      max_length=80,
      blank=False,
  )

  def __str__(self) -> str:
    return f"{str(self.franchise.name)}: {self.address}"
