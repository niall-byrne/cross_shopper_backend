"""Type aliases for stores model factories."""

from typing import TypeVar

import factory

AttributeType = TypeVar("AttributeType")
FakerType = TypeVar("FakerType")
ModelType = TypeVar("ModelType")

AliasFaker = factory.Faker[FakerType, FakerType]
AliasSelfAttribute = factory.SelfAttribute[AttributeType, AttributeType]
AliasSubFactory = factory.SubFactory[ModelType, ModelType]
