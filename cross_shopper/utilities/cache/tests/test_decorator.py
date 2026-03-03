"""Tests for the memoize decorator."""

from typing import Any
from unittest import mock

import pytest
from django.core.cache import cache
from utilities.cache import memoize
from utilities.cache.tests.conftest import MockSerializer


class TestMemoizeDecorator:

  def test_memoized_method__same_instance_same_args__returns_cached_result(
      self,
      mocked_serializer: MockSerializer,
  ) -> None:
    arg = "arg1"
    mocked_serializer.memoized_method(arg)

    result = mocked_serializer.memoized_method(arg)

    assert result == f"Result for {arg} with context {mocked_serializer.context}"
    assert mocked_serializer.call_count == 1

  def test_memoized_method__different_instances_same_repr__shares_cache(
      self,
      mocked_serializer: MockSerializer,
      mocked_identical_serializer: MockSerializer,
  ) -> None:
    arg = "arg1"
    mocked_serializer.memoized_method(arg)

    result = mocked_identical_serializer.memoized_method(arg)

    assert repr(mocked_serializer) == repr(mocked_identical_serializer)
    assert result == f"Result for {arg} with context {mocked_serializer.context}"
    assert mocked_identical_serializer.call_count == 0

  def test_memoized_method__different_instances_different_repr__uses_isolated_cache(
      self,
      mocked_serializer: MockSerializer,
      mocked_different_serializer: MockSerializer,
  ) -> None:
    arg = "arg1"
    mocked_serializer.memoized_method(arg)

    result = mocked_different_serializer.memoized_method(arg)

    assert repr(mocked_serializer) != repr(mocked_different_serializer)
    assert result != f"Result for {arg} with context {mocked_serializer.context}"
    assert mocked_different_serializer.call_count == 1

  def test_memoized_method__same_instance_different_args__uses_isolated_cache(
      self,
      mocked_serializer: MockSerializer,
  ) -> None:
    arg1 = "arg1"
    arg2 = "arg2"
    mocked_serializer.memoized_method(arg1)

    result = mocked_serializer.memoized_method(arg2)

    assert result != f"Result for {arg1} with context {mocked_serializer.context}"
    assert mocked_serializer.call_count == 2

  def test_memoized_method__none_result__returns_cached_none(self) -> None:
    call_count = 0

    @memoize()
    def return_none(x):
      nonlocal call_count
      call_count += 1
      return None

    return_none(1)
    result = return_none(1)

    assert result is None
    assert call_count == 1

  def test_memoized_method__same_args__vary_func__isolated_caches(self) -> None:
    call_counts = {"f1": 0, "f2": 0}

    @memoize()
    def func1(x):
      call_counts["f1"] += 1
      return f"f1:{x}"

    @memoize()
    def func2(x):
      call_counts["f2"] += 1
      return f"f2:{x}"

    res1 = func1(1)
    res2 = func2(1)

    assert res1 == "f1:1"
    assert res2 == "f2:1"
    assert call_counts["f1"] == 1
    assert call_counts["f2"] == 1

  def test_memoized_method__timeout__passes_timeout_backend(self,) -> None:
    timeout_value = 123

    @memoize(timeout=timeout_value)
    def timed_func(x):
      return x

    with mock.patch.object(cache, 'set', wraps=cache.set) as mock_set:
      timed_func("test")

      args, _ = mock_set.call_args

    assert args[2] == timeout_value

  @pytest.mark.parametrize("val", [
      123,
      "string",
      (1, 2),
      3.14,
      None,
  ])
  def test_memoize__vary_args__returns_correct_cached_results(
      self,
      val: Any,
  ) -> None:
    call_count = 0

    @memoize()
    def identity(x):
      nonlocal call_count
      call_count += 1
      return x

    identity(val)
    result = identity(val)

    assert result == val
    assert call_count == 1
