"""Custom model admins for the django-address app."""

from address.models import Address, Locality, State
from django.contrib import admin
from utilities.admin.django_address.address import AddressAdmin
from utilities.admin.django_address.locality import LocalityAdmin

admin.site.unregister(Address)
admin.site.unregister(Locality)
admin.site.unregister(State)

admin.site.register(Address, AddressAdmin)
admin.site.register(Locality, LocalityAdmin)
admin.site.register(State)
