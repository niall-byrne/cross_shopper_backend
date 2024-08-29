"""Factories for building Report models."""

from typing import TYPE_CHECKING, Any, Dict, List

import factory
from stores.models.factories.store import StoreFactory

if TYPE_CHECKING:  # no cover
  from django.contrib.auth.models import AbstractUser
  from items.models import Item
  from reports.models import Report, ReportStore  # noqa: F401
  from stores.models import Store
  from .typing import AliasFaker, AliasSubFactory


class ReportUserFactory(factory.django.DjangoModelFactory["AbstractUser"]):
  first_name: "AliasFaker[str]" = factory.Faker("first_name")
  last_name: "AliasFaker[str]" = factory.Faker("first_name")
  email: "AliasFaker[str]" = factory.Faker("email")

  class Meta:
    model = 'auth.User'


class ReportFactory(factory.django.DjangoModelFactory["Report"]):
  name: "AliasFaker[str]" = factory.Faker('company')
  user: "AliasSubFactory[AbstractUser]" = factory.SubFactory(ReportUserFactory)

  class Meta:
    model = 'reports.Report'

  @factory.post_generation
  def items(
      self,
      create: bool,
      extracted: List["Item"],
      **kwargs: Dict[str, Any],
  ) -> None:
    """Generate Item instances for the created Report instance."""
    if create and extracted:
      for item in extracted:
        self.item.add(item)  # type: ignore[attr-defined]

  @factory.post_generation
  def stores(
      self,
      create: bool,
      extracted: List["Store"],
      **kwargs: Dict[str, Any],
  ) -> None:
    """Generate Store instances for the created Report instance."""
    if create and extracted:
      for store in extracted:
        self.store.add(store)  # type: ignore[attr-defined]


class ReportStoreFactory(factory.django.DjangoModelFactory["ReportStore"]):
  report: "AliasSubFactory[Report]" = factory.SubFactory(ReportFactory)
  store: "AliasSubFactory[Store]" = factory.SubFactory(StoreFactory)

  class Meta:
    model = 'reports.ReportStore'
