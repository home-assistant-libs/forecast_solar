"""Tests."""
from datetime import datetime
from unittest.mock import patch, Mock

import pytest


@pytest.fixture
def patch_previous_day():
    """If no solar is forecasted today, it will start returning tomorrow values."""
    with patch("forecast_solar.models.Estimate.now", Mock(return_value=PREVIOUS_DAY)):
        yield


@pytest.fixture
def patch_now():
    """Patch datetime to return payload datetime."""
    with patch("forecast_solar.models.Estimate.now", Mock(return_value=NOW)):
        yield


@pytest.fixture
def patch_near_end_today():
    """Patch datetime to return payload datetime."""
    with patch("forecast_solar.models.Estimate.now", Mock(return_value=NEAR_END_TODAY)):
        yield


PREVIOUS_DAY = datetime.fromisoformat("2021-07-20T23:48:36.170479+02:00")
NOW = datetime.fromisoformat("2021-07-21T07:48:36.170479+00:00")
NEAR_END_TODAY = datetime.fromisoformat("2021-07-21T16:48:36.170479+00:00")

PAYLOAD = {
    "message": {
        "code": 0,
        "info": {
            "distance": 0.969,
            "place": "2333 DC Leiden, Zuid-Holland, NL",
            "timezone": "Europe/Amsterdam",
        },
        "ratelimit": {"limit": 12, "period": 3600, "remaining": 10},
        "text": "",
        "type": "success",
    },
    "result": {
        "watt_hours": {
            "2021-07-20T05:39:00+02:00": 0,
            "2021-07-20T06:12:00+02:00": 13,
            "2021-07-20T06:45:00+02:00": 82,
            "2021-07-20T07:00:00+02:00": 123,
            "2021-07-20T08:00:00+02:00": 518,
            "2021-07-20T09:00:00+02:00": 1242,
            "2021-07-20T10:00:00+02:00": 2268,
            "2021-07-20T11:00:00+02:00": 3521,
            "2021-07-20T12:00:00+02:00": 4743,
            "2021-07-20T13:00:00+02:00": 6096,
            "2021-07-20T14:00:00+02:00": 7487,
            "2021-07-20T15:00:00+02:00": 8899,
            "2021-07-20T16:00:00+02:00": 10184,
            "2021-07-20T17:00:00+02:00": 11264,
            "2021-07-20T18:00:00+02:00": 12144,
            "2021-07-20T19:00:00+02:00": 12686,
            "2021-07-20T20:00:00+02:00": 12936,
            "2021-07-20T20:59:00+02:00": 12984,
            "2021-07-20T21:57:00+02:00": 12984,
            "2021-07-21T05:40:00+02:00": 0,
            "2021-07-21T06:13:00+02:00": 13,
            "2021-07-21T06:45:00+02:00": 78,
            "2021-07-21T07:00:00+02:00": 119,
            "2021-07-21T08:00:00+02:00": 501,
            "2021-07-21T09:00:00+02:00": 1225,
            "2021-07-21T10:00:00+02:00": 2285,
            "2021-07-21T11:00:00+02:00": 3631,
            "2021-07-21T12:00:00+02:00": 5195,
            "2021-07-21T13:00:00+02:00": 6895,
            "2021-07-21T14:00:00+02:00": 8621,
            "2021-07-21T15:00:00+02:00": 10269,
            "2021-07-21T16:00:00+02:00": 11737,
            "2021-07-21T17:00:00+02:00": 12945,
            "2021-07-21T18:00:00+02:00": 13833,
            "2021-07-21T19:00:00+02:00": 14381,
            "2021-07-21T20:00:00+02:00": 14632,
            "2021-07-21T20:58:00+02:00": 14679,
            "2021-07-21T21:56:00+02:00": 14679,
        },
        "watt_hours_day": {
            "2021-07-20T02:00:00+02:00": 12984,
            "2021-07-21T02:00:00+02:00": 14679,
        },
        "watts": {
            "2021-07-20T05:39:00+02:00": 0,
            "2021-07-20T06:12:00+02:00": 24,
            "2021-07-20T06:45:00+02:00": 124,
            "2021-07-20T07:00:00+02:00": 171,
            "2021-07-20T08:00:00+02:00": 395,
            "2021-07-20T09:00:00+02:00": 722,
            "2021-07-20T10:00:00+02:00": 1026,
            "2021-07-20T11:00:00+02:00": 1254,
            "2021-07-20T12:00:00+02:00": 1222,
            "2021-07-20T13:00:00+02:00": 1351,
            "2021-07-20T14:00:00+02:00": 1391,
            "2021-07-20T15:00:00+02:00": 1413,
            "2021-07-20T16:00:00+02:00": 1286,
            "2021-07-20T17:00:00+02:00": 1080,
            "2021-07-20T18:00:00+02:00": 879,
            "2021-07-20T19:00:00+02:00": 543,
            "2021-07-20T20:00:00+02:00": 249,
            "2021-07-20T20:59:00+02:00": 50,
            "2021-07-20T21:57:00+02:00": 0,
            "2021-07-21T05:40:00+02:00": 0,
            "2021-07-21T06:13:00+02:00": 24,
            "2021-07-21T06:45:00+02:00": 119,
            "2021-07-21T07:00:00+02:00": 165,
            "2021-07-21T08:00:00+02:00": 384,
            "2021-07-21T09:00:00+02:00": 724,
            "2021-07-21T10:00:00+02:00": 1060,
            "2021-07-21T11:00:00+02:00": 1345,
            "2021-07-21T12:00:00+02:00": 1564,
            "2021-07-21T13:00:00+02:00": 1699,
            "2021-07-21T14:00:00+02:00": 1726,
            "2021-07-21T15:00:00+02:00": 1648,
            "2021-07-21T16:00:00+02:00": 1468,
            "2021-07-21T17:00:00+02:00": 1208,
            "2021-07-21T18:00:00+02:00": 888,
            "2021-07-21T19:00:00+02:00": 548,
            "2021-07-21T20:00:00+02:00": 251,
            "2021-07-21T20:58:00+02:00": 50,
            "2021-07-21T21:56:00+02:00": 0,
        },
    },
}
