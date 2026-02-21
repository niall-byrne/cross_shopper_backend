"""Test the ErrorSerializer class."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from errors.models import Error
from errors.models.serializers.error import ErrorSerializer

if TYPE_CHECKING:
  from errors.models import ErrorType
  from items.models import Item
  from scrapers.models import ScraperConfig
  from stores.models import Store


@pytest.mark.django_db
class TestErrorSerializer:

  def test_serialization__correct_representation(
      self,
      error: Error,
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

  def test_deserialization__valid_input__non_existent__correct_model_and_count(
      self,
      error_type: ErrorType,
      item: Item,
      scraper_config: ScraperConfig,
      store: Store,
  ) -> None:
    error_data: dict[str, str | int] = {
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
    assert instance.count == 1

  def test_deserialization__valid_input__existent__correct_model_and_count(
      self,
      error_type: ErrorType,
      item: Item,
      scraper_config: ScraperConfig,
      store: Store,
  ) -> None:
    duplicate_data: dict[str, str | int] = {
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
    serialized.save()

    instance.refresh_from_db()
    assert serialized.data["id"] == instance.pk
    assert instance.count == 2
