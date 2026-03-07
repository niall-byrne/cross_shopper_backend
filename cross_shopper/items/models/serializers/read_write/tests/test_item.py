"""Test the ItemSerializerRW class."""

import re
from typing import TYPE_CHECKING

import pytest
from django.db.models import QuerySet
from items.models import Attribute, Brand, Item, Packaging
from items.models.serializers.read_write.item import ItemSerializerRW
from items.models.serializers.read_write.packaging import PackagingSerializerRW
from rest_framework.exceptions import ErrorDetail, ValidationError
from scrapers.models.scraper_config import ScraperConfig
from scrapers.models.serializers.read_only.scraper_config import (
    ScraperConfigSerializerRO,
)
from utilities.models.validators.restricted_values import VALIDATION_ERROR

if TYPE_CHECKING:  # no cover
  from typing import Any, Dict

  from scrapers.models import Scraper

  AliasNestedItemData = Dict[str, Any]


@pytest.mark.django_db
class TestItemSerializerRW:

  def compare_instance_to_data(
      self,
      item_instance: Item,
      item_data: "Dict[str, Any]",
      attribute_instances: "QuerySet[Attribute]",
      scraper_config_instances: "QuerySet[ScraperConfig]",
  ) -> None:
    assert item_instance.name == item_data['name']
    assert item_instance.brand.name == item_data['brand']
    assert list(item_instance.attribute.all()) == list(attribute_instances)

    assert item_instance.packaging.quantity == \
        item_data['packaging']['quantity']
    assert item_instance.packaging.unit.name == item_data['packaging']['unit']
    assert item_instance.packaging.container is not None
    assert item_instance.packaging.container.name == \
        item_data['packaging']['container']

    assert item_instance.is_non_gmo == item_data['is_non_gmo']
    assert item_instance.is_organic == item_data['is_organic']

    assert list(item_instance.scraper_config.all()) == \
        list(scraper_config_instances)
    for index, scraper_config_instance in enumerate(scraper_config_instances):
      self.validate_scraper_config_instance(
          item_data['scraper_config'][index], scraper_config_instance
      )

  def validate_scraper_config_instance(
      self,
      received_data: "Dict[str, Any]",
      scraper_config_instance: "ScraperConfig",
  ) -> None:
    validation_regex = re.compile(
        scraper_config_instance.scraper.url_validation_regex,
    )
    match = validation_regex.match(received_data['url'])
    assert match is not None
    assert scraper_config_instance.url == match.group(2)

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
        'name_full':
            item.name_full,
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

  def test_deserialization__valid_input__new_all__correct_model(
      self,
      scraper: "Scraper",
  ) -> None:
    item_data: AliasNestedItemData = {
        "name":
            "Avocados",
        "attribute": [
            "new_attribute1",
            "new_attribute2",
        ],
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

    self.compare_instance_to_data(
        instance,
        item_data,
        Attribute.objects.filter(name__in=['new_attribute1', 'new_attribute2']),
        ScraperConfig.objects.filter(scraper=scraper),
    )

  def test_deserialization__valid_input__existing_all__correct_model(
      self,
      attribute: "Attribute",
      brand: "Brand",
      scraper: "Scraper",
      packaging_as_non_bulk: "Packaging",
  ) -> None:
    assert packaging_as_non_bulk.unit is not None
    assert packaging_as_non_bulk.container is not None
    item_data: AliasNestedItemData = {
        "name":
            "Avocados",
        "attribute": [attribute.name,],
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

    self.compare_instance_to_data(
        instance,
        item_data,
        Attribute.objects.filter(pk=attribute.pk),
        ScraperConfig.objects.filter(scraper=scraper),
    )

  def test_deserialization__invalid_input__missing_fields__exception(
      self,
      scraper: "Scraper",
  ) -> None:
    item_data: "AliasNestedItemData" = {
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
            'attribute':
                [
                    ErrorDetail(
                        string='This field is required.', code='required'
                    )
                ],
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

  def test_deserialization__invalid_input__invalid_attribute__exception(
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
        "attribute": ["invalid,attribute"],
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

    with pytest.raises(ValidationError) as exc:
      serialized = ItemSerializerRW(data=item_data)
      serialized.is_valid(raise_exception=True)

    assert str(exc.value) == str(
        {
            'attribute':
                {
                    'name':
                        [
                            ErrorDetail(
                                string=VALIDATION_ERROR % ',',
                                code='invalid',
                            ),
                        ]
                }
        }
    )
