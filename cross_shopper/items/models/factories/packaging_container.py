"""Factories for PackagingContainer model instances."""

from typing import TYPE_CHECKING

import factory

if TYPE_CHECKING:  # no cover
  from items.models import PackagingContainer  # noqa: F401


class PackagingContainerFactory(
    factory.django.DjangoModelFactory["PackagingContainer"],
):
  name: "factory.Sequence[str]" = factory.Sequence(
      lambda n: "storage container %03d" % n
  )

  class Meta:
    model = "items.PackagingContainer"
