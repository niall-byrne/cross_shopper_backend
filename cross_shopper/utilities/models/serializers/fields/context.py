"""Experimental."""

from typing import TYPE_CHECKING

from rest_framework import serializers

if TYPE_CHECKING:  #no cover
  from typing import Any, Callable, Optional


class SerializerContextField(serializers.Field):
  """A custom field to extract values from serializer context."""

  context_field: "Optional[str]"
  default_value: "Optional[Callable[[], Any]]"

  class Messages:
    no_context_field = "A serializer ContextField requires a context field."

  def __init__(
      self,
      *args: "Any",
      **kwargs: "Any",
  ) -> None:
    kwargs['source'] = '*'
    kwargs['read_only'] = True

    self.default_value = kwargs.pop("default_value", None)

    if "context_field" in kwargs:
      self.context_field = kwargs.pop("context_field")
    else:
      self.context_field = None

    super().__init__(*args, **kwargs)

  def to_representation(self, value: "Any") -> "Any":
    """Transform the *outgoing* native value into primitive data."""
    if not self.context_field:
      raise Exception(self.Messages.no_context_field)

    context_value = self.context.get(self.context_field, None)
    if not context_value and self.default_value is not None:
      context_value = self.default_value()

    return context_value
