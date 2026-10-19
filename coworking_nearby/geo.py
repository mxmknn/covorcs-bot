"""Pure selection over an already validated immutable catalogue snapshot."""

from math import asin, cos, isfinite, radians, sin, sqrt

from .models import Coworking, Origin, SearchResult


_EARTH_RADIUS_M = 6371000


def validate_origin(latitude: object, longitude: object) -> Origin:
    """Return an immutable origin or raise ValueError without coercing input.

    Only actual int/float values are accepted. Check integer bounds before any
    float conversion, so arbitrarily large integers cannot overflow.
    """
    for value, bound in ((latitude, 90), (longitude, 180)):
        if type(value) not in (int, float):
            raise ValueError("invalid origin")
        if type(value) is float and not isfinite(value):
            raise ValueError("invalid origin")
        if not -bound <= value <= bound:
            raise ValueError("invalid origin")
    return Origin(latitude, longitude)


def _distance(origin: Origin, destination: Coworking) -> float:
    latitude = radians(origin.latitude)
    destination_latitude = radians(destination.latitude)
    delta_latitude = radians(destination.latitude - origin.latitude)
    delta_longitude = radians(destination.longitude - origin.longitude)
    a = (sin(delta_latitude / 2) ** 2
         + cos(latitude) * cos(destination_latitude) * sin(delta_longitude / 2) ** 2)
    return 2 * _EARTH_RADIUS_M * asin(sqrt(min(1.0, max(0.0, a))))


def find_nearest(
    origin: Origin, snapshot: tuple[Coworking, ...], limit: int,
) -> tuple[SearchResult, ...]:
    """Rank active records by raw metres then Unicode id; take at most limit.

    Destination records are normalized catalogue values. No city, rating or
    radius criterion applies; the supplied snapshot and origin stay untouched.
    """
    validate_origin(origin.latitude, origin.longitude)
    if type(limit) is not int or not 1 <= limit <= 5:
        raise ValueError("limit must be an integer from 1 to 5")
    results = (SearchResult(record, _distance(origin, record))
               for record in snapshot if record.active)
    return tuple(sorted(results, key=lambda result: (result.distance_m, result.record.id))[:limit])
