"""Test the models."""
# pylint: disable=protected-access
import aiohttp
import pytest
from aresponses import ResponsesMockServer

from forecast_solar import Estimate, ForecastSolar

from . import load_fixtures


@pytest.mark.asyncio
async def test_forecast(aresponses: ResponsesMockServer) -> None:
    """Test the forecast model."""
    aresponses.add(
        "api.forecast.solar",
        "/estimate/51.5/4.47/10/20/2.1",
        "GET",
        aresponses.Response(
            text=load_fixtures("forecast.json"),
            status=200,
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "X-Ratelimit-Limit": "10",
                "X-Ratelimit-Period": "1",
            },
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
        estimate: Estimate = await client.estimate()
        assert estimate.timezone == "Europe/Amsterdam"
        assert estimate.api_rate_limit == 12
