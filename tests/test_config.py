"""FOUNDATION boundaries only; no future application/CLI acceptance claims."""

import asyncio
from dataclasses import FrozenInstanceError, fields
from datetime import date
from pathlib import Path
import socket
import subprocess
import sys

import pytest


def config():
    from coworking_nearby import config
    return config


def test_defaults_and_secret():
    c = config()
    settings = c.load_mapping({"BOT_TOKEN": "synthetic-secret"})
    assert settings.bot_token == "synthetic-secret"
    assert settings.catalog_path == Path("data/coworkings.json")
    assert settings.results_limit == 3
    assert settings.log_level == "INFO"
    assert "synthetic-secret" not in repr(settings)
    assert "synthetic-secret" not in str(settings)
    with pytest.raises(FrozenInstanceError):
        settings.results_limit = 1


def test_settings_repr_never_formats_configuration_values():
    settings = config().load_mapping({"BOT_TOKEN": "synthetic-secret", "CATALOG_PATH": "synthetic-sensitive-path.json"})
    assert "synthetic-sensitive-path" not in repr(settings)


def test_card_cannot_retain_mutable_rows():
    from coworking_nearby.models import Card, UrlButton
    button = UrlButton("Synthetic", "https://yandex.ru/maps/")
    with pytest.raises(TypeError):
        Card("Synthetic", [[button]])
    with pytest.raises(TypeError):
        Card("Synthetic", ([button],))


@pytest.mark.parametrize("limit", list("12345"))
def test_limits(limit):
    assert config().load_mapping({"BOT_TOKEN": "synthetic", "RESULTS_LIMIT": limit}).results_limit == int(limit)


@pytest.mark.parametrize("limit", ["", "0", "6", "12", " 3", "3 ", "+3", "-3", "3.0", "٣", "３", "true", True, False, 3, 3.0, None])
def test_invalid_limits(limit):
    c = config()
    with pytest.raises(c.ConfigurationError) as caught:
        c.load_mapping({"BOT_TOKEN": "synthetic-secret", "RESULTS_LIMIT": limit})
    assert caught.value.field == "RESULTS_LIMIT"
    assert caught.value.code == "invalid"
    assert "synthetic-secret" not in str(caught.value)


@pytest.mark.parametrize("token", [None, "", " ", "\t", False, 123])
def test_required_token(token):
    c = config()
    with pytest.raises(c.ConfigurationError) as caught:
        c.load_mapping({"BOT_TOKEN": token})
    assert str(caught.value) == "BOT_TOKEN: required"
    with pytest.raises(c.ConfigurationError):
        c.load_mapping({})


@pytest.mark.parametrize("level", ["CRITICAL", "FATAL", "ERROR", "WARNING", "WARN", "INFO", "DEBUG", "NOTSET"])
def test_log_levels(level):
    assert config().load_mapping({"BOT_TOKEN": "synthetic", "LOG_LEVEL": level}).log_level == level


@pytest.mark.parametrize("field,value", [("LOG_LEVEL", "synthetic-secret"), ("LOG_LEVEL", "info"), ("LOG_LEVEL", 10), ("LOG_LEVEL", None), ("CATALOG_PATH", ""), ("CATALOG_PATH", " "), ("CATALOG_PATH", None), ("CATALOG_PATH", 1)])
def test_safe_invalid_fields(field, value):
    c = config()
    with pytest.raises(c.ConfigurationError) as caught:
        c.load_mapping({"BOT_TOKEN": "synthetic-secret", field: value})
    assert caught.value.field == field
    assert "synthetic-secret" not in str(caught.value)
    assert "synthetic-secret" not in repr(caught.value)


def test_environment_is_explicit_and_read_at_call(monkeypatch):
    c = config()
    monkeypatch.setenv("BOT_TOKEN", "synthetic-env")
    assert c.load_settings().bot_token == "synthetic-env"
    assert c.load_settings({"BOT_TOKEN": "synthetic-map", "CATALOG_PATH": "other.json"}).catalog_path == Path("other.json")
    with pytest.raises(c.ConfigurationError):
        c.load_settings({})


def test_value_contracts(synthetic_record):
    from coworking_nearby.models import Card, CatalogDiagnostic, Origin, RouteMode, SearchResult, UrlButton

    assert [f.name for f in fields(synthetic_record)] == ["id", "name", "address", "latitude", "longitude", "active", "yandex_maps_url", "short_review", "description", "rating_text", "rating_source", "rating_checked_at", "updated_at"]
    assert synthetic_record.to_mapping() == {"id": "synthetic-001", "name": "SYNTHETIC", "address": "Test city, Example 1", "latitude": 0, "longitude": 0, "active": True, "rating_source": "catalog"}
    origin = Origin(0, -180)
    result = SearchResult(synthetic_record, 0.0)
    assert result.record is synthetic_record
    assert result.distance_m == 0.0
    assert {mode.value for mode in RouteMode} == {"pd", "mt", "auto"}
    button = UrlButton("Synthetic", "https://yandex.ru/maps/")
    card = Card("Synthetic", ((button,),))
    diagnostic = CatalogDiagnostic(Path("synthetic.json"), "type", "active", index=0)
    assert diagnostic.index == 0 and diagnostic.record_id is None
    assert diagnostic.field == "active" and diagnostic.error_class == "type"
    for value, attr in [(synthetic_record, "name"), (origin, "latitude"), (result, "distance_m"), (card, "text"), (button, "text"), (diagnostic, "field")]:
        with pytest.raises(FrozenInstanceError):
            setattr(value, attr, "changed")
    with pytest.raises(TypeError):
        card.button_rows[0][0] = button


def test_dates_and_absence_are_stable(synthetic_record):
    from dataclasses import replace
    record = replace(synthetic_record, active=False, rating_source="yandex", updated_at=date(1, 1, 1), rating_checked_at=date(9999, 12, 31))
    mapping = record.to_mapping()
    assert mapping["updated_at"] == "0001-01-01"
    assert mapping["rating_checked_at"] == "9999-12-31"
    assert mapping["active"] is False and mapping["rating_source"] == "yandex"
    assert "rating_text" not in mapping and "yandex_maps_url" not in mapping
    mapping["name"] = "changed"
    assert record.name == "SYNTHETIC"


def test_imports_are_inert():
    # A fresh interpreter catches import effects hidden by pytest's module cache.
    script = '''
import sys, os, socket, builtins
def denied(*a, **k): raise AssertionError("unexpected import I/O")
class NoEnvironment(dict):
    def __getitem__(self, key): return denied()
    def get(self, *a): return denied()
os.environ = NoEnvironment()
socket.socket = denied
builtins.open = denied
import coworking_nearby
import coworking_nearby.models
import coworking_nearby.config
assert not any(n.split(".")[0] in {"aiogram", "pydantic", "aiohttp"} for n in sys.modules)
'''
    result = subprocess.run([sys.executable, "-B", "-c", script], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert result.stdout == "" and result.stderr == ""


def test_offline_guard_and_asyncio_socketpair():
    with pytest.raises(AssertionError, match="network disabled"):
        socket.getaddrinfo("example.invalid", 443)
    for method in ("connect", "connect_ex", "sendto"):
        with socket.socket() as sock:
            with pytest.raises(AssertionError, match="network disabled"):
                getattr(sock, method)(*( [b"x", ("127.0.0.1", 9)] if method == "sendto" else [("127.0.0.1", 9)] ))
    async def once():
        await asyncio.sleep(0)
        return 1
    assert asyncio.run(once()) == 1
