"""Test for the ScrapersReadOnlyViewSet modify view."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from rest_framework import status

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
class TestScrapersReadOnlyViewSetModify:

  def test_modify__forbids_access(
      self,
      client: APIClient,
      scraper: Scraper,
      scraper_detail_url: AliasScraperDetailUrl,
  ) -> None:
    res = client.put(scraper_detail_url(scraper.pk), data={})

    assert res.status_code == status.HTTP_403_FORBIDDEN
