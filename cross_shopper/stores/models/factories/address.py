"""Factories for building Address models."""

import random
from typing import TYPE_CHECKING

import factory

if TYPE_CHECKING:  # no cover
  from address.models import Address, Country, Locality, State  # noqa: F401
  from .typing import AliasFaker, AliasSubFactory


class CountryFactory(factory.django.DjangoModelFactory["Country"]):
  name: "AliasFaker[str]" = factory.Faker("current_country")
  code: "AliasFaker[str]" = factory.Faker("current_country_code")

  class Meta:
    model = "address.Country"
    django_get_or_create = ("name",)


class StateFactory(factory.django.DjangoModelFactory["State"]):
  name: str = random.choice(["AB", "BC", "ON"])
  country: "AliasSubFactory[CountryFactory]" = factory.SubFactory(
      CountryFactory
  )

  class Meta:
    model = "address.State"
    django_get_or_create = ("name",)


class LocalityFactory(factory.django.DjangoModelFactory["Locality"]):
  name: "AliasFaker[str]" = factory.Faker("city")
  postal_code: "AliasFaker[str]" = factory.Faker("postcode")
  state: "AliasSubFactory[StateFactory]" = factory.SubFactory(StateFactory)

  class Meta:
    model = "address.Locality"
    django_get_or_create = ("name",)


class AddressFactory(factory.django.DjangoModelFactory["Address"]):
  street_number: "AliasFaker[str]" = factory.Faker("random_digit")
  route: "AliasFaker[str]" = factory.Faker("street_name")
  locality: "AliasSubFactory[LocalityFactory]" = factory.SubFactory(
      LocalityFactory
  )
  raw: "AliasFaker[str]" = factory.Faker(provider="address")

  class Meta:
    model = "address.Address"
