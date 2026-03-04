"""A custom serializer field to extract values from the serializer context."""
from __future__ import annotations

from typing import Any, Callable

from rest_framework import serializers


class ContextField(serializers.Field["Any", "Any", "Any", "Any"]):
  """A custom field to extract values from the serializer context."""

  context_key: str
  default_value: Callable[[], Any] | None

  class Messages:
    no_context_key = (
        "A serializer ContextField requires a value for "
        "context_key to be specified."
    )

  def __init__(
      self,
      *args: Any,
      **kwargs: Any,
  ) -> None:
    kwargs["source"] = "*"
    kwargs["read_only"] = True
    self.default_value = kwargs.pop("default_value", None)
    self.context_key = kwargs.pop("context_key", None)
    if (not self.context_key):
      raise Exception(self.Messages.no_context_key)
    super().__init__(*args, **kwargs)

  def _get_context_value(self) -> Any:
    context_value = self.context.get(self.context_key, None)
    if not context_value and self.default_value is not None:
      context_value = self.default_value()

    return context_value

  def to_representation(self, value: Any) -> Any:
    """Transform the *outgoing* native value into primitive data."""
    return self._get_context_value()
