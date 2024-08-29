"""Factories for Brand model instances."""
from __future__ import annotations

from typing import TYPE_CHECKING

import factory

if TYPE_CHECKING:
  from items.models import Brand  # noqa: F401


class BrandFactory(factory.django.DjangoModelFactory["Brand"]):
  name: factory.Sequence[str] = factory.Sequence(lambda n: "Brand %03d" % n)

  class Meta:
    model = "items.Brand"
