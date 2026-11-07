"""Text exceptions raised by the Forecast.Solar API client."""

import json

import pytest
from aresponses import ResponsesMockServer

from forecast_solar import (
    ForecastSolar,
    ForecastSolarAuthenticationError,
    ForecastSolarConfigError,
    ForecastSolarConnectionError,
    ForecastSolarRatelimitError,
    ForecastSolarRequestError,
)

from . import load_fixtures


async def test_status_400(
    aresponses: ResponsesMockServer,
    forecast_client: ForecastSolar,
) -> None:
    """Test response status 400."""
    aresponses.add(
        "api.forecast.solar",
        "/test",
        "GET",
        aresponses.Response(
            status=400,
            headers={
                "Content-Type": "application/json",
                "X-Ratelimit-Limit": "10",
                "X-Ratelimit-Period": "1",
            },
            text=load_fixtures("forecast.json"),
        ),
    )
    with pytest.raises(ForecastSolarRequestError):
        assert await forecast_client._request("test")


async def test_status_401(
    aresponses: ResponsesMockServer,
    forecast_client: ForecastSolar,
) -> None:
    """Test response status 401 or 403."""
    aresponses.add(
        "api.forecast.solar",
        "/test",
        "GET",
        aresponses.Response(
            status=401,
            headers={
                "Content-Type": "application/json",
                "X-Ratelimit-Limit": "10",
                "X-Ratelimit-Period": "1",
            },
            text=load_fixtures("forecast.json"),
        ),
    )
    with pytest.raises(ForecastSolarAuthenticationError):
        assert await forecast_client._request("test")


async def test_status_422(
    aresponses: ResponsesMockServer,
    forecast_client: ForecastSolar,
) -> None:
    """Test response status 422."""
    aresponses.add(
        "api.forecast.solar",
        "/test",
        "GET",
        aresponses.Response(
            status=422,
            headers={
                "Content-Type": "application/json",
                "X-Ratelimit-Limit": "10",
                "X-Ratelimit-Period": "1",
            },
            text=load_fixtures("forecast.json"),
        ),
    )
    with pytest.raises(ForecastSolarConfigError):
        assert await forecast_client._request("test")


async def test_status_429(
    aresponses: ResponsesMockServer,
    forecast_client: ForecastSolar,
) -> None:
    """Test response status 429."""
    aresponses.add(
        "api.forecast.solar",
        "/test",
        "GET",
        aresponses.Response(
            status=429,
            headers={
                "Content-Type": "application/json",
                "X-Ratelimit-Limit": "10",
                "X-Ratelimit-Period": "1",
            },
            text=load_fixtures("ratelimit.json"),
        ),
    )
    with pytest.raises(ForecastSolarRatelimitError):
        assert await forecast_client._request("test")


async def test_status_429_without_retry_at(
    aresponses: ResponsesMockServer,
    forecast_client: ForecastSolar,
) -> None:
    """Test response status 429 when ratelimit has no retry-at key."""
    aresponses.add(
        "api.forecast.solar",
        "/test",
        "GET",
        aresponses.Response(
            status=429,
            headers={
                "Content-Type": "application/json",
                "X-Ratelimit-Limit": "10",
                "X-Ratelimit-Period": "1",
            },
            text=json.dumps(
                {
                    "message": {
                        "code": 429,
                        "text": "Rate limit for API calls reached.",
                        "ratelimit": {
                            "zone": "YOUR IP ADDRESS",
                            "period": 3600,
                            "limit": 12,
                        },
                    }
                }
            ),
        ),
    )
    with pytest.raises(ForecastSolarRatelimitError) as exc_info:
        assert await forecast_client._request("test")
    assert exc_info.value.reset_at is None


def test_ratelimit_error_without_ratelimit_key() -> None:
    """Test rate limit error without a ratelimit object at all."""
    err = ForecastSolarRatelimitError(
        {"code": 429, "text": "Rate limit for API calls reached."}
    )
    assert err.reset_at is None


async def test_status_502(
    aresponses: ResponsesMockServer,
    forecast_client: ForecastSolar,
) -> None:
    """Test response status 502 or 503."""
    aresponses.add(
        "api.forecast.solar",
        "/test",
        "GET",
        aresponses.Response(
            status=502,
            headers={
                "Content-Type": "application/json",
                "X-Ratelimit-Limit": "10",
                "X-Ratelimit-Period": "1",
            },
            text=load_fixtures("forecast.json"),
        ),
    )
    with pytest.raises(ForecastSolarConnectionError):
        assert await forecast_client._request("test")


async def test_status_404(
    aresponses: ResponsesMockServer,
    forecast_client: ForecastSolar,
) -> None:
    """Test response status 404."""
    aresponses.add(
        "api.forecast.solar",
        "/test",
        "GET",
        aresponses.Response(
            status=404,
            headers={
                "Content-Type": "application/json",
            },
            text='{"message": {"code": 404, "text": "Not Found"}}',
        ),
    )
    with pytest.raises(ForecastSolarRequestError):
        assert await forecast_client._request("test")
