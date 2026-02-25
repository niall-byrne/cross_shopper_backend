"""Serializer for the ScraperConfig model."""

from rest_framework import serializers
from scrapers.models import Scraper, ScraperConfig
from scrapers.models.scraper_config import CONSTRAINT_NAMES


class ScraperConfigSerializer(serializers.ModelSerializer):
  """Serializer for the ScraperConfig model."""

  scraper = serializers.SlugRelatedField(
      queryset=Scraper.objects.all(),
      slug_field='name',
  )
  url = serializers.CharField()

  class Meta:
    model = ScraperConfig
    fields = ('id', 'scraper', 'url', 'is_active')

  def validate_url(self, value: str):
    """Ensure that the url is unique, ignoring case."""
    lower_value = value.lower()

    if ScraperConfig.objects.filter(url__iexact=lower_value).exists():
      raise serializers.ValidationError(CONSTRAINT_NAMES['url'])

    return lower_value
