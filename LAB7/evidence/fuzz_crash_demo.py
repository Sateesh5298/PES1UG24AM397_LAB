"""Runs Hypothesis against BOTH versions and prints the minimal failing inputs."""
import importlib, sys
from hypothesis import given, settings, strategies as st, HealthCheck

def fuzz(modname):
    m = importlib.import_module(modname)
    print(f"##### {modname}.py #####")
    for name in ("parse_ticket_id", "total_fines", "speed_excess"):
        f = getattr(m, name)
        seen = {}
        @settings(max_examples=2000, database=None, derandomize=True,
                  suppress_health_check=list(HealthCheck))
        @given(st.text() | st.none())
        def run(s):
            try:
                f(s)
            except ValueError:
                if modname == "traffic_fine_original":
                    seen.setdefault("ValueError", s)   # original leaks raw ValueError too
            except Exception as e:
                key = type(e).__name__
                if key not in seen or len(repr(s)) < len(repr(seen[key])):
                    seen[key] = s
        run()
        print(f"{name}: " + (", ".join(f"{k} on {v!r}" for k, v in seen.items()) or "no unexpected exception types"))
    print()

sys.path.insert(0, ".")
fuzz("traffic_fine_original")
fuzz("traffic_fine")
