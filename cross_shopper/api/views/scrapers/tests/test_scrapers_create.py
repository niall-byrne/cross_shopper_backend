"""Test for the ScrapersReadOnlyViewSet create view."""

from typing import TYPE_CHECKING

import pytest
from rest_framework import status

if TYPE_CHECKING:  # no cover
  from rest_framework.test import APIClient
  from .conftest import AliasScraperListUrl


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestScrapersReadOnlyViewSetCreate:
  """Tests for the ScrapersReadOnlyViewSet create view."""

  def test_create__forbids_access(
      self,
      client: "APIClient",
      scraper_list_url: "AliasScraperListUrl",
  ) -> None:
    res = client.post(scraper_list_url(), data={})

    assert res.status_code == status.HTTP_403_FORBIDDEN
