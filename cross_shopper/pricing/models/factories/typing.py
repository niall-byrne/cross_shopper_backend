"""Type aliases for pricing model factories."""

from typing import TypeVar

import factory
from factory import fuzzy

FakerType = TypeVar("FakerType")
ModelType = TypeVar("ModelType")

AliasFaker = factory.Faker[FakerType, FakerType]
AliasFuzzyChoice = fuzzy.FuzzyChoice[FakerType, FakerType]
AliasSubFactory = factory.SubFactory[ModelType, ModelType]
