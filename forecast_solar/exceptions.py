"""Exceptions for Forecast.Solar."""


class ForecastSolarError(Exception):
    """Generic Forecast.Solar exception."""


class ForecastSolarConnectionError(ForecastSolarError):
    """Forecast.Solar API connection exception."""


class ForecastSolarRequestError(ForecastSolarError):
    """Forecast.Solar wrong request input variables."""


class ForecstSolarRateLimit(ForecastSolarError):
    """Forecast.Solar maximum number of requests reached exception."""
