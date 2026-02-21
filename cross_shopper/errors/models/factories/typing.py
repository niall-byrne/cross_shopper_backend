"""Type aliases for error model factories."""

from typing import TypeVar

import factory

FakerType = TypeVar("FakerType")
ModelType = TypeVar("ModelType")

AliasFaker = factory.Faker[FakerType, FakerType]
AliasSubFactory = factory.SubFactory[ModelType, ModelType]
