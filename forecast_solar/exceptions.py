"""Exceptions for Forecast.Solar."""
from datetime import datetime
from typing import Any


class ForecastSolarError(Exception):
    """Generic Forecast.Solar exception."""


class ForecastSolarConnectionError(ForecastSolarError):
    """Forecast.Solar API connection exception."""


class ForecastSolarAuthenticationError(ForecastSolarError):
    """Forecast.Solar API authentication exception."""

    def __init__(self, data: dict[str, Any]) -> None:
        """Init a solar auth error.

        https://doc.forecast.solar/doku.php?id=api#invalid_request

        Args:
            data: The response from the Forecast.Solar API.
        """
        super().__init__(f'{data["text"]} (error {data["code"]})')
        self.code = data["code"]


class ForecastSolarRequestError(ForecastSolarError):
    """Forecast.Solar wrong request input variables."""

    def __init__(self, data: dict[str, Any]) -> None:
        """Init a solar request error.

        https://doc.forecast.solar/doku.php?id=api#invalid_request

        Args:
            data: The response from the Forecast.Solar API.
        """
        super().__init__(f'{data["text"]} (error {data["code"]})')
        self.code = data["code"]


class ForecastSolarRatelimit(ForecastSolarRequestError):
    """Forecast.Solar maximum number of requests reached exception."""

    def __init__(self, data: dict[str, Any]) -> None:
        """Init a rate limit error.

        Args:
            data: The response from the Forecast.Solar API.
        """
        super().__init__(data)

        self.reset_at = datetime.fromisoformat(data["ratelimit"]["retry-at"])
