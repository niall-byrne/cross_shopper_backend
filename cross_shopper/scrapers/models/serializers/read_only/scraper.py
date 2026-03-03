"""Serializer to retrieve or list Scrapers."""

from rest_framework import serializers
from scrapers.models.scraper import CONSTRAINT_NAMES, Scraper
from utilities.models.serializers.fields.title import TitleField


class ScraperSerializerRO(serializers.ModelSerializer[Scraper]):
  """Serializer to retrieve or list Scrapers."""

  name = TitleField(max_length=80, allow_blank=False)

  class Meta:
    model = Scraper
    fields = (
        'id',
        'name',
        'url_validation_regex',
    )

  def validate_name(self, value: str) -> str:
    """Ensure that the name is unique, ignoring case."""
    lower_value = value.lower()

    if Scraper.objects.filter(name__iexact=lower_value).exists():
      raise serializers.ValidationError(CONSTRAINT_NAMES['name'])

    return lower_value
