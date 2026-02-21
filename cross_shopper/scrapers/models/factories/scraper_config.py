"""Factories for ScraperConfig model instances."""

from typing import TYPE_CHECKING

import factory
from scrapers.models.factories.scraper import ScraperFactory

if TYPE_CHECKING:  # no cover
  from scrapers.models import Scraper, ScraperConfig  # noqa: F401
  from .typing import AliasFaker, AliasSubFactory


class ScraperConfigFactory(factory.django.DjangoModelFactory["ScraperConfig"]):
  is_active: "AliasFaker[bool]" = factory.Faker("pybool")
  scraper: "AliasSubFactory[Scraper]" = factory.SubFactory(ScraperFactory)
  url: "factory.Sequence[str]" = factory.Sequence(
      lambda n: "/url/path/%03d" % n
  )

  class Meta:
    model = 'scrapers.ScraperConfig'
