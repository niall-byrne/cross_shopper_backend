"""Default value for a Price model's year field."""

from datetime import timedelta

from django.apps import apps
from django.utils import timezone


def default_pricing_year() -> int:
  """Generate the current year."""
  day_of_week_for_pricing = apps.get_model(
      'pricing.Price'
  ).DAY_OF_WEEK_FOR_PRICING
  today = timezone.now()
  if today.weekday() >= day_of_week_for_pricing:
    if (today + timedelta(weeks=1)).year > today.year:
      return today.year + 1
  return today.year
