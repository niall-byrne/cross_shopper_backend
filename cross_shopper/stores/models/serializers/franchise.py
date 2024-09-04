"""Serializer for the Franchise model."""

from rest_framework import serializers
from scrapers.models import Scraper
from stores.models.franchise import Franchise
from utilities.models.serializers.fields.blonde import BlondeCharField


class FranchiseSerializer(serializers.ModelSerializer[Franchise]):
  """Serializer for the Franchise model."""

  name = BlondeCharField(max_length=80, allow_blank=False)
  scraper = serializers.SlugRelatedField(
      queryset=Scraper.objects.all(),
      slug_field="name",
  )

  class Meta:
    model = Franchise
    fields = ("name", "scraper")
