"""SPEC-001 C01–C08 / T01–T24; all places and values are synthetic.

Generator: coder/coworking-20261019-01. These are generator checks, not
independent certification. Startup composition belongs to a later wave.
"""

from dataclasses import FrozenInstanceError
from datetime import date
from contextlib import redirect_stderr, redirect_stdout
import importlib
import io
import json
from pathlib import Path
import subprocess
import sys

import pytest


BASE = dict(id="synthetic-001", name="SYNTHETIC", address="Synthetic city, Example 1", latitude=0, longitude=0)
TRIM = "\t\n\v\f\r \x85\xa0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u2028\u2029\u202f\u205f\u3000"
NULLABLE = ("yandex_maps_url", "short_review", "description", "rating_text", "rating_checked_at", "updated_at")
LIMITS = [("id", 64), ("name", 150), ("address", 250), ("short_review", 200), ("description", 500), ("rating_text", 50)]
MISSING = object()


def api():
    return importlib.import_module("coworking_nearby.catalog")


def write(tmp_path, value):
    path = tmp_path / "synthetic.json"
    path.write_text(json.dumps(value, ensure_ascii=True), encoding="utf-8")
    return path


def load(tmp_path, **updates):
    path = write(tmp_path, [BASE | updates])
    records = api().load_catalog(path)
    with redirect_stdout(io.StringIO()) as output, redirect_stderr(io.StringIO()) as errors:
        assert api().main([str(path)]) == 0
    assert output.getvalue() == errors.getvalue() == ""
    return records


def failure(path, error_class, field=None, index=0, record_id="synthetic-001"):
    with pytest.raises(api().CatalogError) as caught:
        api().load_catalog(path)
    d = caught.value.diagnostic
    assert d.path == path
    assert d.error_class == error_class
    if field is not None:
        assert d.field == field
    assert d.index == index
    assert d.record_id == record_id
    # Every negative variant goes through the actual CLI's shared loader too.
    with redirect_stdout(io.StringIO()) as output, redirect_stderr(io.StringIO()) as errors:
        assert api().main([str(path)]) == 1
    assert output.getvalue() == ""
    assert errors.getvalue().strip() == api().format_diagnostic(d)
    return d


def bad(tmp_path, field, value, error_class):
    entry = BASE.copy()
    if value is MISSING:
        del entry[field]
    else:
        entry[field] = value
    identifier = None if field == "id" else BASE["id"]
    return failure(write(tmp_path, [entry]), error_class, field, record_id=identifier)


def test_T01_defaults(tmp_path):
    records = load(tmp_path)
    assert type(records) is tuple
    r, = records
    assert r.to_mapping() == BASE | dict(active=True, rating_source="catalog")
    with pytest.raises(FrozenInstanceError):
        r.name = "changed"


@pytest.mark.parametrize("field", ["id", "name", "address"])
@pytest.mark.parametrize("value,code", [(MISSING, "required"), (None, "required"), ("", "required"), (TRIM, "required"), (1, "type"), (False, "type"), ([], "type"), ({}, "type")])
def test_T02_required(tmp_path, field, value, code):
    bad(tmp_path, field, value, code)


@pytest.mark.parametrize("field,limit", LIMITS)
@pytest.mark.parametrize("character", ["x", "😀"])
def test_T03_codepoint_limits(tmp_path, field, limit, character):
    value = character * limit
    assert getattr(load(tmp_path, **{field: TRIM + value + TRIM})[0], field) == value
    entry = BASE | {field: value + character}
    failure(write(tmp_path, [entry]), "length", field, record_id=(value + character if field == "id" else BASE["id"]))


@pytest.mark.parametrize("field", NULLABLE)
@pytest.mark.parametrize("value", [None, "", TRIM])
def test_T04_absence(tmp_path, field, value):
    r = load(tmp_path, **{field: value})[0]
    assert getattr(r, field) is None
    assert field not in r.to_mapping()


@pytest.mark.parametrize("value", ["", TRIM, " catalog "])
def test_T04_source_default(tmp_path, value):
    assert load(tmp_path, rating_source=value)[0].rating_source == "catalog"


@pytest.mark.parametrize("field", NULLABLE + ("rating_source",))
@pytest.mark.parametrize("value", [1, False, [], {}])
def test_T05_types(tmp_path, field, value):
    bad(tmp_path, field, value, "type")


