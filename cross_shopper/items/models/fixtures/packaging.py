"""Fixtures for building Packaging models."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from items.models.factories.packaging import PackagingFactory
from items.models.factories.packaging_container import PackagingContainerFactory
from items.models.factories.packaging_unit import PackagingUnitFactory

if TYPE_CHECKING:
  from items.models import Packaging, PackagingContainer, PackagingUnit


@pytest.fixture
def packaging_as_bulk() -> Packaging:
  return PackagingFactory.create(
      quantity=None,
      container=None,
      unit__name="lbs",
  )


@pytest.fixture
def packaging_as_non_bulk() -> Packaging:
  return PackagingFactory.create(
      container__name="box",
      unit__name="g",
  )


@pytest.fixture
def packaging_container() -> PackagingContainer:
  return PackagingContainerFactory.create()


@pytest.fixture
def packaging_unit() -> PackagingUnit:
  return PackagingUnitFactory.create()
