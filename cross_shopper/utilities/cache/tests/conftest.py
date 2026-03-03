"""Test fixtures for the summary family of serializers for Reports."""

import pytest
from django.core.cache import cache
from utilities.cache import memoize


class RealisticModel:
  """A realistic model-like class for testing."""

  def __init__(self, pk: int, name: str):
    self.pk = pk
    self.name = name

  def __repr__(self) -> str:
    return f"<{self.__class__.__name__}: {self.pk}>"


class RealisticSerializer:
  """A realistic serializer-like class for testing."""

  def __init__(self, instance: RealisticModel, context: dict = None):
    self.instance = instance
    self.context = context or {}
    self.call_count = 0

  def __repr__(self) -> str:
    return ":".join(
        map(
            repr, [
                self.context.get('week'),
                self.context.get('year'),
                self.context.get('report'), self.__class__
            ]
        )
    )

  @memoize(timeout=60)
  def compute_expensive_value(self, arg: str) -> str:
    self.call_count += 1
    return f"Result for {arg} with context {self.context}"


@pytest.fixture(autouse=True)
def clear_django_cache():
  cache.clear()
  yield
  cache.clear()


@pytest.fixture
def model_instance() -> RealisticModel:
  return RealisticModel(pk=1, name="Test Item")


@pytest.fixture
def serializer_context() -> dict:
  return {'week': 1, 'year': 2024, 'report': 'ReportA'}


@pytest.fixture
def serializer(
    model_instance: RealisticModel,
    serializer_context: dict,
) -> RealisticSerializer:
  return RealisticSerializer(model_instance, context=serializer_context)


@pytest.fixture
def identical_serializer(
    model_instance: RealisticModel,
    serializer_context: dict,
) -> RealisticSerializer:
  return RealisticSerializer(model_instance, context=dict(serializer_context))


@pytest.fixture
def different_serializer(
    model_instance: RealisticModel,
) -> RealisticSerializer:
  return RealisticSerializer(
      model_instance, context={
          'week': 2,
          'year': 2024,
          'report': 'ReportA'
      }
  )
