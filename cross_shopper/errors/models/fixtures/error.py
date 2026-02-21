"""Fixtures for building Error models."""

from typing import TYPE_CHECKING

import pytest
from errors.models import Error
from errors.models.factories.error import ErrorFactory

if TYPE_CHECKING:  # no cover
  from django.db.models import QuerySet
  from errors.models import ErrorType


@pytest.fixture
def error(error_type: "ErrorType") -> "Error":
  return ErrorFactory.create(type=error_type)


@pytest.fixture
def error_batch() -> "QuerySet[Error]":
  errors = ErrorFactory.create_batch(size=10)
  return Error.objects.filter(id__in=[instance.id for instance in errors])
