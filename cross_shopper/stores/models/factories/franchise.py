"""Factories for building stores models."""

from typing import TYPE_CHECKING

import factory
from scrapers.models.factories.scraper import ScraperFactory

if TYPE_CHECKING:  # no cover
  from scrapers.models import Scraper
  from stores.models import Franchise  # noqa: 401
  from .typing import AliasSubFactory


class FranchiseFactory(factory.django.DjangoModelFactory["Franchise"]):
  name: "factory.Sequence[str]" = factory.Sequence(
      lambda n: "Franchise %03d" % n
  )
  scraper: "AliasSubFactory[Scraper]" = factory.SubFactory(ScraperFactory)

  class Meta:
    model = 'stores.Franchise'
