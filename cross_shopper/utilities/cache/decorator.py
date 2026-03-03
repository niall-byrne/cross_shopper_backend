"""Django cache method decorator."""

import functools
import hashlib

from django.core.cache import cache


def memoize(timeout=None):
  """Memoize a function with the django caching system."""

  def generate_key(func, *args, **kwargs) -> str:
    cache_key = ":".join(map(repr, [
        args,
        kwargs,
    ]))
    return "{}:{}".format(func.__name__, cache_key)

  def decorator(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      cache_key = generate_key(func, *args, **kwargs)

      hashed_key = hashlib.sha256(cache_key.encode('utf-8')).hexdigest()

      result = cache.get(hashed_key)
      if result is not None:
        return result

      result = func(*args, **kwargs)

      cache.set(hashed_key, result, timeout)
      return result

    return wrapper

  return decorator
