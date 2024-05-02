"""Tests for Forecast.Solar."""

# pylint: disable=protected-access

import pytest
from aresponses import ResponsesMockServer

from forecast_solar import (
    ForecastSolar,
    ForecastSolarError,
)

from . import load_fixtures


async def test_json_request(
    aresponses: ResponsesMockServer,
    forecast_client: ForecastSolar,
) -> None:
    """Test JSON response is handled correctly."""
    aresponses.add(
        "api.forecast.solar",
        "/test",
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
    response = await forecast_client._request("test")
    assert response is not None
    await forecast_client.close()


async def test_internal_session(aresponses: ResponsesMockServer) -> None:
    """Test internal session is handled correctly."""
    aresponses.add(
        "api.forecast.solar",
        "/test",
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
    async with ForecastSolar(
        latitude=52.16,
        longitude=4.47,
        declination=20,
        azimuth=10,
        kwp=2.160,
        damping=0,
        horizon="0,0,0,10,10,20,20,30,30",
    ) as client:
        await client._request("test")


async def test_content_type(
    aresponses: ResponsesMockServer,
    forecast_client: ForecastSolar,
) -> None:
    """Test content type error handling."""
    aresponses.add(
        "api.forecast.solar",
        "/test",
        "GET",
        aresponses.Response(
            status=200,
            headers={
                "Content-Type": "blabla/blabla",
                "X-Ratelimit-Limit": "10",
                "X-Ratelimit-Period": "1",
            },
        ),
    )
    with pytest.raises(ForecastSolarError):
        assert await forecast_client._request("test")
