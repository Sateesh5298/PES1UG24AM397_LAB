"""Parcel tracker for a courier service.

Books parcels, moves them through the delivery stages, tracks a parcel by id,
checks whether it is with the courier and works out the shipping cost.
"""
import ipaddress
import secrets
import subprocess  # nosec B404
import tempfile
from datetime import date

STATUS_FLOW = ["Booked", "Picked Up", "In Transit",
               "Out for Delivery", "Delivered"]
parcels = {}


def book_parcel(sender, receiver, weight_kg, history=None):
    """Book a parcel and return its new tracking id."""
    if history is None:
        history = []
    tracking_id = "TRK" + str(10001 + len(parcels))
    parcels[tracking_id] = {"sender": sender, "receiver": receiver,
                            "weight": weight_kg, "status": 0,
                            "booked": str(date.today())}
    history.append(tracking_id)
    return tracking_id


def advance_status(tracking_id):
    """Move a parcel to its next delivery stage and return the new stage."""
    parcel = parcels[tracking_id]
    if parcel["status"] < len(STATUS_FLOW) - 1:
        parcel["status"] += 1
    return STATUS_FLOW[parcel["status"]]


def shipping_cost(weight_kg):
    """Return the shipping cost: 50 base plus 30 per kg above the first."""
    cost = 50
    if weight_kg > 1:
        cost += (weight_kg - 1) * 30
    return round(cost, 2)


def track_parcel(tracking_id):
    """Return a readable route and status line for a parcel."""
    try:
        parcel = parcels[tracking_id]
    except KeyError:
        return "Unknown tracking id " + tracking_id
    route = parcel["sender"] + " -> " + parcel["receiver"]
    return route + ": " + STATUS_FLOW[parcel["status"]]


def is_with_courier(tracking_id):
    """Return True while the parcel is picked up or in transit."""
    status = STATUS_FLOW[parcels[tracking_id]["status"]]
    return status in ("Picked Up", "In Transit")


def label_path():
    """Create a unique temporary label file safely and return its path."""
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
        return tmp.name


def ping_hub(hub_address):
    """Ping a hub by IP address (validated, no shell) and return output."""
    ipaddress.ip_address(hub_address)  # ValueError if not a valid IP
    return subprocess.check_output(  # nosec B603 B607
        ["ping", "-c", "1", hub_address], timeout=10)


def main():
    """Run a short demonstration of the parcel tracker."""
    first = book_parcel("Bengaluru Books", "Ravi Kumar", 2.5)
    second = book_parcel("Gadget Hub", "Sneha Rao", 0.8)
    third = book_parcel("Spice Store", "Imran Khan", 4)
    advance_status(first)
    advance_status(first)
    advance_status(second)
    for _ in range(6):
        advance_status(third)
    for tracking_id in (first, second, third):
        print(track_parcel(tracking_id))
        print("  with courier:", is_with_courier(tracking_id))
        print("  cost:", shipping_cost(parcels[tracking_id]["weight"]))
    print(track_parcel("TRK00000"))  # unknown id
    delivery_otp = 1000 + secrets.randbelow(9000)
    print("Delivery OTP for", third, "is", delivery_otp)
    print("Parcels booked today:", len(parcels))


if __name__ == "__main__":
    main()
