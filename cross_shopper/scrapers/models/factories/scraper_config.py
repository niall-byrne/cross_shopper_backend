"""Factories for ScraperConfig model instances."""

from typing import TYPE_CHECKING

import factory
from scrapers.models.factories.scraper import ScraperFactory

if TYPE_CHECKING:  # no cover
  from scrapers.models import Scraper, ScraperConfig  # noqa: F401
  from .typing import AliasFaker, AliasSubFactory


class ScraperConfigFactory(factory.django.DjangoModelFactory["ScraperConfig"]):
  scraper: "AliasSubFactory[Scraper]" = factory.SubFactory(
      ScraperFactory,
      url_validation_regex=factory.SelfAttribute("..url"),
  )
  url: "AliasFaker[str]" = factory.Faker("url")

  class Meta:
    model = 'scrapers.ScraperConfig'
