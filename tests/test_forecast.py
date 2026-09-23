"""Tests for Forecast.Solar."""

# pylint: disable=protected-access

import re
from datetime import date

import pytest
from aiohttp import web
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


async def test_estimate_requests_local_time(
    aresponses: ResponsesMockServer,
    forecast_client: ForecastSolar,
) -> None:
    """Test the estimate is requested in the local timezone.

    With ``time=utc`` the API buckets ``watt_hours_day`` by UTC date, which
    shifts production across days for non-UTC sites (see #294). Requesting
    iso8601 keeps the day buckets aligned with the site timezone.
    """
    captured: dict[str, str] = {}

    async def handler(request: web.Request) -> web.Response:
        captured["query"] = request.query.get("time", "")
        return web.Response(
            status=200,
            headers={
                "Content-Type": "application/json",
                "X-Ratelimit-Limit": "10",
                "X-Ratelimit-Period": "1",
            },
            text=load_fixtures("forecast.json"),
        )

    aresponses.add(
        "api.forecast.solar",
        re.compile(r"/estimate/.+"),
        "GET",
        handler,
    )

    await forecast_client.estimate()
    assert captured["query"] == "iso8601"


async def test_estimate_day_buckets_follow_local_timezone(
    aresponses: ResponsesMockServer,
    forecast_client: ForecastSolar,
) -> None:
    """Verify day buckets are aligned to the site timezone, not UTC.

    Regression test for #294. With ``time=utc`` the API buckets
    ``watt_hours_day`` by UTC date, which shifts production across days for
    non-UTC sites. Requesting ``iso8601`` keeps the returned keys on local
    dates, so ``energy_production_today`` reads the intended bucket.

    The fixture is anchored on the Europe/Amsterdam (UTC+02:00) local date
    boundary: 22:00 local is 20:00 UTC, so the two dating schemes disagree on
    which bucket that hour belongs to.
    """
    captured: dict[str, str] = {}

    async def handler(request: web.Request) -> web.Response:
        captured["query"] = request.query.get("time", "")
        return web.Response(
            status=200,
            headers={
                "Content-Type": "application/json",
                "X-Ratelimit-Limit": "10",
                "X-Ratelimit-Period": "1",
            },
            text=load_fixtures("forecast_timezone_boundary.json"),
        )

    aresponses.add(
        "api.forecast.solar",
        re.compile(r"/estimate/.+"),
        "GET",
        handler,
    )

    estimate = await forecast_client.estimate()

    assert captured["query"] == "iso8601"
    assert estimate.api_timezone == "Europe/Amsterdam"
    # The returned keys are local dates, so a site at UTC+02:00 reads its own
    # day bucket rather than the UTC-shifted one.
    assert estimate.day_production(date(2024, 4, 26)) == 1000
    assert estimate.day_production(date(2024, 4, 27)) == 2000
