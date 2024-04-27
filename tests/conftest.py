"""Fixtures for the Forecast.Solar tests."""

from collections.abc import AsyncGenerator

import pytest
from aiohttp import ClientSession

from forecast_solar import ForecastSolar


@pytest.fixture(name="forecast_client")
async def client() -> AsyncGenerator[ForecastSolar, None]:
    """Return a Forecast.Solar client."""
    async with (
        ClientSession() as session,
        ForecastSolar(
            latitude=52.16,
            longitude=4.47,
            declination=20,
            azimuth=10,
            kwp=2.160,
            damping=0,
            horizon="0,0,0,10,10,20,20,30,30",
            session=session,
        ) as forecast_client,
    ):
        yield forecast_client


@pytest.fixture(name="forecast_key_client")
async def client_api_key() -> AsyncGenerator[ForecastSolar, None]:
    """Return a Forecast.Solar client."""
    async with (
        ClientSession() as session,
        ForecastSolar(
            api_key="myapikey",
            latitude=52.16,
            longitude=4.47,
            declination=20,
            azimuth=10,
            kwp=2.160,
            damping_morning=0,
            damping_evening=0,
            horizon="0,0,0,10,10,20,20,30,30",
            inverter=1.300,
            session=session,
        ) as forecast_key_client,
    ):
        yield forecast_key_client
