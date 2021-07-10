"""Exceptions for Forecast.Solar."""


class ForecastSolarError(Exception):
    """Generic Forecast.Solar exception."""


class ForecastSolarConnectionError(ForecastSolarError):
    """Forecast.Solar API connection exception."""


class ForecastSolarNoCoverage(ForecastSolarError):
    """Forecast.Solar out of data coverage exception."""


class ForecstSolarRateLimit(ForecastSolarError):
    """Forecast.Solar maximum number of requests reached exception."""
