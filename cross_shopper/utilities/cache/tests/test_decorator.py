"""Tests for the memoize decorator."""

from unittest import mock

import pytest
from django.core.cache import cache
from utilities.cache import memoize


class TestMemoizeDecorator:
  """Tests for the memoize decorator."""

  def test_compute__same_instance_same_args__shares_cache(self, serializer) -> None:
    """Test that calling the same method on the same instance twice uses the cache."""
    res1 = serializer.compute_expensive_value("arg1")
    res2 = serializer.compute_expensive_value("arg1")

    assert res1 == res2
    assert serializer.call_count == 1

  def test_compute__different_instance_same_repr__shares_cache(
      self, serializer, identical_serializer
  ) -> None:
    """Test that two different instances with the same __repr__ share the cache."""
    assert repr(serializer) == repr(identical_serializer)

    res1 = serializer.compute_expensive_value("arg1")
    assert serializer.call_count == 1

    res2 = identical_serializer.compute_expensive_value("arg1")
    assert res1 == res2
    # The second serializer's compute_expensive_value should not have been executed
    assert identical_serializer.call_count == 0

  def test_compute__different_instance_different_repr__isolated_cache(
      self, serializer, different_serializer
  ) -> None:
    """Test that instances with different __repr__ have isolated caches."""
    assert repr(serializer) != repr(different_serializer)

    res1 = serializer.compute_expensive_value("arg1")
    assert serializer.call_count == 1

    res2 = different_serializer.compute_expensive_value("arg1")
    # results are different because context is different
    assert res1 != res2
    assert different_serializer.call_count == 1

  def test_compute__same_instance_different_args__isolated_cache(
      self, serializer
  ) -> None:
    """Test that calling with different arguments has isolated cache entries."""
    res1 = serializer.compute_expensive_value("arg1")
    res2 = serializer.compute_expensive_value("arg2")

    assert res1 != res2
    assert serializer.call_count == 2

  def test_memoize__none_result__is_cached(self) -> None:
    """Test that None result is correctly cached and doesn't re-trigger computation."""
    call_count = 0

    @memoize()
    def return_none(x):
      nonlocal call_count
      call_count += 1
      return None

    assert return_none(1) is None
    assert return_none(1) is None
    assert call_count == 1

  def test_memoize__function_isolation__same_args_different_funcs_isolated(
      self,
  ) -> None:
    """Test that two different functions don't share cache even with same args."""
    call_counts = {"f1": 0, "f2": 0}

    @memoize()
    def func1(x):
      call_counts["f1"] += 1
      return f"f1:{x}"

    @memoize()
    def func2(x):
      call_counts["f2"] += 1
      return f"f2:{x}"

    assert func1(1) == "f1:1"
    assert func2(1) == "f2:1"
    assert call_counts["f1"] == 1
    assert call_counts["f2"] == 1

  def test_memoize__timeout__is_honored(self) -> None:
    """Test that the timeout parameter is correctly passed to the cache backend."""

    @memoize(timeout=123)
    def timed_func(x):
      return x

    with mock.patch.object(cache, 'set', wraps=cache.set) as mock_set:
      timed_func("test")
      # Get the arguments of the first call to cache.set
      # signature is cache.set(key, value, timeout)
      args, _ = mock_set.call_args
      assert args[2] == 123

  @pytest.mark.parametrize(
      "val", [
          123,
          "string",
          (1, 2),
          3.14,
          None,
      ]
  )
  def test_memoize__various_types__handles_correctly(self, val) -> None:
    """Test memoization handles common hashable/repr-able types as arguments."""
    call_count = 0

    @memoize()
    def identity(x):
      nonlocal call_count
      call_count += 1
      return x

    assert identity(val) == val
    assert identity(val) == val
    assert call_count == 1
