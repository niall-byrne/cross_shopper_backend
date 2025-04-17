"""Test for the ScrapersReadOnlyViewSet retrieve view."""

from typing import TYPE_CHECKING

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from scrapers.models.serializers.scraper import ScraperSerializer
from .conftest import AliasScraperDetailUrl

if TYPE_CHECKING:  # no cover
  from scrapers.models import Scraper


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestScrapersViewSetRetrieve:
  """Tests for the ScrapersReadOnlyViewSet retrieve view."""

  def test_retrieve__returns_correct_response(
      self,
      client: APIClient,
      scraper: "Scraper",
      scraper_detail_url: AliasScraperDetailUrl,
  ) -> None:
    res = client.get(scraper_detail_url(scraper.id))
    serializer = ScraperSerializer(scraper)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data
