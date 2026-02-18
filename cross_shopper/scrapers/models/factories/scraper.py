"""Factories for Scraper model instances."""
from __future__ import annotations

from typing import TYPE_CHECKING

import factory

if TYPE_CHECKING:
  from scrapers.models import Scraper  # noqa: F401


class ScraperFactory(factory.django.DjangoModelFactory["Scraper"]):

  name: factory.Sequence[str] = factory.Sequence(lambda n: "Scraper %03d" % n)
  url_validation_regex: str = "^(https?://)*(.*)"

  class Meta:
    model = "scrapers.Scraper"
