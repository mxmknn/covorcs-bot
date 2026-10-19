"""Pure Yandex web route links from explicit validated coordinates."""

from urllib.parse import urlencode

from .models import Coworking, Origin, RouteMode


def _coordinate(value: int | float) -> str:
    text = format(value, ".6f").rstrip("0").rstrip(".")
    return "0" if text == "-0" else text


def build_yandex_route_url(origin: Origin, destination: Coworking, mode: RouteMode) -> str:
    """Preserve latitude/longitude and origin/destination order; never fetch."""
    start = f"{_coordinate(origin.latitude)},{_coordinate(origin.longitude)}"
    finish = f"{_coordinate(destination.latitude)},{_coordinate(destination.longitude)}"
    return "https://yandex.ru/maps/?" + urlencode({"rtext": start + "~" + finish, "rtt": mode.value})
