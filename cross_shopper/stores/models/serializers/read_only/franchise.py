"""Serializer to retrieve or list Franchises."""

from rest_framework import serializers
from scrapers.models import Scraper
from stores.models.franchise import Franchise
from utilities.models.serializers.fields.blonde import BlondeCharField


class FranchiseSerializerRO(serializers.ModelSerializer[Franchise]):
  """Serializer to retrieve or list Franchises."""

  name = BlondeCharField(max_length=80, allow_blank=False)
  scraper = serializers.SlugRelatedField(
      queryset=Scraper.objects.all(),
      slug_field="name",
  )

  class Meta:
    model = Franchise
    fields = ("name", "scraper")
