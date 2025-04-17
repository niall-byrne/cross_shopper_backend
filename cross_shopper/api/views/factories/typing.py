"""Type aliases for API views model factories."""

from typing import TypeVar

import factory

FakerType = TypeVar("FakerType")

AliasFaker = factory.Faker[FakerType, FakerType]
