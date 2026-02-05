"""Custom admin for the django-address app."""

from address.models import Address, Locality, State
from django.contrib import admin


class AddressAdmin(admin.ModelAdmin[Address]):
  ordering = (
      "locality__state__country",
      "locality__state",
      "locality__name",
      "route",
      "street_number",
  )


admin.site.unregister(Address)
admin.site.unregister(Locality)
admin.site.unregister(State)

admin.site.register(
    Address,
    AddressAdmin,
    list_filter=(
        "locality__name",
        "locality__state",
        "locality__state__country",
    )
)
admin.site.register(Locality, list_filter=("state__name", "state__country"))
admin.site.register(State, list_filter=("country",))
