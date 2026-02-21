"""Fixtures for building Error models."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from errors.models import Error
from errors.models.factories.error import ErrorFactory

if TYPE_CHECKING:
  from django.db.models import QuerySet
  from errors.models import ErrorType


@pytest.fixture
def error(error_type: ErrorType) -> Error:
  return ErrorFactory.create(type=error_type)


@pytest.fixture
def error_batch() -> QuerySet[Error]:
  errors = ErrorFactory.create_batch(size=10)
  return Error.objects.filter(id__in=[instance.pk for instance in errors])
