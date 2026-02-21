"""Serializer for the ScraperConfig model."""

from rest_framework import serializers
from scrapers.models import Scraper, ScraperConfig


class ScraperConfigSerializer(serializers.ModelSerializer[ScraperConfig]):
  """Serializer for the ScraperConfig model."""

  scraper = serializers.SlugRelatedField(
      queryset=Scraper.objects.all(),
      slug_field='name',
  )
  url = serializers.CharField()

  class Meta:
    model = ScraperConfig
    fields = ('id', 'scraper', 'url', 'is_active')
