"""Data models for the Forecast.Solar API."""
from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from enum import Enum
from typing import Any

from aiohttp import ClientResponse

if sys.version_info[:2] >= (3, 9):
    import zoneinfo
else:
    from backports import zoneinfo


def _timed_value(time_at: datetime, data: dict[datetime, int]) -> int | None:
    """Return the value for a specific time.

    Args:
        time_at: The time to look for.
        data: The data to look in.

    Returns:
        The value for the time, or None if not found.
    """
    value = None
    for timestamp, cur_value in data.items():
        if timestamp > time_at:
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
        """Get the API timezone information.

        Returns:
            The API timezone information.
        """
        return self.api_timezone

    @property
    def account_type(self) -> AccountType:
        """Get the account type information.

        Returns:
            The API account_type information.
        """
        if self.api_rate_limit == 60:
            return AccountType.PERSONAL
        if self.api_rate_limit == 5:
            return AccountType.PROFESSIONAL
        return AccountType.PUBLIC

    @property
    def energy_production_today(self) -> int:
        """Estimated energy produced for today.

        Returns:
            The estimated energy production for today.
        """
        return self.day_production(self.now().date())

    @property
    def energy_production_tomorrow(self) -> int:
        """Estimated energy produced for tomorrow.

        Returns:
            The estimated energy production for tomorrow.
        """
        return self.day_production(self.now().date() + timedelta(days=1))

    @property
    def power_production_now(self) -> int:
        """Estimated power production right now.

        Returns:
            The estimated power production right now.
        """
        return self.power_production_at_time(self.now())

    @property
    def power_highest_peak_time_today(self) -> datetime | None:
        """Highest power production moment today.

        Returns:
            The datetime with the highest power production moment today.
        """
        return self.peak_production_time(self.now().date())

    @property
    def power_highest_peak_time_tomorrow(self) -> datetime | None:
        """Get the datetime with highest power production moment for tomorrow.

        Returns:
            The datetime with the highest power production moment tomorrow.
        """
        return self.peak_production_time(self.now().date() + timedelta(days=1))

    @property
    def energy_current_hour(self) -> int:
        """Get the estimated energy production for the current hour.

        Returns:
            The estimated energy production for the current hour.
        """
        return _timed_value(self.now(), self.wh_hours) or 0

    def day_production(self, specific_date: date) -> int:
        """Get the day production.

        Args:
            specific_date: The date to get the production for.

        Returns:
            The day production for the given date.
        """
        for timestamp, production in self.wh_days.items():
            if timestamp.date() == specific_date:
                return production

        return 0

    def now(self) -> datetime:
        """Get the current timestamp in the API timezone.

        Returns:
            The current timestamp in the API timezone.
        """
        return datetime.now(tz=zoneinfo.ZoneInfo(self.api_timezone))

    def peak_production_time(self, specific_date: date) -> datetime | None:
        """Production peak time on a specific date.

        Args:
            specific_date: The date to get the peak time for.

        Returns:
            The datetime with the highest power production on the given date.
        """
        value = max(
            (watt for date, watt in self.watts.items() if date.date() == specific_date),
            default=None,
        )
        for (timestamp, watt) in self.watts.items():
            if watt == value:
                return timestamp
        return None

    def power_production_at_time(self, time: datetime) -> int:
        """Estimated power production at a specific time.

        Args:
            time: The time to get the power production for.

        Returns:
            The estimated power production at the given time.
        """
        return _timed_value(time, self.watts) or 0

    def sum_energy_production(self, period_hours: int) -> int:
        """Sum of the energy production.

        Args:
            period_hours: The number of hours to sum.

        Returns:
            The sum of the energy production for the last period_hours.
        """
        now = self.now().replace(minute=59, second=59)
        until = now + timedelta(hours=period_hours)

        total = 0

        for timestamp, energy_wh in self.wh_hours.items():
            # Skip all dates until this hour
            if timestamp < now:
                continue

            if timestamp > until:
                break

            total += energy_wh

        return total

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Estimate:
        """Estimate object from a Forecast.Solar API response.

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
        """Initialize rate limit object from response.

        Args:
            response: The response from the Forecast.Solar API.

        Returns:
            Ratelimit object.
        """
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
