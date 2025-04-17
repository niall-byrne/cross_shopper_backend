"""Test for the ScrapersReadOnlyViewSet retrieve view."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from rest_framework import status
from scrapers.models.serializers.scraper import ScraperSerializer

if TYPE_CHECKING:
  from rest_framework.test import APIClient
  from scrapers.models import Scraper
  from .conftest import AliasScraperDetailUrl


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestScrapersReadOnlyViewSetRetrieve:

  def test_retrieve__returns_correct_response(
      self,
      client: APIClient,
      scraper: Scraper,
      scraper_detail_url: AliasScraperDetailUrl,
  ) -> None:
    res = client.get(scraper_detail_url(scraper.pk))
    serializer = ScraperSerializer(scraper)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data
