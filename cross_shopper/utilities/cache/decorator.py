"""Django cache method decorator."""

import functools
import hashlib
from typing import Any, Callable, Optional

from django.core.cache import cache


class CacheMiss:
  """A sentinel for identifying a cache miss."""


def memoize(timeout: Optional[int] = None) -> Callable[..., Callable[..., Any]]:
  """Memoize a function with the django caching system."""

  def generate_key(func: Callable[..., Any], *args: Any, **kwargs: Any) -> str:
    cache_key = ":".join(map(
        repr,
        [
            args,
            kwargs,
        ],
    ))
    return "{}:{}".format(func.__name__, cache_key)

  def decorator(func: Callable[..., Any]) -> Callable[..., Any]:

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
      cache_key = generate_key(func, *args, **kwargs)

      hashed_key = hashlib.sha256(cache_key.encode("utf-8")).hexdigest()

      result = cache.get(hashed_key, default=CacheMiss)
      if result is not CacheMiss:
        return result

      result = func(*args, **kwargs)

      cache.set(hashed_key, result, timeout)
      return result

    return wrapper

  return decorator
