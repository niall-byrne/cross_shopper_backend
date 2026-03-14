"""PriceGroup model."""
from __future__ import annotations

from typing import TYPE_CHECKING, cast

from django.apps import apps
from django.core.validators import MaxValueValidator
from django.db import models
from items import constants
from items.models.validators.price_group import model_level_validators
from utilities.models.bases.model_base import ModelBase
from utilities.models.fields.blonde import BlondeCharField
from utilities.models.validators.greater_than_zero import (
    validator_greater_than_zero,
)

if TYPE_CHECKING:

  from django.db.models import QuerySet
  from items.models import Item


class PriceGroup(
    ModelBase,
):

  class Meta:
    unique_together = ("name", "is_non_gmo", "is_organic", "quantity", "unit")

  is_non_gmo = models.BooleanField()
  is_organic = models.BooleanField()

  name = BlondeCharField(
      max_length=80,
      blank=False,
  )
  attribute = models.ManyToManyField(
      "items.Attribute",
      through="items.PriceGroupAttribute",
  )
  quantity = models.PositiveIntegerField(
      validators=[
          validator_greater_than_zero,
          MaxValueValidator(1000),
      ]
  )
  unit = models.ForeignKey(
      "items.PackagingUnit",
      on_delete=models.PROTECT,
  )

  def __str__(self) -> str:
    return str(self.name_full)

  def clean(self) -> None:
    """Pre-save verification."""
    if self.is_organic:
      self.is_non_gmo = True

    for validator in model_level_validators:
      if not validator.is_model_valid(self):
        raise validator.generate_model_error()

  @property
  def attribute_summary(self) -> str:
    """Generate a summary of all item attributes."""
    summary = ", ".join(map(str, self.attribute.order_by("name")))
    if summary:
      return "[{}]".format(summary)
    return ""

  @property
  def has_item(self) -> bool:
    """Return a boolean if an item is associated with this group."""
    return self.items.count() != 0

  @property
  def items(self) -> QuerySet[Item]:
    """Return a the items associated with this instance."""
    ItemModel = cast(
        "Item",
        apps.get_model("items", "Item"),
    )
    if self.pk:
      return ItemModel.objects.all().filter(price_group=self)
    return ItemModel.objects.none()

  @property
  def name_attributed(self) -> str:
    """Generate the name of this Item with an attribute summary."""
    basename = str(self.name)
    summary = self.attribute_summary

    if summary:
      basename += " " + summary
    return basename

  @property
  def name_full(self) -> str:
    """Generate the full verbose name for this PriceGroup."""
    basename = self.name_attributed

    measure = f"{self.quantity}{self.unit}"
    if self.quantity == 1:
      measure = f"{self.unit}"

    if self.is_organic:
      basename = " ".join([constants.ITEM_NAME_PREFIX_ORGANIC, basename])
    elif self.is_non_gmo:
      basename = " ".join([constants.ITEM_NAME_PREFIX_NON_GMO, basename])

    return f"{basename} per {measure}"