@pytest.mark.parametrize("value", [None, "", "true", 0, 1, [], {}])
def test_T05_active(tmp_path, value):
    bad(tmp_path, "active", value, "type")


@pytest.mark.parametrize("value", [None, "Catalog", "YANDEX", "other"])
def test_T05_source(tmp_path, value):
    bad(tmp_path, "rating_source", value, "type")


@pytest.mark.parametrize("lat,lon", [(-90, -180), (90, 180), (0, 0), (-0.25, -0.5)])
def test_T06_bounds(tmp_path, lat, lon):
    r = load(tmp_path, latitude=lat, longitude=lon)[0]
    assert (r.latitude, r.longitude) == (lat, lon)


@pytest.mark.parametrize("field,value", [("latitude", -90.001), ("latitude", 90.001), ("longitude", -180.001), ("longitude", 180.001)])
def test_T06_range(tmp_path, field, value):
    bad(tmp_path, field, value, "range")


@pytest.mark.parametrize("field", ["latitude", "longitude"])
@pytest.mark.parametrize("value", ["0", True, False, None, [], {}])
def test_T07_numbers(tmp_path, field, value):
    bad(tmp_path, field, value, "type")


@pytest.mark.parametrize("field", ["latitude", "longitude"])
def test_T07_missing(tmp_path, field):
    bad(tmp_path, field, MISSING, "required")


@pytest.mark.parametrize("literal,code", [("NaN", "JSON"), ("Infinity", "JSON"), ("-Infinity", "JSON"), ("1e309", "number"), ("-1e309", "number")])
def test_T07_nonfinite(tmp_path, literal, code):
    path = write(tmp_path, [BASE])
    path.write_text(path.read_text().replace('"latitude": 0', '"latitude": ' + literal))
    failure(path, code, "$json" if code == "JSON" else "latitude", index=None if code == "JSON" else 0, record_id=None if code == "JSON" else BASE["id"])


def test_T08_samecoords(tmp_path):
    records = api().load_catalog(write(tmp_path, [BASE, BASE | dict(id="synthetic-002")]))
    assert len(records) == 2
    assert records[0].latitude == records[1].latitude == 0


def test_T09_identity(tmp_path):
    path = write(tmp_path, [BASE | dict(id=" a "), BASE | dict(id="a")])
    d = failure(path, "duplicate_id", "id", index=1, record_id="a")
    assert d.conflicting_index == 0
    records = api().load_catalog(write(tmp_path, [BASE | dict(id=x) for x in ["a", "A", "é", "e\u0301", "Ａ"]]))
    assert [r.id for r in records] == ["a", "A", "é", "e\u0301", "Ａ"]


@pytest.mark.parametrize("field", ["Name", "unknown", " id", "description "])
def test_T09_unknown(tmp_path, field):
    failure(write(tmp_path, [BASE | {field: "ignored?"}]), "unknown_field", field)


@pytest.mark.parametrize("field", ["rating_checked_at", "updated_at"])
@pytest.mark.parametrize("value", ["2024-02-29", "2000-02-29", "0001-01-01", "9999-12-31", "2099-01-01"])
def test_T10_valid_dates(tmp_path, field, value):
    r = load(tmp_path, **{field: TRIM + value + TRIM})[0]
    assert getattr(r, field) == date.fromisoformat(value)
    assert type(getattr(r, field)) is date
    assert r.to_mapping()[field] == value


@pytest.mark.parametrize("field", ["rating_checked_at", "updated_at"])
@pytest.mark.parametrize("value", ["1900-02-29", "2025-02-29", "2026-04-31", "0000-01-01", "10000-01-01", "2026-2-01", "2026-01-1", "2026-01-01T00:00:00", "２０２６-01-01", "20260101", "2026-00-01", "2026-01-00"])
def test_T11_invalid_dates(tmp_path, field, value):
    bad(tmp_path, field, value, "date")


VALID_URLS = ["https://yandex.ru/maps", "https://yandex.com/maps/org/demo", "HTTPS://YANDEX.RU:443/maps/?q=a%20b#x", "https://yandex.ru/maps/-/synthetic", "https://yandex.ru/maps/%20x", "https://yandex.ru/maps/a..b", "https://yandex.ru/maps/.hidden", "https://yandex.ru/maps/%252F?q=%2f#%2F", "https://yandex.ru/maps/?x=" + "a" * 20000]


