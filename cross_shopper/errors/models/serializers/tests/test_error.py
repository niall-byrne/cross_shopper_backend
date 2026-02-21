"""Test the ErrorSerializer class."""

from typing import TYPE_CHECKING, Dict, Union

import pytest
from django.core.exceptions import ValidationError
from errors.models import Error, ErrorType
from errors.models.serializers.error import ErrorSerializer
from rest_framework.exceptions import (
    ValidationError as SerializerValidationError,
)

if TYPE_CHECKING:  # no cover
  from items.models import Item
  from scrapers.models import ScraperConfig
  from stores.models import Store


@pytest.mark.django_db
class TestErrorSerializer:

  def test_serialization__correct_representation(
      self,
      error: "Error",
  ) -> None:
    serialized = ErrorSerializer(error)

    assert serialized.data == {
        "id": error.pk,
        "type": error.type.name,
        "item": error.item.pk,
        "is_reoccurring": error.is_reoccurring,
        "scraper_config": error.scraper_config.pk,
        "store": error.store.pk,
    }

  def test_deserialization__valid_input__non_existent__correct_model(
      self,
      error_type: ErrorType,
      item: "Item",
      scraper_config: "ScraperConfig",
      store: "Store",
  ) -> None:
    error_data: Dict[str, Union[str, int]] = {
        "type": error_type.name,
        "item": item.pk,
        "scraper_config": scraper_config.pk,
        "store": store.pk,
    }

    serialized = ErrorSerializer(data=error_data)
    serialized.is_valid(raise_exception=True)
    instance = serialized.save()

    assert instance.type == error_type
    assert instance.item == item
    assert instance.scraper_config == scraper_config
    assert instance.store == store

  def test_deserialization__valid_input__existent__database_error_only(
      self,
      error_type: ErrorType,
      item: "Item",
      scraper_config: "ScraperConfig",
      store: "Store",
  ) -> None:
    duplicate_data: Dict[str, Union[str, int]] = {
        "type": error_type.name,
        "item": item.pk,
        "scraper_config": scraper_config.pk,
        "store": store.pk,
    }
    instance = Error(
        type=error_type,
        item=item,
        scraper_config=scraper_config,
        store=store,
    )
    instance.save()

    serialized = ErrorSerializer(data=duplicate_data)
    serialized.is_valid(raise_exception=True)

    with pytest.raises(ValidationError) as exc:
      serialized.save()

    assert exc.type != SerializerValidationError
