"""Class instance comparison test helper."""

from dataclasses import dataclass
from typing import Any


@dataclass
class InstanceOfClass:
  """Class instance comparison test helper."""

  base: type[Any]
  attributes: dict[str, Any]
  error_prefix: str = ""

  class Messages:
    attribute_missing = "missing attribute {}!"
    attribute_wrong = (
        "attribute '{}' has incorrect value '{}' (expected '{}')!"
    )
    not_an_instance = "not an instance of {}!"

  def fail(self, message: str) -> None:
    """Triggers a pytest test failure with an appropriate message."""
    raise Exception(self.error_prefix + message)

  def __eq__(self, target_instance: object) -> bool:
    self.error_prefix = f"'{target_instance}' -- "

    if not isinstance(target_instance, self.base):
      self.fail(self.Messages.not_an_instance.format(self.base))

    for attribute, expected in self.attributes.items():
      if not hasattr(target_instance, attribute):
        self.fail(self.Messages.attribute_missing.format(attribute))
      actual = getattr(target_instance, attribute)
      if not actual == expected:
        self.fail(
            self.Messages.attribute_wrong.format(attribute, actual, expected)
        )

    return True

  def __repr__(self) -> str:
    return str(self.__class__)
