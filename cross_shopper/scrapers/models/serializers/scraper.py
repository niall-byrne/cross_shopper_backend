"""Serializer for the Scraper model."""

from rest_framework import serializers
from scrapers.models import Scraper
from utilities.models.serializers.fields.title import TitleField


class ScraperSerializer(serializers.ModelSerializer):
  """Serializer for the Scraper model."""

  name = TitleField(max_length=80, allow_blank=False)

  class Meta:
    model = Scraper
    fields = (
        'id',
        'name',
        'url_validation_regex',
    )
