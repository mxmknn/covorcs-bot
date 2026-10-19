"""Synthetic geography with independent metre oracles; no real places."""

from dataclasses import FrozenInstanceError
from decimal import Decimal
from itertools import permutations

import pytest

from coworking_nearby.geo import find_nearest, validate_origin
from coworking_nearby.models import Coworking, Origin, SearchResult


def place(id, latitude=0, longitude=0, **kwargs):
    return Coworking(id, "SYNTHETIC", "Test address", latitude, longitude, **kwargs)


class IntSubclass(int):
    pass


class FloatSubclass(float):
    pass


@pytest.mark.parametrize("bad", [True, False, None, "0", [], {}, Decimal("0"),
                                 IntSubclass(0), FloatSubclass(0), float("nan"),
                                 float("inf"), -float("inf"), 10**1000, -10**1000])
@pytest.mark.parametrize("axis", [0, 1])
def test_invalid_origin(bad, axis):
    values = [0, 0]
    values[axis] = bad
    with pytest.raises(ValueError):
        validate_origin(*values)
    with pytest.raises(ValueError):
        find_nearest(Origin(*values), (), 3)


@pytest.mark.parametrize("lat,lon", [(90.00001, 0), (-90.00001, 0),
                                   (0, 180.00001), (0, -180.00001)])
def test_origin_outside_bounds(lat, lon):
    with pytest.raises(ValueError):
        validate_origin(lat, lon)


@pytest.mark.parametrize("lat,lon", [(0, 0), (-0., 0.), (-90, -180), (90, 180),
                                   (-33.86, 151.20)])
def test_valid_origin_immutable(lat, lon):
    origin = validate_origin(lat, lon)
    assert origin == Origin(lat, lon)
    with pytest.raises(FrozenInstanceError):
        origin.latitude = 1


@pytest.mark.parametrize("limit", [True, False, None, "3", 3., IntSubclass(3), 0, -1, 6, 10**1000])
def test_invalid_limit(limit):
    with pytest.raises(ValueError):
        find_nearest(Origin(0, 0), (), limit)


@pytest.mark.parametrize("origin,ids,distances", [
    (Origin(0, 0), ("W", "M", "E"), (0, 111194.926644559, 333584.779933676)),
    (Origin(0, 3), ("E", "M", "W"), (0, 222389.853289118, 333584.779933676)),
])
def test_known_order_two_origins(origin, ids, distances):
    records = (place("W"), place("M", longitude=1), place("E", longitude=3),
               place("R", longitude=10, rating_text="BEST"))
    for snapshot in permutations(records):
        before = tuple(r.to_mapping() for r in snapshot)
        results = find_nearest(origin, snapshot, 3)
        assert type(results) is tuple
        assert all(type(r) is SearchResult for r in results)
        assert tuple(r.record.id for r in results) == ids
        assert tuple(r.distance_m for r in results) == pytest.approx(distances, abs=.001)
        assert all(any(r.record is entry for entry in snapshot) for r in results)
        assert tuple(r.to_mapping() for r in snapshot) == before


@pytest.mark.parametrize("limit", range(1, 6))
@pytest.mark.parametrize("count", range(7))
def test_cardinality_active_no_radius(limit, count):
    snapshot = (place("inactive", active=False),) + tuple(
        place(str(i), latitude=-80, longitude=-170, rating_text="remote") for i in range(count))
    results = find_nearest(Origin(80, 170), snapshot, limit)
    assert len(results) == min(limit, count)
    assert tuple(r.record.id for r in results) == tuple(str(i) for i in range(min(limit, count)))
    assert all(r.distance_m > 1000000 for r in results)
    assert snapshot[0].active is False


def test_exact_unicode_ties_and_raw_near_ties():
    ids = ("A", "a", "é", "\ue000", "\U00010000", "😀")
    snapshot = tuple(place(id) for id in reversed(ids))
    assert tuple(r.record.id for r in find_nearest(Origin(0, 0), snapshot, 5)) == ids[:5]
    near = (place("a", longitude=.008991), place("z", longitude=.008990))
    results = find_nearest(Origin(0, 0), near, 2)
    assert tuple(r.record.id for r in results) == ("z", "a")
    assert tuple(r.distance_m for r in results) == pytest.approx(
        (999.6423905345829, 999.7535854612277), abs=.001)


@pytest.mark.parametrize("origin,destination,expected", [
    (Origin(0, 0), place("zero"), 0),
    (Origin(0, 0), place("quarter", longitude=90), 10007543.398010286),
    (Origin(0, 0), place("antipode", longitude=180), 20015086.79602057),
    (Origin(-90, -180), place("pole", latitude=-90, longitude=180), 0),
    (Origin(90, 0), place("south", latitude=-90), 20015086.79602057),
    (Origin(0, -90), place("negative", longitude=-180), 10007543.398010286),
])
def test_zero_negative_remote_poles_antipodes(origin, destination, expected):
    assert find_nearest(origin, (destination,), 1)[0].distance_m == pytest.approx(expected, abs=.001)
