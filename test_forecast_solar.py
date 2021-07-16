import asyncio
from datetime import datetime, timezone, timedelta

from forecast_solar import Estimate, ForecastSolar, ForecastSolarRatelimit


async def main():
    """Simple function to test the output."""
    async with ForecastSolar(
        latitude=52.16, longitude=4.47, declination=20, azimuth=10, kwp=2.160, damping=0
    ) as forecast:
        try:
            estimate: Estimate = await forecast.estimate()
        except ForecastSolarRatelimit as err:
            print("Ratelimit reached")
            print(f"Rate limit resets at {err.reset_at}")
            reset_period = err.reset_at - datetime.now(timezone.utc)
            # Strip microseconds as they are not informative
            reset_period -= timedelta(microseconds=reset_period.microseconds)
            print(f"That's in {reset_period}")
            return

        print(estimate)
        print()
        print(f"energy_production_today: {estimate.energy_production_today}")
        print(f"energy_production_tomorrow: {estimate.energy_production_tomorrow}")
        print(f"power_production_now: {estimate.power_production_now}")
        print(
            f"power_highest_peak_time_today: {estimate.power_highest_peak_time_today}"
        )
        print(
            f"power_highest_peak_time_tomorrow: {estimate.power_highest_peak_time_tomorrow}"
        )
        print(f"power_production_next_hour: {estimate.power_production_next_hour}")
        print(f"power_production_next_6hours: {estimate.power_production_next_6hours}")
        print(
            f"power_production_next_12hours: {estimate.power_production_next_12hours}"
        )
        print(
            f"power_production_next_24hours: {estimate.power_production_next_24hours}"
        )
        print(f"energy_current_hour: {estimate.energy_current_hour}")
        print(f"energy_next_hour: {estimate.energy_next_hour}")
        print(f"timezone: {estimate.timezone}")
        print(forecast.ratelimit)


if __name__ == "__main__":
    asyncio.run(main())
