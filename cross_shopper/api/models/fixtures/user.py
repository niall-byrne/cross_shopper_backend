"""Test fixtures for API user instances."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from api.models.factories.user import UserFactory
from django.contrib.auth import get_user_model

if TYPE_CHECKING:
  from django.contrib.auth.base_user import AbstractBaseUser

User = get_user_model()


@pytest.fixture
def user() -> AbstractBaseUser:
  return UserFactory.create()
