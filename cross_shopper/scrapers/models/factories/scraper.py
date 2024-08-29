"""Factories for Scraper model instances."""

from typing import TYPE_CHECKING

import factory

if TYPE_CHECKING:  # no cover
  from scrapers.models import Scraper  # noqa: F401
  from .typing import AliasFaker


class ScraperFactory(factory.django.DjangoModelFactory["Scraper"]):
  name: "factory.Sequence[str]" = factory.Sequence(lambda n: "Scraper %03d" % n)
  pricing_selector: "AliasFaker[str]" = factory.Faker("sentence")
  pricing_regex: "AliasFaker[str]" = factory.Faker("sentence")
  pricing_bulk_selector: "AliasFaker[str]" = factory.Faker("sentence")
  pricing_bulk_regex: "AliasFaker[str]" = factory.Faker("sentence")
  url_validation_regex: "AliasFaker[str]" = factory.Faker("url")

  class Meta:
    model = "scrapers.Scraper"
