"""Item model."""

from django.db import models
from django.forms import ValidationError
from items import constants
from utilities.models.bases.model_base import ModelBase
from utilities.models.fields.blonde import BlondeCharField

VALIDATION_ERRORS = {
    'invalid_price_group':
        {
            'packaging':
                [
                    'The price group comparison unit must match the '
                    'packaging unit!',
                ],
            'price_group':
                [
                    'The price group comparison unit must match the '
                    'packaging unit!',
                ]
        }
}


class Item(
    ModelBase,
):

  is_non_gmo = models.BooleanField()
  is_organic = models.BooleanField()

  name = BlondeCharField(
      max_length=80,
      blank=False,
  )
  attribute = models.ManyToManyField(
      'items.Attribute',
      through='items.ItemAttribute',
  )
  brand = models.ForeignKey(
      'items.Brand',
      on_delete=models.PROTECT,
  )
  packaging = models.ForeignKey(
      'items.Packaging',
      on_delete=models.PROTECT,
  )
  price_group = models.ForeignKey(
      'items.PriceGroup',
      on_delete=models.PROTECT,
  )
  scraper_config = models.ManyToManyField(
      'scrapers.ScraperConfig',
      through='items.ItemScraperConfig',
  )

  # TODO: Consider unique together on name, attribute, brand, packaging

  def __str__(self) -> str:
    return self.name_full

  def clean(self) -> None:
    """Pre-save verification."""
    if self.is_organic:
      self.is_non_gmo = True
    if self.price_group.unit.name != self.packaging.unit.name:
      raise ValidationError(VALIDATION_ERRORS['invalid_price_group'])

  @property
  def attribute_summary(self) -> str:
    """Generate a summary of all item attributes."""
    summary = ", ".join(map(str, self.attribute.order_by('name')))
    if summary:
      return "[{}]".format(summary)
    return ''

  @property
  def is_bulk(self) -> bool:
    """Indicate whether this Item is configured with bulk packaging."""
    return self.packaging.container is None

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
    """Generate the full verbose name for this Item."""
    basename = self.name_attributed

    if self.is_organic:
      basename = " ".join([constants.ITEM_NAME_PREFIX_ORGANIC, basename])
    return ", ".join([basename, str(self.brand), str(self.packaging)])
