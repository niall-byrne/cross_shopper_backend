"""Test fixtures for the API client."""

import pytest
from django.contrib.auth.base_user import AbstractBaseUser
from rest_framework.test import APIClient


@pytest.fixture
def authenticated_client(
    unauthenticated_client: "APIClient",
    user: AbstractBaseUser,
) -> APIClient:
  unauthenticated_client.force_authenticate(user)
  return unauthenticated_client


@pytest.fixture
def unauthenticated_client() -> APIClient:
  return APIClient()
