"""Default value for a Price model's week field."""

from datetime import timedelta

from django.apps import apps
from django.utils import timezone


def default_pricing_week() -> int:
  """Generate the current isoweek offset by the pricing day."""
  day_of_week_for_pricing = apps.get_model(
      "pricing.Price"
  ).DAY_OF_WEEK_FOR_PRICING
  today = timezone.now()
  if today.weekday() >= day_of_week_for_pricing:
    if (today + timedelta(weeks=1)).year > today.year:
      return 1
    else:
      return today.isocalendar().week + 1
  return today.isocalendar().week
