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
  brand = models.ForeignKey(
      "items.Brand",
      on_delete=models.PROTECT,
  )
  packaging = models.ForeignKey(
      "items.Packaging",
      on_delete=models.PROTECT,
  )
  scraper_config = models.ManyToManyField(
      "scrapers.ScraperConfig",
      through="items.ItemScraperConfig",
  )

  def __str__(self) -> str:
    return self.full_name

  def clean(self) -> None:
    """Pre-save verification."""
    if self.is_organic:
      self.is_non_gmo = True

  @property
  def full_name(self) -> str:
    """Generate verbose descriptive name for this Item."""
    base_name = str(self.name)
    if self.is_organic:
      base_name = " ".join([self.NAME_PREFIX_ORGANIC, base_name])
    return ", ".join([base_name, str(self.brand), str(self.packaging)])

  @property
  def is_bulk(self) -> bool:
    """Indicate whether this Item is configured with bulk packaging."""
    return self.packaging.container is None
