# Lab 5 – Issues Found in parcel_tracker.py

Tools: Pylint, Bandit, Flake8 (reports in `reports/before/`).
Before: Pylint 4.91/10, Bandit 4 issues (1 High, 1 Medium, 2 Low), Flake8 4 issues.

| # | Issue | Type | Line(s) | Description | Fix Approach |
|---|-------|------|---------|-------------|--------------|
| 1 | subprocess with shell=True (B602) | Security – High | 55 | `"ping -c 1 " + hubAddress` is run through a shell, so input like `8.8.8.8; rm -rf /` runs extra commands (command injection, CWE-78). | Validate with `ipaddress.ip_address()`, pass an argument list `["ping","-c","1",addr]` with `shell=False` and a `timeout`. |
| 2 | Insecure temp file (B306 mktemp) | Security – Medium | 50 | `tempfile.mktemp()` only returns a name; another process can create that file first (race condition, CWE-377). | Use `tempfile.NamedTemporaryFile(delete=False)` which creates the file atomically. |
| 3 | Mutable default argument (W0102) | Bug | 11 | `history=[]` is created once and shared by every call, so ids leak between calls. | Default to `None` and create a new list inside the function. |
| 4 | Overly broad exception (W0718) | Bug / Quality | 37 | `except Exception` hides unrelated errors (typos, TypeError, etc.). | Catch only `KeyError`, the real "unknown id" case. |
| 5 | Weak random for OTP (B311) | Security – Low | 72 | `random.randint` is predictable, not suitable for a delivery OTP (CWE-330). | Use `secrets.randbelow()` -> `1000 + secrets.randbelow(9000)`. |
| 6 | subprocess import (B404) | Security – Low | 2 | Informational warning for importing subprocess. | Import kept (needed); usage made safe (#1) and annotated `# nosec B404`. |
| 7 | Naming not snake_case (C0103) | Style | 11-67 | `bookParcel`, `weightKg`, `trackingId`, `pingHub` ... break PEP 8. | Rename to `book_parcel`, `weight_kg`, `tracking_id`, `ping_hub` ... |
| 8 | Missing docstrings (C0114/C0116) | Style | 1, 11-58 | Module and all functions undocumented. | Add a module docstring and one-line docstrings. |
| 9 | Chained comparison (R1714) | Refactor | 45 | `status == "A" or status == "B"` | `status in ("Picked Up", "In Transit")` |
| 10 | Missing whitespace (E225) | Style (Flake8) | 28 | `cost=50` | `cost = 50` |
| 11 | Inline comment spacing (E261) | Style (Flake8) | 71 | one space before `#` | two spaces before `#` |
| 12 | Missing space after comma (E231) | Style (Flake8) | 74 | `"...today:",len(...)` | add a space after the comma |
| 13 | Blank lines after function (E305) | Style (Flake8) | 75 | `main()` right after the function; also runs on import. | Two blank lines + `if __name__ == "__main__":` guard. |

After: Pylint 10.00/10, Bandit 0 issues, Flake8 0 issues. Program output unchanged.