@pytest.mark.parametrize("url", VALID_URLS)
def test_T12_url_valid(tmp_path, url):
    assert load(tmp_path, yandex_maps_url=TRIM + url + TRIM)[0].yandex_maps_url == url


@pytest.mark.parametrize("url", ["http://yandex.ru/maps", "javascript:alert(1)", "/maps", "//yandex.ru/maps", "https:///maps", "https://evil.test/maps", "https://sub.yandex.ru/maps", "https://www.yandex.ru/maps", "https://yandex.ru.evil/maps", "https://user@yandex.ru/maps", "https://@yandex.ru/maps", "https://:pass@yandex.ru/maps", "https://yandex.ru@evil/maps", "https://yandex.ru./maps", "https://%79andex.ru/maps", "https://yаndex.ru/maps", "https://[yandex.ru/maps", "https://127.0.0.1/maps", "https://[::1]/maps"])
def test_T13_url_authority(tmp_path, url):
    bad(tmp_path, "yandex_maps_url", url, "URL")


@pytest.mark.parametrize("suffix", [":80/maps", ":0443/maps", ":/maps", ":x/maps", ":443:443/maps", "/mapsx", "/MAPS", "", "/%6Daps", "//maps", "/maps/../x", "/maps/./x", "/maps/%2e%2E/x", "/maps/.%2e", "/maps/%2E", "/maps/a%2fb", "/maps/a%2Fb", "/maps/%5c"])
def test_T14_url_path_ports(tmp_path, suffix):
    bad(tmp_path, "yandex_maps_url", "https://yandex.ru" + suffix, "URL")


@pytest.mark.parametrize("component", ["/maps/x{}x", "/maps/?q=x{}x", "/maps/#x{}x"])
@pytest.mark.parametrize("invalid", list(TRIM) + ["\x00", "\x1c", "\x1f", "\x7f", "\\", "%", "%G0", "%0", "%00", "%1F", "%7f", "%5C"])
def test_T15_url_encoding(tmp_path, component, invalid):
    bad(tmp_path, "yandex_maps_url", "https://yandex.ru" + component.format(invalid), "URL")


@pytest.mark.parametrize("url", ["https://ya.ru/abc", "https://yandex.ru/-/abc", "https://yandex.com/navi/abc"])
def test_T16_shortlinks(tmp_path, url):
    bad(tmp_path, "yandex_maps_url", url, "URL")


@pytest.mark.parametrize("field", ["yandex_maps_url", "rating_checked_at"])
@pytest.mark.parametrize("absent", [MISSING, None, "", TRIM])
def test_T17_yandex_dependencies(tmp_path, field, absent):
    entry = BASE | dict(rating_text="4,7/5", rating_source="yandex", yandex_maps_url=VALID_URLS[0], rating_checked_at="2024-02-29")
    if absent is MISSING:
        del entry[field]
    else:
        entry[field] = absent
    failure(write(tmp_path, [entry]), "conditional", field)


def test_T17_valid_provenance(tmp_path):
    r = load(tmp_path, rating_text="4,7/5", rating_source=" yandex ", yandex_maps_url=VALID_URLS[0], rating_checked_at="2024-02-29")[0]
    assert r.rating_text == "4,7/5" and r.rating_source == "yandex"


@pytest.mark.parametrize("rating", [None, "", TRIM])
def test_T18_optional_rating(tmp_path, rating):
    assert load(tmp_path, rating_text=rating, rating_source="yandex")[0].rating_text is None
    assert load(tmp_path, rating_text="8/10")[0].rating_text == "8/10"
    for field, value, code in [("yandex_maps_url", "https://evil.test", "URL"), ("rating_checked_at", "bad", "date")]:
        failure(write(tmp_path, [BASE | {field: value, "rating_source": "yandex", "rating_text": rating}]), code, field)


@pytest.mark.parametrize("entries", [[], [BASE], [BASE, BASE | dict(id="synthetic-002")], [BASE | dict(active=False)]])
def test_T19_cardinality(tmp_path, entries):
    records = api().load_catalog(write(tmp_path, entries))
    assert len(records) == len(entries)
    assert [r.active for r in records] == [e.get("active", True) for e in entries]


