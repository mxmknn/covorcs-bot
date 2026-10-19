"""Exact Russian UI and parsed visible cards, without Telegram delivery claims."""

from dataclasses import replace
from datetime import date
from html.parser import HTMLParser
import json
import subprocess
import sys
from urllib.parse import parse_qs, urlsplit

import pytest

from coworking_nearby.models import Card, Coworking, Origin, SearchResult
from coworking_nearby.render import (
    EMPTY_TEXT, FALLBACK_TEXT, GROUP_TEXT, HELP_TEXT, INTRO_TEXT,
    INVALID_ORIGIN_TEXT, LOCATION_BUTTON_TEXT, format_distance, render_card, start_text,
)


BASE = Coworking("synthetic", "Название", "Тестовый город, дом 1", 55.76, 37.62)
ORIGIN = Origin(55.7558264, 37.6172996)


class VisibleText(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.tags = []
        self.feed(text)
        self.close()

    def handle_data(self, data):
        self.parts.append(data)

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)

    def handle_endtag(self, tag):
        self.tags.append(tag)

    @property
    def text(self):
        return "".join(self.parts)


@pytest.mark.parametrize("limit", range(1, 6))
def test_start_text(limit):
    assert start_text(limit) == (
        f"Отправь геопозицию — покажу {limit} ближайших коворкинга из подборки "
        "с оценкой, описанием и маршрутами в Яндекс Картах")


def test_exact_ui_constants():
    assert LOCATION_BUTTON_TEXT == "📍 Отправить геопозицию"
    assert INTRO_TEXT == "Ближайшие коворкинги из подборки. Расстояние указано по прямой; время в пути смотри в Яндекс Картах"
    assert FALLBACK_TEXT == "Пришли геопозицию через кнопку ниже или через меню вложений Telegram"
    assert INVALID_ORIGIN_TEXT == "Не получилось прочитать геопозицию. Отправь её ещё раз"
    assert EMPTY_TEXT == "В подборке пока нет коворкингов"
    assert GROUP_TEXT == "Открой личный чат с ботом и отправь геопозицию"
    assert HELP_TEXT == ("Пришли геопозицию через кнопку ниже или через меню вложений Telegram. "
                         "Места, оценки и описания — из каталога владельца. Расстояние указано по прямой; "
                         "маршрут и время в пути смотри в Яндекс Картах")


@pytest.mark.parametrize("distance,expected", [
    (0, "0 м"), (.5, "1 м"), (2.5, "3 м"), (999.4, "999 м"),
    (999.5, "1000 м"), (999.6, "1000 м"), (999.999, "1000 м"),
    (1000, "1,0 км"), (1049.9999, "1,0 км"), (1050, "1,1 км"),
    (1150, "1,2 км"), (1250, "1,3 км"), (20015086.79602057, "20015,1 км"),
])
def test_rounding_999_1000_halfup(distance, expected):
    assert format_distance(distance) == expected
    assert render_card(SearchResult(BASE, distance), 1, ORIGIN).text.splitlines()[2] == (
        "📏 Примерно " + expected + " по прямой")


def test_card_order_catalog_source_and_unchanged_inputs():
    record = replace(BASE, rating_text="8/10", short_review="Тихо.", description="Из каталога.")
    result = SearchResult(record, 1250)
    before = record.to_mapping()
    card = render_card(result, 2, ORIGIN)
    assert type(card) is Card
    assert card.text == ("2. Название\n📍 Тестовый город, дом 1\n📏 Примерно 1,3 км по прямой\n"
                         "⭐ Оценка из списка: 8/10\n💬 Тихо.\nИз каталога.")
    assert record.to_mapping() == before
    assert result == SearchResult(record, 1250) and ORIGIN == Origin(55.7558264, 37.6172996)


@pytest.mark.parametrize("checked,expected", [(date(1, 1, 2), "02.01.0001"),
                                             (date(2024, 2, 29), "29.02.2024"),
                                             (date(9999, 12, 31), "31.12.9999")])
def test_yandex_source_stored_dates(checked, expected):
    record = replace(BASE, rating_text="4,7/5", rating_source="yandex", rating_checked_at=checked,
                     yandex_maps_url="https://yandex.ru/maps/org/synthetic")
    card = render_card(SearchResult(record, 0), 1, ORIGIN)
    assert card.text.splitlines()[3] == f"⭐ Рейтинг Яндекс Карт: 4,7/5 · проверен {expected}"
    assert "Оценка из списка" not in card.text


@pytest.mark.parametrize("source", ["catalog", "yandex"])
def test_absent_rating_and_exact_fallbacks(source):
    record = replace(BASE, rating_source=source)
    card = render_card(SearchResult(record, 0), 1, ORIGIN)
    assert card.text == ("1. Название\n📍 Тестовый город, дом 1\n📏 Примерно 0 м по прямой\n"
                         "💬 Краткая оценка пока не добавлена\nОписание пока не добавлено")
    assert "⭐" not in card.text
    assert len(card.button_rows) == 2


