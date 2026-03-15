"""Test fixtures for the API client."""

from typing import TYPE_CHECKING

import pytest
from rest_framework.test import APIClient

if TYPE_CHECKING:  # no cover
  from django.contrib.auth.base_user import AbstractBaseUser


@pytest.fixture
def authenticated_client(
    unauthenticated_client: "APIClient",
    user: "AbstractBaseUser",
) -> APIClient:
  unauthenticated_client.force_authenticate(user)
  return unauthenticated_client


@pytest.fixture
def unauthenticated_client() -> APIClient:
  return APIClient()
