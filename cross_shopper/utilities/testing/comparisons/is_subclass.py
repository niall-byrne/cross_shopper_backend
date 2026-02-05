"""Dynamic subclass comparison test helper."""

from dataclasses import dataclass
from typing import Any, Dict, Type, cast


@dataclass
class DynamicSubClass:
  """Dynamic subclass comparison test helper."""

  base: Type[Any]
  attributes: Dict[str, Any]
  error_prefix: str = ""

  class Messages:
    attribute_missing = "missing attribute {}!"
    attribute_wrong = (
        "attribute '{}' has incorrect value '{}' (expected '{}')!"
    )
    not_a_class = "is not a class!"
    not_a_subclass = "not an subclass of {}!"

  def fail(self, message: str) -> None:
    """Triggers a pytest test failure with an appropriate message."""
    raise Exception(self.error_prefix + message)

  def __eq__(self, target_klass: object) -> bool:
    self.error_prefix = f"'{target_klass}' -- "

    if not isinstance(target_klass, type):
      self.fail(self.Messages.not_a_class)

    if not issubclass(cast(type, target_klass), self.base):
      self.fail(self.Messages.not_a_subclass.format(self.base))

    for attribute, expected in self.attributes.items():
      if not hasattr(target_klass, attribute):
        self.fail(self.Messages.attribute_missing.format(attribute))
      actual = getattr(target_klass, attribute)
      if not actual == expected:
        self.fail(
            self.Messages.attribute_wrong.format(attribute, actual, expected)
        )

    return True

  def __repr__(self) -> str:
    return str(self.__class__)
