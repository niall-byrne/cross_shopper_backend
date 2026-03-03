"""Test the ItemSerializerRW class."""

import re
from typing import TYPE_CHECKING, Any, Dict

import pytest
from items.models import Brand, Item, Packaging
from items.models.serializers.read_write.item import ItemSerializerRW
from items.models.serializers.read_write.packaging import PackagingSerializerRW
from rest_framework.exceptions import ErrorDetail, ValidationError
from scrapers.models.serializers.read_only.scraper_config import (
    ScraperConfigSerializerRO,
)

if TYPE_CHECKING:  # no cover
  from scrapers.models import Scraper

AliasNestedItemData = Dict[str, Any]


@pytest.mark.django_db
class TestItemSerializerRW:

  def compare_instance_to_data(
      self,
      item_instance: Item,
      item_data: Dict[str, Any],
      scraper_instance: "Scraper",
  ) -> None:
    assert item_instance.name == item_data['name']
    assert item_instance.brand.name == item_data['brand']
    assert item_instance.packaging.quantity == item_data['packaging']['quantity'
                                                                     ]
    assert item_instance.packaging.unit.name == item_data['packaging']['unit']
    assert item_instance.packaging.container
    assert item_instance.packaging.container.name == \
           item_data['packaging']['container']
    assert item_instance.is_non_gmo == item_data['is_non_gmo']
    assert item_instance.is_organic == item_data['is_organic']
    assert item_instance.scraper_config.all()[0].scraper == scraper_instance
    validation_regex = re.compile(
        item_instance.scraper_config.all()[0].scraper.url_validation_regex
    )
    match = validation_regex.match(item_data['scraper_config'][0]['url'])
    assert match
    assert item_instance.scraper_config.all()[0].url == match.group(2)
    assert item_instance.scraper_config.all()[1].scraper == scraper_instance
    validation_regex = re.compile(
        item_instance.scraper_config.all()[0].scraper.url_validation_regex
    )
    match = validation_regex.match(item_data['scraper_config'][1]['url'])
    assert match
    assert item_instance.scraper_config.all()[1].url == match.group(2)

  def test_serialization__correct_representation(
      self,
      item: Item,
  ) -> None:
    serialized = ItemSerializerRW(item)

    assert serialized.data == {
        'id':
            item.pk,
        'name':
            item.name,
        'full_name':
            item.full_name,
        'brand':
            item.brand.name,
        'packaging':
            PackagingSerializerRW(item.packaging).data,
        'is_bulk':
            item.is_bulk,
        'is_non_gmo':
            item.is_non_gmo,
        'is_organic':
            item.is_organic,
        'scraper_config':
            ScraperConfigSerializerRO(item.scraper_config, many=True).data
    }

  def test_deserialization__valid_input__existing_scraper__correct_model(
      self,
      scraper: "Scraper",
  ) -> None:
    item_data: AliasNestedItemData = {
        "name":
            "Avocados",
        "brand":
            "Generic",
        "packaging": {
            "quantity": 4,
            "unit": "pcs",
            "container": "Bag"
        },
        "is_non_gmo":
            False,
        "is_organic":
            False,
        "scraper_config":
            [
                {
                    "scraper": scraper.name,
                    "url": "https://site.com/1",
                }, {
                    "scraper": scraper.name,
                    "url": "https://site.com/2",
                }
            ]
    }

    serialized = ItemSerializerRW(data=item_data)
    serialized.is_valid(raise_exception=True)
    instance = serialized.save()

    self.compare_instance_to_data(instance, item_data, scraper)

  def test_deserialization__valid_input__existing_all__correct_model(
      self,
      brand: "Brand",
      scraper: "Scraper",
      packaging_as_non_bulk: "Packaging",
  ) -> None:
    assert packaging_as_non_bulk.unit is not None
    assert packaging_as_non_bulk.container is not None
    item_data: AliasNestedItemData = {
        "name":
            "Avocados",
        "brand":
            brand.name,
        "packaging":
            {
                "quantity": packaging_as_non_bulk.quantity,
                "unit": packaging_as_non_bulk.unit.name,
                "container": packaging_as_non_bulk.container.name,
            },
        "is_non_gmo":
            False,
        "is_organic":
            False,
        "scraper_config":
            [
                {
                    "scraper": scraper.name,
                    "url": "https://site.com/1",
                }, {
                    "scraper": scraper.name,
                    "url": "https://site.com/2",
                }
            ]
    }

    serialized = ItemSerializerRW(data=item_data)
    serialized.is_valid(raise_exception=True)
    instance = serialized.save()

    self.compare_instance_to_data(instance, item_data, scraper)

  def test_deserialization__invalid_input__existing_scraper__exception(
      self,
      scraper: "Scraper",
  ) -> None:
    item_data: AliasNestedItemData = {
        "name":
            "Avocados",
        "is_non_gmo":
            False,
        "is_organic":
            False,
        "scraper_config":
            [
                {
                    "scraper": scraper.name,
                    "url": scraper.url_validation_regex + "/1",
                }, {
                    "scraper": scraper.name,
                    "url": scraper.url_validation_regex + "/2",
                }
            ]
    }

    with pytest.raises(ValidationError) as exc:
      serialized = ItemSerializerRW(data=item_data)
      serialized.is_valid(raise_exception=True)

    assert str(exc.value) == str(
        {
            'brand':
                [
                    ErrorDetail(
                        string='This field is required.', code='required'
                    )
                ],
            'packaging':
                [
                    ErrorDetail(
                        string='This field is required.', code='required'
                    )
                ]
        }
    )
