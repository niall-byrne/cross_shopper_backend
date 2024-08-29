"""Factories for PackagingUnit model instances."""
from __future__ import annotations

from typing import TYPE_CHECKING

import factory

if TYPE_CHECKING:
  from items.models import PackagingUnit  # noqa: F401


class PackagingUnitFactory(
    factory.django.DjangoModelFactory["PackagingUnit"],
):
  name: factory.Sequence[str] = factory.Sequence(
      lambda n: "unit of measure %03d" % n
  )

  class Meta:
    model = "items.PackagingUnit"
