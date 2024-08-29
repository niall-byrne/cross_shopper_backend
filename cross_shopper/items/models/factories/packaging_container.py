"""Factories for PackagingContainer model instances."""
from __future__ import annotations

from typing import TYPE_CHECKING

import factory

if TYPE_CHECKING:
  from items.models import PackagingContainer  # noqa: F401


class PackagingContainerFactory(
    factory.django.DjangoModelFactory["PackagingContainer"],
):
  name: factory.Sequence[str] = factory.Sequence(
      lambda n: "storage container %03d" % n
  )

  class Meta:
    model = "items.PackagingContainer"
