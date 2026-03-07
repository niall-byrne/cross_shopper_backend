"""Item model."""

from django.db import models
from utilities.models.bases.model_base import ModelBase
from utilities.models.fields.blonde import BlondeCharField


class Item(
    ModelBase,
):
  NAME_PREFIX_ORGANIC = "Organic"

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
    basename = self.name
    summary = self.attribute_summary

    if summary:
      basename += " " + summary
    return basename

  @property
  def name_full(self) -> str:
    """Generate the full verbose name for this Item."""
    basename = self.name_attributed

    if self.is_organic:
      basename = " ".join([self.NAME_PREFIX_ORGANIC, basename])
    return ", ".join([basename, str(self.brand), str(self.packaging)])