@pytest.mark.parametrize("changes,code,field", [(dict(updated_at="bad"), "date", "updated_at"), (dict(description=1), "type", "description"), (dict(typo="x"), "unknown_field", "typo")])
def test_T20_inactive_invalid(tmp_path, changes, code, field):
    failure(write(tmp_path, [BASE | dict(active=False) | changes]), code, field)


@pytest.mark.parametrize("raw,code,field", [(b"\xff", "encoding", "$encoding"), (b"\xef\xbb\xbf[]", "encoding", "$encoding"), (b"[", "JSON", "$json"), (b'[{"id":"a","id":"b"}]', "JSON", "$json"), (b'[{"id":"a","\\u0069d":"b"}]', "JSON", "$json"), (b'[{"x":{"z":1,"z":2}}]', "JSON", "$json"), (b'["\\ud800"]', "JSON", "$json"), (b'[{"\\udfff":0}]', "JSON", "$json"), (b'[{"x":["\\ud800"]}]', "JSON", "$json"), (b"{}", "root", "$root"), (b"null", "root", "$root"), (b"true", "root", "$root")])
def test_T21_input(tmp_path, raw, code, field):
    path = tmp_path / "synthetic.json"
    path.write_bytes(raw)
    failure(path, code, field, index=None, record_id=None)


@pytest.mark.parametrize("entry", [None, "x", [], 1, False])
def test_T21_entry(tmp_path, entry):
    failure(write(tmp_path, [entry]), "entry", "index", record_id=None)


def test_T21_file(tmp_path, monkeypatch):
    path = tmp_path / "missing.json"
    failure(path, "configuration/file", "$file", index=None, record_id=None)
    failure(tmp_path, "configuration/file", "$file", index=None, record_id=None)
    def unreadable(self):
        raise PermissionError("synthetic private OS message")
    monkeypatch.setattr(Path, "read_bytes", unreadable)
    failure(path, "configuration/file", "$file", index=None, record_id=None)


def test_T21_json_location(tmp_path):
    path = tmp_path / "synthetic.json"
    path.write_text('[\n {"id": }\n]')
    d = failure(path, "JSON", "$json", index=None, record_id=None)
    assert d.line == 2 and d.column == 9


