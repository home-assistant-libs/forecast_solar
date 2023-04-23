"""Test the models."""
from datetime import datetime
from forecast_solar import models
from . import PAYLOAD, patch_now, patch_previous_day, patch_near_end_today


def test_estimate_previous_day(patch_previous_day):
    """Test estimate."""
    estimate = models.Estimate.from_dict(PAYLOAD)

    assert estimate.timezone == "Europe/Amsterdam"

    assert estimate.now().date().isoformat() == "2022-10-15"

    assert estimate.energy_production_today == 4528
    assert estimate.energy_production_tomorrow == 5435

    assert estimate.power_production_now == 0
    # production this hour at 23:48 is zero
    assert estimate.energy_current_hour == 0

    assert estimate.power_highest_peak_time_today == datetime.fromisoformat(
        "2022-10-15T15:00:00+02:00"
    )
    assert estimate.power_highest_peak_time_tomorrow == datetime.fromisoformat(
        "2022-10-16T14:00:00+02:00"
    )

    assert estimate.sum_energy_production(1) == 0
    assert estimate.sum_energy_production(6) == 0
    assert estimate.sum_energy_production(12) == 760
    assert estimate.sum_energy_production(24) == 5435


def test_estimate_now(patch_now):
    """Test estimate."""
    estimate = models.Estimate.from_dict(PAYLOAD)

    assert estimate.timezone == "Europe/Amsterdam"
    assert estimate.now().date().isoformat() == "2022-10-15"

    assert estimate.energy_production_today == 4528
    assert estimate.energy_production_tomorrow == 5435

    assert estimate.energy_production_today_remaining == 4504

    assert estimate.power_production_now == 53
    assert estimate.energy_current_hour == 24

    assert estimate.power_highest_peak_time_today == datetime.fromisoformat(
        "2022-10-15T15:00:00+02:00"
    )
    assert estimate.power_highest_peak_time_tomorrow == datetime.fromisoformat(
        "2022-10-16T14:00:00+02:00"
    )

    assert estimate.sum_energy_production(1) == 61
    assert estimate.sum_energy_production(6) == 2200
    assert estimate.sum_energy_production(12) == 4504
    assert estimate.sum_energy_production(24) == 4621


def test_estimate_near_end(patch_near_end_today):
    """Test estimate."""
    estimate = models.Estimate.from_dict(PAYLOAD)

    assert estimate.timezone == "Europe/Amsterdam"
    assert estimate.now().date().isoformat() == "2022-10-15"

    assert estimate.energy_production_today == 4528
    assert estimate.energy_production_tomorrow == 5435

    assert estimate.power_production_now == 337
    # production this hour at 16:48 is sum of values between 16:00 and 16:59:59.999
    assert estimate.energy_current_hour == 642

    assert estimate.power_highest_peak_time_today == datetime.fromisoformat(
        "2022-10-15T15:00:00+02:00"
    )
    assert estimate.power_highest_peak_time_tomorrow == datetime.fromisoformat(
        "2022-10-16T14:00:00+02:00"
    )

    assert estimate.sum_energy_production(1) == 0
    assert estimate.sum_energy_production(6) == 0
    assert estimate.sum_energy_production(12) == 0
    assert estimate.sum_energy_production(24) == 5435
