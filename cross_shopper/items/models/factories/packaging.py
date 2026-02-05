"""Factories for Packaging model instances."""

from typing import TYPE_CHECKING

import factory
from items.models.factories.packaging_container import PackagingContainerFactory
from items.models.factories.packaging_unit import PackagingUnitFactory

if TYPE_CHECKING:  # no cover
  from decimal import Decimal

  from items.models import (  # noqa: F401
    Packaging,
    PackagingContainer,
    PackagingUnit,
  )
  from .typing import AliasFaker, AliasSubFactory


class PackagingFactory(factory.django.DjangoModelFactory["Packaging"]):
  quantity: "AliasFaker[Decimal]" = factory.Faker(
      'pydecimal',
      left_digits=4,
      right_digits=2,
      min_value=1,
  )
  container: "AliasSubFactory[PackagingContainer]" = factory.SubFactory(
      PackagingContainerFactory
  )
  unit: "AliasSubFactory[PackagingUnit]" = factory.SubFactory(
      PackagingUnitFactory
  )

  class Meta:
    model = 'items.Packaging'
