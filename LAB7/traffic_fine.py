"""Traffic fine helpers (Lab 7 - Fuzz Testing, hardened version).

Error contract
--------------
Every public function either returns a valid result or raises ``ValueError``
with a clear message.  No other exception type (AttributeError, TypeError,
ZeroDivisionError, ...) may ever escape - Hypothesis fuzz tests enforce this.
"""
import re

MAX_TOTAL_FINE = 10000

_PREFIX_RE = re.compile(r"[A-Za-z]+", re.ASCII)
_YEAR_RE = re.compile(r"[0-9]{4}", re.ASCII)
_SERIAL_RE = re.compile(r"[0-9]{1,10}", re.ASCII)
_AMOUNT_RE = re.compile(r"[0-9]{1,18}", re.ASCII)
_SPEED_RE = re.compile(r"[0-9]{1,6}", re.ASCII)


def _require_str(value, name):
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a string, got {type(value).__name__}")
    return value.strip()


def parse_ticket_id(ticket_id):
    """Parse 'PREFIX-YYYY-SERIAL' (e.g. 'TF-2024-0456') -> (PREFIX, year, serial)."""
    text = _require_str(ticket_id, "ticket_id")
    parts = text.split("-")
    if len(parts) != 3:
        raise ValueError("ticket_id must look like PREFIX-YYYY-SERIAL")
    prefix, year, serial = (p.strip() for p in parts)
    if not _PREFIX_RE.fullmatch(prefix):
        raise ValueError("ticket prefix must contain letters A-Z only")
    if not _YEAR_RE.fullmatch(year):
        raise ValueError("ticket year must be exactly 4 digits")
    if not _SERIAL_RE.fullmatch(serial):
        raise ValueError("ticket serial must be 1-10 digits")
    return prefix.upper(), int(year), int(serial)


def total_fines(amounts_csv):
    """Sum comma separated non-negative integer fines, capped at MAX_TOTAL_FINE."""
    text = _require_str(amounts_csv, "amounts_csv")
    if text == "":
        raise ValueError("amounts_csv must not be empty")
    total = 0
    for raw in text.split(","):
        item = raw.strip()
        if not _AMOUNT_RE.fullmatch(item):
            raise ValueError(f"invalid fine amount: {item!r}")
        total += int(item)
    return min(total, MAX_TOTAL_FINE)


def speed_excess(reading):
    """Parse 'speed/limit' (e.g. '72/60') -> whole percent over the limit.

    A negative result means the driver was under the limit.
    """
    text = _require_str(reading, "reading")
    parts = text.split("/")
    if len(parts) != 2:
        raise ValueError("reading must look like SPEED/LIMIT")
    speed_s, limit_s = (p.strip() for p in parts)
    if not _SPEED_RE.fullmatch(speed_s) or not _SPEED_RE.fullmatch(limit_s):
        raise ValueError("speed and limit must be non-negative integers")
    speed, limit = int(speed_s), int(limit_s)
    if limit == 0:
        raise ValueError("speed limit must be greater than zero")
    return (speed - limit) * 100 // limit


def _ask(prompt, func):
    try:
        return func(input(prompt))
    except ValueError as exc:
        return f"Invalid input - {exc}"


def main():
    print("==== Running parse_ticket_id ====")
    print("Ticket Prefix, Year and Serial:",
          _ask("Enter a ticket ID (e.g. TF-2024-0456): ", parse_ticket_id))

    print("\n==== Running total_fines ====")
    print("Total Fines:",
          _ask("Enter fine amounts as CSV (e.g. 500,1200,300): ", total_fines))

    print("\n==== Running speed_excess ====")
    print("Percent Over Limit:",
          _ask("Enter speed/limit (e.g. 72/60): ", speed_excess))


if __name__ == "__main__":
    main()
