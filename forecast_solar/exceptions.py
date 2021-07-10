"""Exceptions for Forecast.Solar."""


class ForecastSolarError(Exception):
    """Generic Forecast.Solar exception."""


class ForecastSolarConnectionError(ForecastSolarError):
    """Forecast.Solar API connection exception."""


class ForecastSolarNoCoverage(ForecastSolarConnectionError):
    """Forecast.Solar out of data coverage exception."""