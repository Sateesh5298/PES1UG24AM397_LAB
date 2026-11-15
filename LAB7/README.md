# L6_L7_27 — Traffic Fine Calculator

**Lab 7: Fuzz Testing** — SRN: PES1UG24AM397

## About

A small Python module that parses traffic ticket details, totals fines and measures how far over the limit a driver was.
Lab 7 fuzz tests it with [Hypothesis](https://hypothesis.readthedocs.io/), fixes the crashes found, and adds regression tests.

## Files

| File | Description |
|------|-------------|
| `traffic_fine.py` | Fixed module: strict validation, only `ValueError` on bad input |
| `traffic_fine_original.py` | Original starter code (kept to reproduce the crashes) |
| `test_traffic_fine.py` | Completed fuzz, property and regression tests (47 tests) |
| `evidence/` | Before/after pytest output, coverage and fuzzer crash demo |
| `PES1UG24AM397_SE_LAB7.pdf` | Lab report |

## Run

```bash
pip install hypothesis pytest pytest-cov
pytest -v
pytest --cov=traffic_fine --cov-branch --cov-report=term-missing
python evidence/fuzz_crash_demo.py     # shows crashes in original vs fixed code
```

## Bugs found by fuzzing (original code)

`None` input (AttributeError), empty input, `ZeroDivisionError` for limit 0, wrong field counts,
negative fines/speeds, and lenient `int()` parsing (`+1`, `1_0`, Unicode digits).
