"""Tests for Forecast.Solar."""
# pylint: disable=protected-access
import aiohttp
import pytest
from aresponses import ResponsesMockServer

from forecast_solar import ForecastSolar, ForecastSolarError

from . import load_fixtures


@pytest.mark.asyncio
async def test_json_request(aresponses: ResponsesMockServer) -> None:
    """Test JSON response is handled correctly."""
    aresponses.add(
        "api.forecast.solar",
        "/",
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
    async with aiohttp.ClientSession() as session:
        client = ForecastSolar(
            latitude=51.5,
            longitude=4.47,
            declination=10,
            azimuth=20,
            kwp=2.1,
            damping=0,
            session=session,
        )
        response = await client._request("")
        assert response is not None
        await client.close()


@pytest.mark.asyncio
async def test_internal_session(aresponses: ResponsesMockServer) -> None:
    """Test JSON response is handled correctly."""
    aresponses.add(
        "api.forecast.solar",
        "/",
        "GET",
        aresponses.Response(
            status=200,
            headers={
                "Content-Type": "application/json",
                "X-Ratelimit-Limit": "10",
                "X-Ratelimit-Period": "1",
            },
            text='{"message": "success"}',
        ),
    )
    async with ForecastSolar(
        latitude=52.16, longitude=4.47, declination=20, azimuth=10, kwp=2.160, damping=0
    ) as client:
        response = await client._request("")
        assert response["message"] == "success"


@pytest.mark.asyncio
async def test_content_type(aresponses: ResponsesMockServer) -> None:
    """Test request content type error from Forecast.Solar API."""
    aresponses.add(
        "api.forecast.solar",
        "/",
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

    async with aiohttp.ClientSession() as session:
        client = ForecastSolar(
            latitude=52.16,
            longitude=4.47,
            declination=20,
            azimuth=10,
            kwp=2.160,
            damping=0,
            session=session,
        )
        with pytest.raises(ForecastSolarError):
            assert await client._request("")
