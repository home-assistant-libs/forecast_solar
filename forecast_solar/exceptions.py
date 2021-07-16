"""Exceptions for Forecast.Solar."""


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


class ForecastSolarRatelimit(ForecastSolarError):
    """Forecast.Solar maximum number of requests reached exception."""
