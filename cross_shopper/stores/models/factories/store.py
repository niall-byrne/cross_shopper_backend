"""Factories for building stores models."""

from typing import TYPE_CHECKING

import factory
from stores.models.factories.address import AddressFactory
from stores.models.factories.franchise import FranchiseFactory

if TYPE_CHECKING:  # no cover
  from address.models import Address
  from stores.models import Franchise, Store  # noqa: F401
  from .typing import AliasFaker, AliasSubFactory


class StoreFactory(factory.django.DjangoModelFactory["Store"]):
  address: "AliasSubFactory[Address]" = factory.SubFactory(AddressFactory)
  franchise: "AliasSubFactory[Franchise]" = factory.SubFactory(FranchiseFactory)
  franchise_location: "AliasFaker[str]" = factory.Faker("sentence", nb_words=2)

  class Meta:
    model = 'stores.Store'
