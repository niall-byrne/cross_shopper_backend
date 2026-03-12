"""Default value for a Price model's year field."""

from datetime import timedelta

from django.utils import timezone
from pricing.constants import DAY_OF_WEEK_FOR_PRICING


def default_pricing_year() -> int:
  """Generate the current year."""
  today = timezone.now()
  if today.weekday() >= DAY_OF_WEEK_FOR_PRICING:
    if (today + timedelta(weeks=1)).year > today.year:
      return today.year + 1
  return today.year
