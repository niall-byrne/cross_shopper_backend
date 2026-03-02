"""Type aliases for reports model factories."""

from typing import TypeVar

import factory

ModelType = TypeVar("ModelType")

AliasSubFactory = factory.SubFactory[ModelType, ModelType]
