"""Lab 7 - Fuzz testing of traffic_fine.py with Hypothesis.

Contract under test: a function may return a result or raise ValueError.
Any other exception escaping is a bug and fails the test.
"""
import pytest
from hypothesis import given, example, settings, strategies as st

from traffic_fine import (parse_ticket_id, total_fines, speed_excess,
                          MAX_TOTAL_FINE)

# ---------------------------------------------------------------------------
# 1. Starter "no crash" fuzz tests (arbitrary text or None)
# ---------------------------------------------------------------------------

@given(st.text() | st.none())
@example(None)
@example("")
@example("TF-2024")
@example("TF-2024-0456-9")
@example("TF--")
def test_parse_ticket_id_no_crash(s):
    try:
        parse_ticket_id(s)
    except ValueError:
        pass


@given(st.text() | st.none())
@example(None)
@example("")
@example("1,,2")
@example("-5,3")
@example("1.5")
def test_total_fines_no_crash(s):
    try:
        total_fines(s)
    except ValueError:
        pass


@given(st.text() | st.none())
@example(None)
@example("")
@example("/")
@example("72/0")
@example("1/2/3")
def test_speed_excess_no_crash(s):
    try:
        speed_excess(s)
    except ValueError:
        pass


# Wider fuzzing: arbitrary non-string objects must also be rejected cleanly.
@given(st.one_of(st.integers(), st.floats(), st.binary(), st.lists(st.integers()),
                 st.booleans()))
def test_non_string_inputs_rejected_with_valueerror(x):
    for func in (parse_ticket_id, total_fines, speed_excess):
        with pytest.raises(ValueError):
            func(x)


# Structured fuzzing: inputs that look almost valid reach deeper code paths.
_almost = st.text(alphabet="TFtf0123456789-,/ .+_\n\t\u0663", max_size=20)

@settings(max_examples=500)
@given(_almost)
def test_all_functions_no_crash_on_near_valid_text(s):
    for func in (parse_ticket_id, total_fines, speed_excess):
        try:
            func(s)
        except ValueError:
            pass


# ---------------------------------------------------------------------------
# 2. Property tests on valid input
# ---------------------------------------------------------------------------

@given(st.text(alphabet="abcXYZ", min_size=1, max_size=5),
       st.integers(0, 9999), st.integers(0, 10**10 - 1))
def test_parse_ticket_id_roundtrip(prefix, year, serial):
    tid = f"{prefix}-{year:04d}-{serial}"
    assert parse_ticket_id(tid) == (prefix.upper(), year, serial)


@given(st.lists(st.integers(0, 10**9), min_size=1, max_size=20))
def test_total_fines_is_capped_sum(amounts):
    result = total_fines(",".join(map(str, amounts)))
    assert result == min(sum(amounts), MAX_TOTAL_FINE)
    assert 0 <= result <= MAX_TOTAL_FINE


@given(st.integers(0, 999999), st.integers(1, 999999))
def test_speed_excess_matches_formula(speed, limit):
    result = speed_excess(f"{speed}/{limit}")
    assert result == (speed - limit) * 100 // limit
    assert result >= -100
    assert (result > 0) <= (speed > limit)   # positive excess implies speeding
    assert (speed <= limit) <= (result <= 0)  # at/under limit gives <= 0


# ---------------------------------------------------------------------------
# 3. Regression tests for every crash the fuzzer found in the original code
# ---------------------------------------------------------------------------

def test_known_good_values():
    assert parse_ticket_id("TF-2024-0456") == ("TF", 2024, 456)
    assert parse_ticket_id(" tf-2024-0456 ") == ("TF", 2024, 456)
    assert total_fines("500,1200,300") == 2000
    assert total_fines("9000, 2000") == 10000
    assert speed_excess("72/60") == 20
    assert speed_excess("50/60") == -17


@pytest.mark.parametrize("bad", [None, "", "TF-2024", "TF-2024-1-2", "TF--",
                                 "TF-abc-1", "TF-2024-x", "T1-2024-1",
                                 "TF-2024-1\n9", "TF-\u0663\u0664\u0665\u0666-1",
                                 "TF-2024-+1", "TF-2024--1", "TF-20_4-1"])
def test_parse_ticket_id_rejects(bad):
    with pytest.raises(ValueError):
        parse_ticket_id(bad)


@pytest.mark.parametrize("bad", [None, "", " ", "1,,2", "a,b", "1.5", "-5,3",
                                 "1,", ",1", "1_0", "+5", "\u0663", "1e3"])
def test_total_fines_rejects(bad):
    with pytest.raises(ValueError):
        total_fines(bad)


@pytest.mark.parametrize("bad", [None, "", "72", "/", "72/0", "0/0", "a/60",
                                 "1/2/3", "-5/60", "60/-60", "6.5/60", "7_2/60"])
def test_speed_excess_rejects(bad):
    with pytest.raises(ValueError):
        speed_excess(bad)
