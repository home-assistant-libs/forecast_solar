"""Data models for the Forecast.Solar API."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, date
from enum import Enum
from typing import Any
import sys

if sys.version_info[:2] >= (3, 9):
    import zoneinfo
else:
    from backports import zoneinfo

from aiohttp import ClientResponse


def _timed_value(at: datetime, data: dict[datetime, int]) -> int | None:
    """Return the value for a specific time."""
    value = None
    for timestamp, cur_value in data.items():
        if timestamp > at:
            return value
        value = cur_value

    return None


class AccountType(str, Enum):
    """Enumeration representing the Forecast.Solar account type."""

    PUBLIC = "public"
    PERSONAL = "personal"
    PROFESSIONAL = "professional"


@dataclass
class Estimate:
    """Object holding estimate forecast results from Forecast.Solar.

    Attributes:
        wh_days: Estimated solar energy production per day.
        wh_hours: Estimated solar energy production per hour.
        watts: Estimated solar power output per hour.
    """

    wh_days: dict[datetime, int]
    wh_hours: dict[datetime, int]
    watts: dict[datetime, int]
    api_rate_limit: int
    api_timezone: str

    @property
    def timezone(self) -> str:
        """Return API timezone information."""
        return self.api_timezone

    @property
    def account_type(self) -> AccountType:
        """Return API account_type information."""
        if self.api_rate_limit == 60:
            return AccountType.PERSONAL
        if self.api_rate_limit == 5:
            return AccountType.PROFESSIONAL
        return AccountType.PUBLIC

    @property
    def energy_production_today(self) -> int:
        """Return estimated energy produced today."""
        return self.day_production(self.now().date())

    @property
    def energy_production_tomorrow(self) -> int:
        """Return estimated energy produced today."""
        return self.day_production(self.now().date() + timedelta(days=1))

    @property
    def power_production_now(self) -> int:
        """Return estimated power production right now."""
        return self.power_production_at_time(self.now())

    @property
    def power_highest_peak_time_today(self) -> datetime:
        """Return datetime with highest power production moment today."""
        return self.peak_production_time(self.now().date())

    @property
    def power_highest_peak_time_tomorrow(self) -> datetime:
        """Return datetime with highest power production moment tomorrow."""
        return self.peak_production_time(self.now().date() + timedelta(days=1))

    @property
    def energy_current_hour(self) -> int:
        """Return the estimated energy production for the current hour."""
        return _timed_value(self.now(), self.wh_hours) or 0

    def day_production(self, specific_date: date) -> int:
        """Return the day production."""
        for timestamp, production in self.wh_days.items():
            if timestamp.date() == specific_date:
                return production

        return 0

    def now(self) -> datetime:
        """Return the current timestamp in the API timezone."""
        return datetime.now(tz=zoneinfo.ZoneInfo(self.api_timezone))

    def peak_production_time(self, specific_date: date) -> datetime:
        """Return the peak time on a specific date."""
        value = max(
            (watt for date, watt in self.watts.items() if date.date() == specific_date),
            default=None,
        )
        for (
            timestamp,
            watt,
        ) in self.watts.items():
            if watt == value:
                return timestamp

    def power_production_at_time(self, time: datetime) -> int:
        """Return estimated power production at a specific time."""
        return _timed_value(time, self.watts) or 0

    def sum_energy_production(self, period_hours: int) -> int:
        """Return the sum of the energy production."""
        now = self.now().replace(minute=59, second=59)
        until = now + timedelta(hours=period_hours)

        total = 0

        for timestamp, wh in self.wh_hours.items():
            # Skip all dates until this hour
            if timestamp < now:
                continue

            if timestamp > until:
                break

            total += wh

        return total

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Estimate:
        """Return a Estimate object from a Forecast.Solar API response.

        Converts a dictionary, obtained from the Forecast.Solar API into
        a Estimate object.

        Args:
            data: The estimate response from the Forecast.Solar API.

        Returns:
            An Estimate object.
        """
        previous_value = 0
        wh_hours = {}

        for timestamp, energy in data["result"]["watt_hours"].items():
            timestamp = datetime.fromisoformat(timestamp)

            # If we get a reset
            if energy < previous_value:
                previous_value = 0

            wh_hours[timestamp] = energy - previous_value
            previous_value = energy

        return cls(
            wh_days={
                datetime.fromisoformat(d): e
                for d, e in data["result"]["watt_hours_day"].items()
            },
            wh_hours=wh_hours,
            watts={
                datetime.fromisoformat(d): w for d, w in data["result"]["watts"].items()
            },
            api_rate_limit=data["message"]["ratelimit"]["limit"],
            api_timezone=data["message"]["info"]["timezone"],
        )


@dataclass
class Ratelimit:
    """Information about the current rate limit."""

    call_limit: int
    remaining_calls: int
    period: int
    retry_at: datetime | None

    @classmethod
    def from_response(cls, response: ClientResponse) -> Ratelimit:
        """Initialize rate limit object from response."""
        # The documented headers do not match the returned headers
        # https://doc.forecast.solar/doku.php?id=api#headers
        limit = int(response.headers["X-Ratelimit-Limit"])
        period = int(response.headers["X-Ratelimit-Period"])

        # Remaining is not there if we exceeded limit
        remaining = int(response.headers.get("X-Ratelimit-Remaining", 0))

        if "X-Ratelimit-Retry-At" in response.headers:
            retry_at = datetime.fromisoformat(response.headers["X-Ratelimit-Retry-At"])
        else:
            retry_at = None

        return cls(limit, remaining, period, retry_at)
