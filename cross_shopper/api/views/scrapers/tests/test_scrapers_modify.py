"""Test for the ScrapersReadOnlyViewSet modify view."""

from typing import TYPE_CHECKING

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from .conftest import AliasScraperDetailUrl

if TYPE_CHECKING:  # no cover
  from scrapers.models import Scraper


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestScrapersViewSetModify:
  """Tests for the ScrapersReadOnlyViewSet modify view."""

  def test_modify__forbids_access(
      self,
      client: APIClient,
      scraper: "Scraper",
      scraper_detail_url: AliasScraperDetailUrl,
  ) -> None:
    res = client.put(scraper_detail_url(scraper.id), data={})

    assert res.status_code == status.HTTP_403_FORBIDDEN
