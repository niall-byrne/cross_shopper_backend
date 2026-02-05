"""Test fixtures for the comparison utilities tests."""

from typing import Any, Callable, Dict, Type

import pytest

AliasAttributes = Dict[str, Any]
AliasGenericClass = Type[Any]
AliasGenericClassFactory = Callable[[AliasAttributes], AliasGenericClass]


@pytest.fixture
def generic_class() -> AliasGenericClass:

  class GenericClass:
    pass

  return GenericClass


@pytest.fixture
def generic_class_factory(
    generic_class: AliasGenericClass
) -> AliasGenericClassFactory:

  def create(attributes: AliasAttributes) -> AliasGenericClass:

    class GeneratedSubClass(generic_class):
      pass

    for attr, value in attributes.items():
      setattr(GeneratedSubClass, attr, value)

    return GeneratedSubClass

  return create
