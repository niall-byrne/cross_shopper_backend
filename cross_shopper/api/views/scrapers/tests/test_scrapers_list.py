"""Test for the ScrapersReadOnlyViewSet list view."""

from typing import TYPE_CHECKING

import pytest
from rest_framework import status
from scrapers.models.serializers.scraper import ScraperSerializer

if TYPE_CHECKING:  # no cover
  from rest_framework.test import APIClient
  from scrapers.models import Scraper
  from .conftest import AliasScraperListUrl


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestScrapersReadOnlyViewSetList:

  def test_list__no_filter__returns_correct_response(
      self,
      client: "APIClient",
      scraper: "Scraper",
      scraper_list_url: "AliasScraperListUrl",
  ) -> None:
    res = client.get(scraper_list_url())
    serializer = ScraperSerializer(scraper)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == [serializer.data]

  def test_list__filter_by_scraper_id__returns_correct_response(
      self,
      client: "APIClient",
      scraper: "Scraper",
      scraper_alternate: "Scraper",
      scraper_list_url: "AliasScraperListUrl",
  ) -> None:
    res = client.get(scraper_list_url({"id": scraper_alternate.pk}))
    serializer = ScraperSerializer(scraper_alternate)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == [serializer.data]

  def test_list__filter_by_scraper_name__returns_correct_response(
      self,
      client: "APIClient",
      scraper: "Scraper",
      scraper_alternate: "Scraper",
      scraper_list_url: "AliasScraperListUrl",
  ) -> None:
    res = client.get(scraper_list_url({"name": scraper_alternate.name}))
    serializer = ScraperSerializer(scraper_alternate)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == [serializer.data]

  def test_list__filter_by_uppercase_scraper_name__returns_correct_response(
      self,
      client: "APIClient",
      scraper: "Scraper",
      scraper_alternate: "Scraper",
      scraper_list_url: "AliasScraperListUrl",
  ) -> None:
    res = client.get(scraper_list_url({"name": scraper_alternate.name.upper()}))
    serializer = ScraperSerializer(scraper_alternate)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == [serializer.data]
