"""Factories for ScraperConfig model instances."""
from __future__ import annotations

from typing import TYPE_CHECKING

import factory
from scrapers.models.factories.scraper import ScraperFactory

if TYPE_CHECKING:
  from scrapers.models import Scraper, ScraperConfig  # noqa: F401
  from .typing import AliasSubFactory


class ScraperConfigFactory(factory.django.DjangoModelFactory["ScraperConfig"]):
  scraper: AliasSubFactory[Scraper] = factory.SubFactory(ScraperFactory)
  url: factory.Sequence[str] = factory.Sequence(lambda n: "/url/path/%03d" % n)

  class Meta:
    model = "scrapers.ScraperConfig"
