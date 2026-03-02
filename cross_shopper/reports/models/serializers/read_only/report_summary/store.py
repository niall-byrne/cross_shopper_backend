"""Serializer for Store instances in summarized results of Reports."""

from rest_framework import serializers
from stores.models import Store


class ReportSummaryStoreSerializerRO(serializers.ModelSerializer[Store]):
  """Serializer for Store instances in summarized results of Reports."""

  franchise_name = serializers.CharField(source='franchise.name')
  postal_code = serializers.CharField(source='address.locality.postal_code')

  class Meta:
    model = Store
    fields = ('id', 'franchise_name', 'postal_code')
