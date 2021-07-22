"""Test the models."""
from datetime import datetime
from forecast_solar import models
from . import PAYLOAD, patch_now, patch_previous_day, patch_near_end_today


def test_estimate_previous_day(patch_previous_day):
    """Test estimate."""
    estimate = models.Estimate.from_dict(PAYLOAD)

    assert estimate.timezone == "Europe/Amsterdam"

    assert estimate.now().date().isoformat() == "2021-07-20"

    assert estimate.energy_production_today == 12984
    assert estimate.energy_production_tomorrow == 14679

    assert estimate.power_production_now == 0
    assert estimate.energy_current_hour == 0

    assert estimate.power_highest_peak_time_today == datetime.fromisoformat(
        "2021-07-20T15:00:00+02:00"
    )
    assert estimate.power_highest_peak_time_tomorrow == datetime.fromisoformat(
        "2021-07-21T14:00:00+02:00"
    )

    assert estimate.sum_energy_production(1) == 0
    assert estimate.sum_energy_production(6) == 0
    assert estimate.sum_energy_production(12) == 3631
    assert estimate.sum_energy_production(24) == 14679


def test_estimate_now(patch_now):
    """Test estimate."""
    estimate = models.Estimate.from_dict(PAYLOAD)

    assert estimate.timezone == "Europe/Amsterdam"
    assert estimate.now().date().isoformat() == "2021-07-21"

    assert estimate.energy_production_today == 14679
    assert estimate.energy_production_tomorrow == 0

    assert estimate.power_production_now == 724
    assert estimate.energy_current_hour == 724

    assert estimate.power_highest_peak_time_today == datetime.fromisoformat(
        "2021-07-21T14:00:00+02:00"
    )
    assert estimate.power_highest_peak_time_tomorrow is None

    assert estimate.sum_energy_production(1) == 1060
    assert estimate.sum_energy_production(6) == 9044
    assert estimate.sum_energy_production(12) == 13454
    assert estimate.sum_energy_production(24) == 13454


def test_estimate_near_end(patch_near_end_today):
    """Test estimate."""
    estimate = models.Estimate.from_dict(PAYLOAD)

    assert estimate.timezone == "Europe/Amsterdam"
    assert estimate.now().date().isoformat() == "2021-07-21"

    assert estimate.energy_production_today == 14679
    assert estimate.energy_production_tomorrow == 0

    assert estimate.power_production_now == 888
    assert estimate.energy_current_hour == 888

    assert estimate.power_highest_peak_time_today == datetime.fromisoformat(
        "2021-07-21T14:00:00+02:00"
    )
    assert estimate.power_highest_peak_time_tomorrow is None

    assert estimate.sum_energy_production(1) == 548
    assert estimate.sum_energy_production(6) == 846
    assert estimate.sum_energy_production(12) == 846
    assert estimate.sum_energy_production(24) == 846
