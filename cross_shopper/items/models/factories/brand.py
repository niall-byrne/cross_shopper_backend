"""Factories for Brand model instances."""

from typing import TYPE_CHECKING

import factory

if TYPE_CHECKING:  # no cover
  from items.models import Brand  # noqa: F401


class BrandFactory(factory.django.DjangoModelFactory["Brand"]):
  name: "factory.Sequence[str]" = factory.Sequence(lambda n: "Brand %03d" % n)

  class Meta:
    model = "items.Brand"
