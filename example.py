import asyncio
import dataclasses
from datetime import datetime, timezone, timedelta
from pprint import pprint

from forecast_solar import ForecastSolar, ForecastSolarRatelimit


async def main():
    """Simple function to test the output."""
    async with ForecastSolar(
        latitude=52.16,
        longitude=4.47,
        declination=20,
        azimuth=10,
        kwp=2.160,
        damping=0,
        horizon="0,0,0,10,10,20,20,30,30",
    ) as forecast:
        try:
            estimate = await forecast.estimate()
        except ForecastSolarRatelimit as err:
            print("Ratelimit reached")
            print(f"Rate limit resets at {err.reset_at}")
            reset_period = err.reset_at - datetime.now(timezone.utc)
            # Strip microseconds as they are not informative
            reset_period -= timedelta(microseconds=reset_period.microseconds)
            print(f"That's in {reset_period}")
            return

        # Uncomment this if you want to see what's in the estimate arrays
        # pprint(dataclasses.asdict(estimate))
        print()
        print(f"energy_production_today: {estimate.energy_production_today}")
        print(
            f"energy_production_today_remaining: {estimate.energy_production_today_remaining}"
        )
        print(
            f"power_highest_peak_time_today: {estimate.power_highest_peak_time_today}"
        )
        print(f"energy_production_tomorrow: {estimate.energy_production_tomorrow}")
        print(
            f"power_highest_peak_time_tomorrow: {estimate.power_highest_peak_time_tomorrow}"
        )
        print()
        print(f"power_production_now: {estimate.power_production_now}")
        print(
            f"power_production in 1 hour: {estimate.power_production_at_time(estimate.now() + timedelta(hours=1))}"
        )
        print(
            f"power_production in 6 hours: {estimate.power_production_at_time(estimate.now() + timedelta(hours=6))}"
        )
        print(
            f"power_production in 12 hours: {estimate.power_production_at_time(estimate.now() + timedelta(hours=12))}"
        )
        print(
            f"power_production in 24 hours: {estimate.power_production_at_time(estimate.now() + timedelta(hours=24))}"
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