@pytest.mark.parametrize("origin,expected", [
    (ORIGIN, "55.755826,37.6173~55.76,37.62"),
    (Origin(-33.8688201, 151.2092962), "-33.86882,151.209296~55.76,37.62"),
])
def test_button_rows_request_origin_and_optional_org(origin, expected):
    url = "HTTPS://YANDEX.RU:443/maps/org/synthetic?a=1&b=2#fragment"
    record = replace(BASE, yandex_maps_url=url)
    card = render_card(SearchResult(record, 0), 1, origin)
    assert tuple(tuple(b.text for b in row) for row in card.button_rows) == (
        ("🚶 Пешком", "🚇 Транспорт"), ("🚗 На машине",), ("📍 Место в Яндекс Картах",))
    for button, mode in zip(card.button_rows[0] + card.button_rows[1], ("pd", "mt", "auto")):
        parsed = urlsplit(button.url)
        assert (parsed.scheme, parsed.netloc, parsed.path) == ("https", "yandex.ru", "/maps/")
        assert parse_qs(parsed.query) == {"rtext": [expected], "rtt": [mode]}
    assert card.button_rows[2][0].url == url


def test_html_once_all_five_fields():
    value = ' &amp; <b> > " \' '
    record = replace(BASE, name=value, address=value, rating_text=value, short_review=value, description=value)
    card = render_card(SearchResult(record, 0), 1, ORIGIN)
    encoded = ' &amp;amp; &lt;b&gt; &gt; &quot; &#x27; '
    assert card.text == (f"1. {encoded}\n📍 {encoded}\n📏 Примерно 0 м по прямой\n"
                         f"⭐ Оценка из списка: {encoded}\n💬 {encoded}\n{encoded}")
    parsed = VisibleText(card.text)
    assert not parsed.tags
    assert parsed.text == (f"1. {value}\n📍 {value}\n📏 Примерно 0 м по прямой\n"
                           f"⭐ Оценка из списка: {value}\n💬 {value}\n{value}")


@pytest.mark.parametrize("mixed", [False, True])
def test_max_utf16_html_once(mixed):
    def field(length):
        return ("&<>\"'" + "😀" * (length - 5)) if mixed else "😀" * length
    record = replace(BASE, name=field(150), address=field(250), rating_text=field(50),
                     short_review=field(200), description=field(500), rating_source="yandex",
                     rating_checked_at=date(9999, 12, 31), yandex_maps_url="https://yandex.ru/maps/")
    card = render_card(SearchResult(record, 20015086.79602057), 5, ORIGIN)
    parsed = VisibleText(card.text)
    assert not parsed.tags
    assert parsed.text == (f"5. {record.name}\n📍 {record.address}\n📏 Примерно 20015,1 км по прямой\n"
                           f"⭐ Рейтинг Яндекс Карт: {record.rating_text} · проверен 31.12.9999\n"
                           f"💬 {record.short_review}\n{record.description}")
    assert len(parsed.text.encode("utf-16-le")) // 2 <= 2556 < 4096


def test_accepted_long_org_url_unchanged(tmp_path):
    from coworking_nearby.catalog import load_catalog

    url = "https://yandex.ru/maps/org/synthetic?q=" + "x" * 20000 + "&a=%20#tail"
    path = tmp_path / "synthetic.json"
    path.write_text(json.dumps([BASE.to_mapping() | {"yandex_maps_url": url}]))
    record, = load_catalog(path)
    card = render_card(SearchResult(record, 0), 1, ORIGIN)
    assert card.button_rows[2][0].url == url
    assert url not in card.text


def test_domain_imports_and_calls_inert_without_io_or_geo():
    script = '''
import builtins, io, os, socket, math, decimal, urllib.parse
from coworking_nearby.models import Origin, Coworking, SearchResult, RouteMode
import sys
original = builtins.__import__
def guarded(name, *args, **kwargs):
    if name in {"geo", "coworking_nearby.geo", "aiogram"}:
        raise AssertionError("forbidden import")
    return original(name, *args, **kwargs)
def denied(*args, **kwargs):
    raise AssertionError("I/O or environment access")
builtins.open = io.open = os.getenv = socket.socket = denied
os._Environ.__getitem__ = denied
from coworking_nearby.geo import validate_origin, find_nearest
from coworking_nearby.routes import build_yandex_route_url
sys.modules.pop("coworking_nearby.geo")
builtins.__import__ = guarded
from coworking_nearby.render import render_card, start_text
origin = validate_origin(0, 0)
record = Coworking("synthetic", "Test", "Test", 0, 0)
result, = find_nearest(origin, (record,), 1)
assert render_card(result, 1, origin).text
assert start_text(3)
assert build_yandex_route_url(origin, record, RouteMode.WALK)
assert not any(n.split(".")[0] in {"aiogram", "aiohttp", "pydantic"} for n in sys.modules)
assert "coworking_nearby.geo" not in sys.modules
'''
    result = subprocess.run([sys.executable, "-B", "-c", script], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
