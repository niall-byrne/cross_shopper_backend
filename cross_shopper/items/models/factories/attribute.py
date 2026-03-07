"""Factories for Attribute model instances."""
from __future__ import annotations

from typing import TYPE_CHECKING

import factory

if TYPE_CHECKING:
  from items.models import Attribute  # noqa: F401


class AttributeFactory(factory.django.DjangoModelFactory["Attribute"]):
  name: factory.Sequence[str] = factory.Sequence(
      lambda n: "Attribute %03d" % n,
  )

  class Meta:
    model = "items.Attribute"
