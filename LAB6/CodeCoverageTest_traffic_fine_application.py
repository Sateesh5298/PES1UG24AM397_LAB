import pytest
from traffic_fine import speeding_fine, license_action, total_penalty

# --- speeding_fine tests ---
def test_speeding_fine_no_speeding():
    assert speeding_fine(50, 60, "city") == 0

def test_speeding_fine_school_zone_excess_over_40():
    # speed = 100, limit = 50 -> excess = 50 (>40), base = 2000 -> 2000 * 3 = 6000
    assert speeding_fine(100, 50, "school") == 6000

def test_speeding_fine_highway_zone_excess_over_20():
    # speed = 85, limit = 60 -> excess = 25 (>20), base = 1000 -> 1000 * 2 = 2000
    assert speeding_fine(85, 60, "highway") == 2000

def test_speeding_fine_default_zone_normal_excess():
    # speed = 65, limit = 50 -> excess = 15 (<=20), base = 500 -> 500
    assert speeding_fine(65, 50, "residential") == 500


# --- license_action tests ---
def test_license_action_revoke_commercial():
    assert license_action(12, True, False) == "revoke"

def test_license_action_suspend_non_commercial():
    assert license_action(12, False, False) == "suspend"

def test_license_action_suspend_repeat_offender():
    assert license_action(8, False, True) == "suspend"

def test_license_action_warning():
    assert license_action(8, False, False) == "warning"

def test_license_action_notice():
    assert license_action(4, False, False) == "notice"

def test_license_action_none():
    assert license_action(2, False, False) == "none"


# --- total_penalty tests ---
def test_total_penalty_normal_sum():
    assert total_penalty([1000, 2000, 1500]) == 4500

def test_total_penalty_cap_exceeded():
    assert total_penalty([5000, 6000]) == 10000

def test_total_penalty_negative_fine_exception():
    with pytest.raises(ValueError, match="negative fine"):
        total_penalty([500, -200, 1000])
