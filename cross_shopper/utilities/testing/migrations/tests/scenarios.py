"""Scenarios for the migration testing helpers tests."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

import pytest
from errors.models.factories import error_type
from items.models.factories import attribute, brand
from utilities.testing.migrations.app_model_set import AppModelSet

if TYPE_CHECKING:  # no cover

  from typing import Callable, TypeVar

  from errors.models import ErrorType
  from items.models import Attribute, Brand
  from scrapers.models import Scraper

  TestFunctionType = TypeVar("TestFunctionType", bound="Callable[..., None]")


@dataclass
class ErrorModelSet(AppModelSet):
  ErrorType: "ErrorType"

  module: ClassVar[str] = "errors"


@dataclass
class ItemsAppModelSet(AppModelSet):
  Attribute: "Attribute"
  Brand: "Brand"

  module: ClassVar[str] = "items"


@dataclass
class ScraperModelSet(AppModelSet):
  Scraper: "Scraper"

  module: ClassVar[str] = "scrapers"


app_model_set_scenarios = pytest.mark.parametrize(
    "scenario", (
        {
            "klass": ItemsAppModelSet,
            "migration": "0005_add_item_attribute",
            "models":
                {
                    "Attribute": attribute.AttributeFactory,
                    "Brand": brand.BrandFactory
                },
        },
        {
            "klass": ErrorModelSet,
            "migration": "0001_initial",
            "models": {
                "ErrorType": error_type.ErrorTypeFactory,
            },
        },
    )
)


def app_model_set_kwargs_scenarios(
    test_function: "TestFunctionType",
) -> "TestFunctionType":
  test_function = pytest.mark.parametrize(
      "kwargs",
      (
          {
              "name": "Mocked_name1"
          },
          {
              "name": "Mocked_name2",
              "url_validation_regex": ".*",
          },
      ),
  )(test_function)

  test_function = pytest.mark.parametrize(
      "scenario", (
          {
              "klass": ScraperModelSet,
              "migration": "0001_initial",
              "model": "Scraper",
          },
      )
  )(test_function)

  return test_function
