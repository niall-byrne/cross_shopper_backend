"""Tests for the memoize decorator."""

from typing import Any
from unittest import mock

import pytest
from django.core.cache import cache
from utilities.cache import memoize
from utilities.cache.tests.conftest import RealisticSerializer


class TestMemoizeDecorator:

  def test_compute_expensive_value__same_instance_same_args__returns_cached_result(
      self,
      serializer: RealisticSerializer,
  ) -> None:
    arg = "arg1"
    serializer.compute_expensive_value(arg)

    result = serializer.compute_expensive_value(arg)

    assert result == f"Result for {arg} with context {serializer.context}"
    assert serializer.call_count == 1

  def test_compute_expensive_value__different_instances_same_repr__shares_cache(
      self,
      serializer: RealisticSerializer,
      identical_serializer: RealisticSerializer,
  ) -> None:
    arg = "arg1"
    serializer.compute_expensive_value(arg)

    result = identical_serializer.compute_expensive_value(arg)

    assert repr(serializer) == repr(identical_serializer)
    assert result == f"Result for {arg} with context {serializer.context}"
    assert identical_serializer.call_count == 0

  def test_compute_expensive_value__different_instances_different_repr__uses_isolated_cache(
      self,
      serializer: RealisticSerializer,
      different_serializer: RealisticSerializer,
  ) -> None:
    arg = "arg1"
    serializer.compute_expensive_value(arg)

    result = different_serializer.compute_expensive_value(arg)

    assert repr(serializer) != repr(different_serializer)
    assert result != f"Result for {arg} with context {serializer.context}"
    assert different_serializer.call_count == 1

  def test_compute_expensive_value__same_instance_different_args__uses_isolated_cache(
      self,
      serializer: RealisticSerializer,
  ) -> None:
    arg1 = "arg1"
    arg2 = "arg2"
    serializer.compute_expensive_value(arg1)

    result = serializer.compute_expensive_value(arg2)

    assert result != f"Result for {arg1} with context {serializer.context}"
    assert serializer.call_count == 2

  def test_memoize__none_result__returns_cached_none(self) -> None:
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

  def test_memoize__same_args_different_funcs__uses_isolated_cache(
      self
  ) -> None:
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

  def test_memoize__timeout_specified__passes_timeout_to_cache_backend(
      self,
  ) -> None:
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
  def test_memoize__various_argument_types__returns_correct_cached_result(
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
