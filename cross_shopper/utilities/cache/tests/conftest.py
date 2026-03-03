"""Test fixtures for the summary family of serializers for Reports."""

from typing import Any, Generator

import pytest
from django.core.cache import cache
from utilities.cache import memoize


class MockModel:

  def __init__(self, pk: int, name: str) -> None:
    self.pk = pk
    self.name = name


class MockSerializer:

  def __init__(
      self,
      instance: MockModel,
      context: dict[str, Any] | None = None,
  ):
    self.instance = instance
    self.context = context or {}
    self.call_count = 0

  def __repr__(self) -> str:
    return ":".join(
        map(
            repr, [
                self.context.get("week"),
                self.context.get("year"),
                self.context.get("report"), self.__class__
            ]
        )
    )

  @memoize(timeout=60)
  def memoized_method(self, arg: str) -> str:
    self.call_count += 1
    return f"Result for {arg} with context {self.context}"


@pytest.fixture(autouse=True)
def clear_django_cache() -> Generator[None, None, None]:
  cache.clear()
  yield
  cache.clear()


@pytest.fixture
def mocked_arg() -> str:
  return "arg1"


@pytest.fixture
def mocked_different_serializer(
    mocked_model_instance: MockModel,
) -> MockSerializer:
  return MockSerializer(
      mocked_model_instance,
      context={
          "week": 2,
          "year": 2024,
          "report": "ReportA"
      }
  )


@pytest.fixture
def mocked_identical_serializer(
    mocked_model_instance: MockModel,
    mocked_serializer_context: dict[str, Any],
) -> MockSerializer:
  return MockSerializer(
      mocked_model_instance, context=dict(mocked_serializer_context)
  )


@pytest.fixture
def mocked_model_instance() -> MockModel:
  return MockModel(pk=1, name="Test Item")


@pytest.fixture
def mocked_serializer(
    mocked_model_instance: MockModel,
    mocked_serializer_context: dict[str, Any],
) -> MockSerializer:
  return MockSerializer(
      mocked_model_instance, context=mocked_serializer_context
  )


@pytest.fixture
def mocked_serializer_context() -> dict[str, Any]:
  return {"week": 1, "year": 2024, "report": "ReportA"}
