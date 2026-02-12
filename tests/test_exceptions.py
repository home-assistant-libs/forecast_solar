"""Text exceptions raised by the Forecast.Solar API client."""

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
