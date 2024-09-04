"""Serializer for the Scraper model."""

from rest_framework import serializers
from scrapers.models.scraper import CONSTRAINT_NAMES, Scraper
from utilities.models.serializers.fields.title import TitleField


class ScraperSerializer(serializers.ModelSerializer[Scraper]):
  """Serializer for the Scraper model."""

  name = TitleField(max_length=80, allow_blank=False)

  class Meta:
    model = Scraper
    fields = "__all__"

  def validate_name(self, value: str) -> str:
    """Ensure that the name is unique, ignoring case."""
    lower_value = value.lower()

    if Scraper.objects.filter(name__iexact=lower_value).exists():
      raise serializers.ValidationError(CONSTRAINT_NAMES["name"])

    return lower_value
