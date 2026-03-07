"""Factories for Attribute model instances."""

from typing import TYPE_CHECKING

import factory

if TYPE_CHECKING:  # no cover
  from items.models import Attribute  # noqa: F401


class AttributeFactory(factory.django.DjangoModelFactory["Attribute"]):
  name: "factory.Sequence[str]" = factory.Sequence(
      lambda n: "Attribute %03d" % n,
  )

  class Meta:
    model = "items.Attribute"