def test_T22_atomic_shared_entrypoints(tmp_path, capsys):
    path = write(tmp_path, [BASE, BASE | dict(id=" last ", description=42)])
    d = failure(path, "type", "description", index=1, record_id="last")
    assert api().main([str(path)]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.strip() == api().format_diagnostic(d)
    assert "42" not in captured.err


def test_T23_preserve(tmp_path):
    text = ' & <tag' + chr(62) + ' "quoted" \'single\'  two\tspaces\x1c\u200b\ufeff '
    r = load(tmp_path, name=text, description=text, id="\x1c\u200b\ufeffa\ufeff\u200b\x1c")[0]
    assert r.name == text[1:-1] and r.description == text[1:-1]
    assert r.id == "\x1c\u200b\ufeffa\ufeff\u200b\x1c"


def test_T24_owner_boundary(tmp_path):
    assert load(tmp_path, address="No house", yandex_maps_url="https://yandex.ru/maps/?ll=37,55")[0].address == "No house"
    entry = BASE | dict(yandex_maps_url="https://yandex.ru/maps/?ll=37,55")
    del entry["latitude"]
    failure(write(tmp_path, [entry]), "required", "latitude")


def test_snapshot_restart(tmp_path):
    path = write(tmp_path, [BASE])
    old = api().load_catalog(path)
    path.write_text("[]")
    assert len(old) == 1 and api().load_catalog(path) == ()


def test_cli_usage_and_defaults(tmp_path, monkeypatch, capsys):
    (tmp_path / "data").mkdir()
    (tmp_path / "data/coworkings.json").write_text("[]")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("CATALOG_PATH", "does-not-exist")
    assert api().main([]) == 0
    with pytest.raises(SystemExit) as caught:
        api().main(["one", "two"])
    assert caught.value.code == 2
    assert "usage:" in capsys.readouterr().err


@pytest.mark.parametrize("content,arguments,code", [("[]", None, 0), ("[", None, 1), ("[]", ["--help"], 0), ("[]", ["one", "two"], 2), ("[]", ["missing-synthetic.json"], 1)])
def test_standalone_no_environment_sdk_network(tmp_path, content, arguments, code):
    path = tmp_path / "synthetic.json"
    path.write_text(content)
    script = '''
import os, sys, socket, runpy
class ContractEnvironment(dict):
    def __getitem__(self, key):
        if key in {"BOT_TOKEN", "CATALOG_PATH", "RESULTS_LIMIT", "LOG_LEVEL"}:
            raise AssertionError("application environment read: " + key)
        return super().__getitem__(key)
    def get(self, key, default=None):
        try: return self[key]
        except KeyError: return default
    def __contains__(self, key):
        self.get(key)
        return super().__contains__(key)
os.environ = ContractEnvironment(os.environ)
def denied(*a, **k): raise AssertionError("network")
socket.socket = denied
socket.getaddrinfo = denied
sys.argv = ["coworking_nearby.catalog"] + sys.argv[1:]
try:
    runpy.run_module("coworking_nearby.catalog", run_name="__main__")
finally:
    assert not any(n.split(".")[0] in {"aiogram", "pydantic", "aiohttp"} for n in sys.modules)
    assert "coworking_nearby.config" not in sys.modules
'''
    result = subprocess.run([sys.executable, "-B", "-c", script] + (arguments if arguments is not None else [str(path)]), capture_output=True, text=True)
    assert result.returncode == code, result.stderr
    assert "Traceback" not in result.stderr


def test_T21_valid_surrogate_pair(tmp_path):
    r = load(tmp_path, name="😀")[0]
    assert r.name == "😀" and len(r.name) == 1


def test_diagnostic_safe_context(tmp_path, capsys):
    path = tmp_path / "line\nbreak.json"
    path.write_text(json.dumps([BASE | dict(id="x\n\x1b[31m", description="PRIVATE-VALUE" * 100)]))
    with pytest.raises(api().CatalogError) as caught:
        api().load_catalog(path)
    text = str(caught.value)
    assert "PRIVATE-VALUE" not in text and "\x1b" not in text and "\n" not in text
    assert "description" in text and "length" in text
    assert api().main([str(tmp_path / "missing")]) == 1
    assert "CATALOG_PATH" in capsys.readouterr().err


def test_real_empty_synthetic_separate():
    assert Path("data/coworkings.json").read_bytes() == b"[]"
    assert api().load_catalog("data/coworkings.json") == ()
    examples = api().load_catalog("examples/coworkings.synthetic.json")
    assert examples and all("SYNTHETIC" in r.name and "synthetic" in r.id for r in examples)



@pytest.mark.parametrize("field", ["latitude", "longitude"])
@pytest.mark.parametrize("sign", [-1, 1])
def test_huge_integer_coordinates(tmp_path, field, sign):
    path = write(tmp_path, [BASE | {field: sign * 10**400}])
    failure(path, "range", field)
    result = subprocess.run([sys.executable, "-B", "-m", "coworking_nearby.catalog", str(path)], capture_output=True, text=True)
    assert result.returncode == 1
    assert "range;" in result.stderr and field in result.stderr
    assert "Traceback" not in result.stderr


def test_long_unknown_field_diagnostic(tmp_path):
    field = "unknown" * 100 + "\n\x1b\"\\😀"
    path = write(tmp_path, [BASE | {field: "PRIVATE-VALUE"}])
    d = failure(path, "unknown_field", field)
    text = api().format_diagnostic(d)
    assert "field=" + json.dumps(field, ensure_ascii=True) in text
    assert "PRIVATE-VALUE" not in text and "\n" not in text and "\x1b" not in text


def test_long_chosen_path_diagnostic(tmp_path):
    path = tmp_path
    for index in range(4):
        path = path / ("synthetic-" + str(index) + "x" * 70)
    path = path / "missing\n\x1b\"😀.json"
    d = failure(path, "configuration/file", "$file", index=None, record_id=None)
    text = api().format_diagnostic(d)
    assert "path=" + json.dumps(str(path), ensure_ascii=True) in text
    assert "\n" not in text and "\x1b" not in text
