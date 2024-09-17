"""Test the models."""

from datetime import datetime

import pytest
from aresponses import ResponsesMockServer
from syrupy.assertion import SnapshotAssertion

from forecast_solar import AccountType, Estimate, ForecastSolar

from . import load_fixtures


@pytest.mark.freeze_time("2024-04-26T12:00:00+02:00")
async def test_estimated_forecast(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    forecast_client: ForecastSolar,
) -> None:
    """Test estimated forecast."""
    aresponses.add(
        "api.forecast.solar",
        "/estimate/52.16/4.47/20/10/2.16",
        "GET",
        aresponses.Response(
            status=200,
            headers={
                "Content-Type": "application/json",
                "X-Ratelimit-Limit": "10",
                "X-Ratelimit-Period": "1",
            },
            text=load_fixtures("forecast.json"),
        ),
    )
    forecast: Estimate = await forecast_client.estimate()
    assert forecast == snapshot
    assert forecast.timezone == "Europe/Amsterdam"
    assert forecast.account_type == AccountType.PUBLIC

    assert forecast.energy_production_today == 6660
    assert forecast.energy_production_tomorrow == 5338

    assert forecast.power_production_now == 773
    assert forecast.energy_production_today_remaining == 4144
    assert forecast.energy_current_hour == 821

    assert forecast.power_highest_peak_time_today == datetime.fromisoformat(
        "2024-04-26T11:00:00+02:00"
    )
    assert forecast.power_highest_peak_time_tomorrow == datetime.fromisoformat(
        "2024-04-27T12:00:00+02:00"
    )

    assert forecast.sum_energy_production(1) == 742
    assert forecast.sum_energy_production(6) == 3093
    assert forecast.sum_energy_production(12) == 3323
    assert forecast.sum_energy_production(24) == 5633


@pytest.mark.freeze_time("2024-04-27T07:00:00+02:00")
async def test_estimated_forecast_with_subscription(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    forecast_key_client: ForecastSolar,
) -> None:
    """Test estimated forecast."""
    aresponses.add(
        "api.forecast.solar",
        "/myapikey/estimate/52.16/4.47/20/10/2.16",
        "GET",
        aresponses.Response(
            status=200,
            headers={
                "Content-Type": "application/json",
                "X-Ratelimit-Limit": "60",
                "X-Ratelimit-Period": "3600",
            },
            text=load_fixtures("forecast_personal.json"),
        ),
    )
    forecast: Estimate = await forecast_key_client.estimate()
    assert forecast == snapshot
    assert forecast.timezone == "Europe/Amsterdam"
    assert forecast.account_type == AccountType.PERSONAL

    assert forecast.energy_production_today == 5788
    assert forecast.energy_production_tomorrow == 7507

    assert forecast.power_production_now == 92
    assert forecast.energy_production_today_remaining == 5783
    assert forecast.energy_current_hour == 96

    assert forecast.power_highest_peak_time_today == datetime.fromisoformat(
        "2024-04-27T13:30:00+02:00"
    )
    assert forecast.power_highest_peak_time_tomorrow == datetime.fromisoformat(
        "2024-04-28T14:30:00+02:00"
    )

    assert forecast.sum_energy_production(1) == 216
    assert forecast.sum_energy_production(6) == 2802
    assert forecast.sum_energy_production(12) == 5582
    assert forecast.sum_energy_production(24) == 5784


@pytest.mark.freeze_time("2024-04-27T07:00:00+02:00")
async def test_estimated_forecast_with_subscription_and_actual_value(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    forecast_key_client: ForecastSolar,
) -> None:
    """Test estimated forecast."""
    aresponses.add(
        "api.forecast.solar",
        "/myapikey/estimate/52.16/4.47/20/10/2.16",
        "GET",
        aresponses.Response(
            status=200,
            headers={
                "Content-Type": "application/json",
                "X-Ratelimit-Limit": "60",
                "X-Ratelimit-Period": "3600",
            },
            text=load_fixtures("forecast_personal.json"),
        ),
    )
    forecast: Estimate = await forecast_key_client.estimate(actual=5800)
    assert forecast == snapshot
    assert forecast.timezone == "Europe/Amsterdam"
    assert forecast.account_type == AccountType.PERSONAL

    assert forecast.energy_production_today == 5788
    assert forecast.energy_production_tomorrow == 7507

    assert forecast.sum_energy_production(1) == 216
    assert forecast.sum_energy_production(6) == 2802
    assert forecast.sum_energy_production(12) == 5582
    assert forecast.sum_energy_production(24) == 5784


async def test_api_key_validation(
    aresponses: ResponsesMockServer,
    forecast_key_client: ForecastSolar,
) -> None:
    """Test API key validation."""
    aresponses.add(
        "api.forecast.solar",
        "/myapikey/info",
        "GET",
        aresponses.Response(
            status=200,
            headers={
                "Content-Type": "application/json",
                "X-Ratelimit-Limit": "10",
                "X-Ratelimit-Period": "1",
            },
            text=load_fixtures("validate_key.json"),
        ),
    )
    assert await forecast_key_client.validate_api_key() is True


async def test_plane_validation(
    aresponses: ResponsesMockServer,
    forecast_client: ForecastSolar,
) -> None:
    """Test plane validation."""
    aresponses.add(
        "api.forecast.solar",
        "/check/52.16/4.47/20/10/2.16",
        "GET",
        aresponses.Response(
            status=200,
            headers={
                "Content-Type": "application/json",
                "X-Ratelimit-Limit": "10",
                "X-Ratelimit-Period": "1",
            },
            text=load_fixtures("validate_plane.json"),
        ),
    )
    assert await forecast_client.validate_plane() is True
