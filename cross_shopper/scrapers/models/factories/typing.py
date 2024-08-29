"""Type aliases for scrapers model factories."""

from typing import TypeVar

import factory

AttributeType = TypeVar("AttributeType")
FakerType = TypeVar("FakerType")
ModelType = TypeVar("ModelType")

AliasFaker = factory.Faker[FakerType, FakerType]
AliasSubFactory = factory.SubFactory[ModelType, ModelType]
