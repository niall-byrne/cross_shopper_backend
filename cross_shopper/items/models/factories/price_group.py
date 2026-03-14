"""Factories for PriceGroup model instances."""

from typing import TYPE_CHECKING

import factory
from items.models.factories.packaging_unit import PackagingUnitFactory

if TYPE_CHECKING:  # no cover
  from typing import Any, Dict, List

  from items.models import Attribute, PackagingUnit, PriceGroup  # noqa: F401
  from .typing import AliasFaker, AliasSubFactory


class PriceGroupFactory(factory.django.DjangoModelFactory["PriceGroup"]):
  is_non_gmo: "AliasFaker[bool]" = factory.Faker("boolean")
  is_organic: "AliasFaker[bool]" = factory.Faker("boolean")
  name: "factory.Sequence[str]" = factory.Sequence(
      lambda n: "PriceGroup %03d" % n,
  )
  quantity: "AliasFaker[int]" = factory.Faker(
      "random_int",
      min=1,
      max=1000,
  )
  unit: "AliasSubFactory[PackagingUnit]" = factory.SubFactory(
      PackagingUnitFactory
  )

  class Meta:
    model = "items.PriceGroup"

  @factory.post_generation
  def attributes(  # type: ignore[misc]
    obj: "PriceGroup",
    create: bool,
    extracted: "List[Attribute]",
    **kwargs: "Dict[str, Any]",
  ) -> None:
    """Generate Attribute instances for the created PriceGroup instance."""
    if create and extracted:
      for attribue in extracted:
        obj.attribute.add(attribue)
