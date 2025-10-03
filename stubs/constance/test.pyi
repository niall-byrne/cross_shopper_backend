"""Type hints for django-constance testing functions."""
# isort: skip_file

from typing import Any, Callable


def override_config(
    *args: Any,
    **kwargs: Any,
) -> Callable[[Callable[..., None]], None]:
  ...
