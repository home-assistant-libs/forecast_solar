"""Data models for the Forecast.Solar API."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any


@dataclass
class Estimate:
    """Object holding estimate forecast results from Forecast.Solar.

    Attributes:
        kwh_days: Estimated solar energy production per day.
        kwh_hours: Estimated solar energy production per hour.
        watts: Estimated solar power output per hour.
    """

    kwh_days: dict[datetime, float]
    kwh_hours: dict[datetime, float]
    watts: dict[datetime, int]
    api_timezone: str

    @property
    def timezone(self) -> str:
        """Return API timezone information."""
        return self.api_timezone

    @property
    def energy_production_today(self) -> float:
        """Return estimated energy produced today."""
        return list(self.kwh_days.values())[0]

    @property
    def energy_production_tomorrow(self) -> float:
        """Return estimated energy produced today."""
        return list(self.kwh_days.values())[1]

    @property
    def power_production_now(self) -> int:
        """Return estimated power production right now."""
        value = 0
        now = datetime.now(tz=timezone.utc)
        for date, watt in self.watts.items():
            if date > now:
                return value
            value = watt
        return 0

    @property
    def power_highest_peak_time_today(self) -> datetime:
        """Return datetime with highest power production moment today."""
        now = datetime.now(tz=timezone.utc).replace(minute=59, second=59)
        value = max(watt for date, watt in self.watts.items() if date.day == now.day)
        for (
            date,
            watt,
        ) in self.watts.items():
            if watt == value:
                return date

    @property
    def power_highest_peak_time_tomorrow(self) -> datetime:
        """Return datetime with highest power production moment tomorrow."""
        nxt = datetime.now(tz=timezone.utc).replace(minute=59, second=59) + timedelta(
            hours=24
        )
        value = max(watt for date, watt in self.watts.items() if date.day == nxt.day)
        for (
            date,
            watt,
        ) in self.watts.items():
            if watt == value:
                return date

    @property
    def power_production_next_hour(self) -> int:
        """Return estimated power production next hour."""
        nxt = datetime.now(tz=timezone.utc).replace(minute=59, second=59) + timedelta(
            hours=1
        )
        value = 0
        for date, watt in self.watts.items():
            if date > nxt:
                return value
            value = watt
        return 0

    @property
    def power_production_next_6hours(self) -> int:
        """Return estimated power production +6 hours."""
        nxt = datetime.now(tz=timezone.utc).replace(minute=59, second=59) + timedelta(
            hours=6
        )
        value = 0
        for date, watt in self.watts.items():
            if date > nxt:
                return value
            value = watt
        return 0

    @property
    def power_production_next_12hours(self) -> int:
        """Return estimated power production +12 hours."""
        nxt = datetime.now(tz=timezone.utc).replace(minute=59, second=59) + timedelta(
            hours=12
        )
        value = 0
        for date, watt in self.watts.items():
            if date > nxt:
                return value
            value = watt
        return 0

    @property
    def power_production_next_24hours(self) -> int:
        """Return estimated power production +24 hours."""
        nxt = datetime.now(tz=timezone.utc).replace(minute=59, second=59) + timedelta(
            hours=24
        )
        value = 0
        for date, watt in self.watts.items():
            if date > nxt:
                return value
            value = watt
        return 0

    @property
    def energy_current_hour(self) -> float:
        """Return the estimated energy production for the current hour."""
        now = datetime.now(tz=timezone.utc).replace(minute=59, second=59)
        for date, kwh in self.kwh_hours.items():
            if date > now and now.day == date.day:
                return kwh
        return 0

    @property
    def energy_next_hour(self) -> float:
        """Return the estimated energy production for the next hour."""
        nxt = datetime.now(tz=timezone.utc).replace(minute=59, second=59) + timedelta(
            hours=1
        )
        for date, kwh in self.kwh_hours.items():
            if date > nxt and date.day == nxt.day:
                return kwh
        return 0

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Estimate:
        """Return a Estimate object from a Forecast.Solar API response.

        Converts a dictionary, obtained from the Forecast.Solar API into
        a Estimate object.

        Args:
            data: The estimate response from the Forecast.Solar API.

        Returns:
            An estimate object.
        """
        previous_value = 0
        kwh_hours = {}

        for date, energy in data["result"]["watt_hours"].items():
            date = datetime.fromisoformat(date).astimezone(timezone.utc)
            kwh_hours[date] = (energy - previous_value) / 1000
            previous_value = energy

        return Estimate(
            kwh_days={
                datetime.fromisoformat(d).astimezone(timezone.utc): (e / 1000)
                for d, e in data["result"]["watt_hours_day"].items()
            },
            kwh_hours=kwh_hours,
            watts={
                datetime.fromisoformat(d).astimezone(timezone.utc): w
                for d, w in data["result"]["watts"].items()
            },
            api_timezone=data["message"]["info"]["timezone"],
        )
