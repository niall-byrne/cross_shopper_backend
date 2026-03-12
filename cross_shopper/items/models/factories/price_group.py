"""Factories for PriceGroup model instances."""

from typing import TYPE_CHECKING

import factory
from items.models.factories.packaging_unit import PackagingUnitFactory

if TYPE_CHECKING:  # no cover

  from items.models import PackagingUnit, PriceGroup  # noqa: F401
  from .typing import AliasFaker, AliasSubFactory


class PriceGroupFactory(factory.django.DjangoModelFactory["PriceGroup"]):
  name: "factory.Sequence[str]" = factory.Sequence(
      lambda n: "PriceGroup %03d" % n,
  )
  quantity: "AliasFaker[int]" = factory.Faker(
      'random_int',
      min=1,
      max=1000,
  )
  unit: "AliasSubFactory[PackagingUnit]" = factory.SubFactory(
      PackagingUnitFactory
  )

  class Meta:
    model = 'items.PriceGroup'
