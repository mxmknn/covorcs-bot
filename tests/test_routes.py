"""Decode queries to catch endpoint order, coordinate swaps and mode errors."""

from urllib.parse import parse_qs, urlsplit

import pytest

from coworking_nearby.models import Coworking, Origin, RouteMode
from coworking_nearby.routes import build_yandex_route_url


@pytest.mark.parametrize("mode,rtt", [(RouteMode.WALK, "pd"), (RouteMode.TRANSIT, "mt"),
                                     (RouteMode.CAR, "auto")])
@pytest.mark.parametrize("origin,expected", [
    (Origin(55.7558264, 37.6172996), "55.755826,37.6173~55.76,37.62"),
    (Origin(-33.8688201, 151.2092962), "-33.86882,151.209296~55.76,37.62"),
])
def test_parse_three_modes_two_origins_swap(mode, rtt, origin, expected):
    destination = Coworking("synthetic", "Test", "Test", 55.7600001, 37.6200001,
                           yandex_maps_url="https://yandex.ru/maps/?ll=99,88")
    parsed = urlsplit(build_yandex_route_url(origin, destination, mode))
    assert (parsed.scheme, parsed.netloc, parsed.path, parsed.fragment) == (
        "https", "yandex.ru", "/maps/", "")
    assert parse_qs(parsed.query) == {"rtext": [expected], "rtt": [rtt]}
    # Named latitude 55 and longitude 37 must stay in these positions.
    assert parse_qs(parsed.query)["rtext"][0].split("~")[1] != "37.62,55.76"


def test_precision_and_negative_zero():
    destination = Coworking("synthetic", "Test", "Test", .0000014, -.0000014)
    query = parse_qs(urlsplit(build_yandex_route_url(
        Origin(-.0000004, -0.), destination, RouteMode.WALK)).query)
    assert query == {"rtext": ["0,0~0.000001,-0.000001"], "rtt": ["pd"]}


def test_boundary_coordinates():
    destination = Coworking("synthetic", "Test", "Test", -90, 180)
    query = parse_qs(urlsplit(build_yandex_route_url(
        Origin(90, -180), destination, RouteMode.CAR)).query)
    assert query == {"rtext": ["90,-180~-90,180"], "rtt": ["auto"]}
