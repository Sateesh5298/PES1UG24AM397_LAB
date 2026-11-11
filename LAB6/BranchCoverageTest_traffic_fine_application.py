import pytest
from traffic_fine import speeding_fine, license_action, total_penalty

# --- speeding_fine branch tests ---
def test_branch_speed_less_than_limit():
    assert speeding_fine(40, 50, "city") == 0

def test_branch_speed_equal_to_limit():
    assert speeding_fine(50, 50, "city") == 0

def test_branch_zone_school_excess_above_40():
    assert speeding_fine(95, 50, "school") == 6000

def test_branch_zone_highway_excess_between_20_and_40():
    assert speeding_fine(90, 60, "highway") == 2000

def test_branch_zone_default_excess_under_20():
    assert speeding_fine(60, 50, "other") == 500


# --- license_action branch tests ---
def test_branch_points_ge_12_commercial():
    assert license_action(15, True, False) == "revoke"

def test_branch_points_ge_12_non_commercial():
    assert license_action(12, False, False) == "suspend"

def test_branch_points_ge_8_repeat():
    assert license_action(10, False, True) == "suspend"

def test_branch_points_ge_8_non_repeat():
    assert license_action(8, False, False) == "warning"

def test_branch_points_ge_4():
    assert license_action(4, False, False) == "notice"

def test_branch_points_lt_4():
    assert license_action(0, False, False) == "none"


# --- total_penalty branch tests ---
def test_branch_total_penalty_empty_list():
    assert total_penalty([]) == 0

def test_branch_total_penalty_negative_value():
    with pytest.raises(ValueError, match="negative fine"):
        total_penalty([-10])

def test_branch_total_penalty_under_cap():
    assert total_penalty([1000, 2000]) == 3000

def test_branch_total_penalty_exactly_at_cap():
    assert total_penalty([10000]) == 10000

def test_branch_total_penalty_exceeding_cap():
    assert total_penalty([7000, 4000]) == 10000
