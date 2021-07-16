"""Exceptions for Forecast.Solar."""
from datetime import datetime


class ForecastSolarError(Exception):
    """Generic Forecast.Solar exception."""


class ForecastSolarConnectionError(ForecastSolarError):
    """Forecast.Solar API connection exception."""


class ForecastSolarRequestError(ForecastSolarError):
    """Forecast.Solar wrong request input variables."""

    def __init__(self, data: dict) -> None:
        """Init a solar request error.

        https://doc.forecast.solar/doku.php?id=api#invalid_request
        """
        super().__init__(f'{data["text"]} (error {data["code"]})')
        self.code = data["code"]


class ForecastSolarRatelimit(ForecastSolarRequestError):
    """Forecast.Solar maximum number of requests reached exception."""

    def __init__(self, data: dict) -> None:
        """Init a rate limit error."""
        super().__init__(data)

        self.reset_at = datetime.fromisoformat(data["ratelimit"]["retry-at"])
