"""Factories for building Report models."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

import factory
from api.models.factories.user import UserFactory
from stores.models.factories.store import StoreFactory

if TYPE_CHECKING:
  from django.contrib.auth.models import AbstractBaseUser
  from items.models import Item
  from reports.models import Report, ReportStore  # noqa: F401
  from stores.models import Store
  from .typing import AliasSubFactory


class ReportFactory(factory.django.DjangoModelFactory["Report"]):
  name: factory.Sequence[str] = factory.Sequence(lambda n: "Report %03d" % n)
  user: AliasSubFactory[AbstractBaseUser] = factory.SubFactory(UserFactory)

  class Meta:
    model = "reports.Report"

  @factory.post_generation
  def items(  # type: ignore[misc]
      obj: Report,
      create: bool,
      extracted: list[Item],
      **kwargs: dict[str, Any],
  ) -> None:
    """Generate Item instances for the created Report instance."""
    if create and extracted:
      for item in extracted:
        obj.item.add(item)

  @factory.post_generation
  def stores(  # type: ignore[misc]
      obj: Report,
      create: bool,
      extracted: list[Store],
      **kwargs: dict[str, Any],
  ) -> None:
    """Generate Store instances for the created Report instance."""
    if create and extracted:
      for store in extracted:
        obj.store.add(store)


class ReportStoreFactory(factory.django.DjangoModelFactory["ReportStore"]):
  report: AliasSubFactory[Report] = factory.SubFactory(ReportFactory)
  store: AliasSubFactory[Store] = factory.SubFactory(StoreFactory)

  class Meta:
    model = "reports.ReportStore"
