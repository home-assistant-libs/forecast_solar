"""Example of how to use multiple planes with the Forecast.Solar API."""

import asyncio
from datetime import UTC, datetime, timedelta
from pprint import pprint  # noqa: F401

from forecast_solar import ForecastSolar, ForecastSolarRatelimitError, Plane


async def main() -> None:
    """Get an estimate from the Forecast.Solar API using multiple planes.

    This example demonstrates how to configure multiple solar panel arrays
    (planes) with different orientations. Using multiple planes requires both
    an API key and a Personal Plus or higher subscription.
    """
    async with ForecastSolar(
        api_key="your-api-key",  # API key is required for multiple planes
        latitude=52.16,
        longitude=4.47,
        # First plane configuration (main roof)
        declination=20,
        azimuth=10,
        kwp=2.160,
        # Additional planes (e.g., garage roof, secondary array)
        planes=[
            Plane(declination=30, azimuth=-90, kwp=1.5),  # West-facing plane
            Plane(declination=30, azimuth=90, kwp=1.5),  # East-facing plane
        ],
    ) as forecast:
        try:
            estimate = await forecast.estimate()
        except ForecastSolarRatelimitError as err:
            print("Ratelimit reached")
            print(f"Rate limit resets at {err.reset_at}")
            reset_period = err.reset_at - datetime.now(UTC)
            # Strip microseconds as they are not informative
            reset_period -= timedelta(microseconds=reset_period.microseconds)
            print(f"That's in {reset_period}")
            return

        # Uncomment this if you want to see what's in the estimate arrays
        # pprint(dataclasses.asdict(estimate))
        print()
        print(f"energy_production_today: {estimate.energy_production_today}")
        print(
            "energy_production_today_remaining: "
            f"{estimate.energy_production_today_remaining}"
        )
        print(
            f"power_highest_peak_time_today: {estimate.power_highest_peak_time_today}"
        )
        print(f"energy_production_tomorrow: {estimate.energy_production_tomorrow}")
        print(
            "power_highest_peak_time_tomorrow: "
            f"{estimate.power_highest_peak_time_tomorrow}"
        )
        print()
        print(f"power_production_now: {estimate.power_production_now}")
        print(
            "power_production in 1 hour: "
            f"{estimate.power_production_at_time(estimate.now() + timedelta(hours=1))}"
        )
        print(
            "power_production in 6 hours: "
            f"{estimate.power_production_at_time(estimate.now() + timedelta(hours=6))}"
        )
        print(
            "power_production in 12 hours: "
            f"{estimate.power_production_at_time(estimate.now() + timedelta(hours=12))}"
        )
        print(
            "power_production in 24 hours: "
            f"{estimate.power_production_at_time(estimate.now() + timedelta(hours=24))}"
        )
        print()
        print(f"energy_current_hour: {estimate.energy_current_hour}")
        print(f"energy_production next hour: {estimate.sum_energy_production(1)}")
        print(f"energy_production next 6 hours: {estimate.sum_energy_production(6)}")
        print(f"energy_production next 12 hours: {estimate.sum_energy_production(12)}")
        print(f"energy_production next 24 hours: {estimate.sum_energy_production(24)}")
        print(f"timezone: {estimate.timezone}")
        print(f"account_type: {estimate.account_type}")
        print(forecast.ratelimit)


if __name__ == "__main__":
    asyncio.run(main())
