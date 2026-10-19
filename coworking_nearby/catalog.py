"""Atomic, stdlib-only SPEC-001 catalogue loader and offline checker.

Generator: coder/coworking-20261019-01. No application configuration, SDK or network dependency.
Syntactic acceptance does not certify the owner's place/address/link semantics.
"""

import argparse
from dataclasses import fields
from datetime import date
import json
import math
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

from .models import CatalogDiagnostic, Coworking, DiagnosticClass


_TRIM = "\t\n\v\f\r \x85\xa0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u2028\u2029\u202f\u205f\u3000"
_FIELDS = frozenset(field.name for field in fields(Coworking))
_LIMITS = {"id": 64, "name": 150, "address": 250, "short_review": 200, "description": 500, "rating_text": 50}
_REQUIRED_TEXT = ("id", "name", "address")
_NULLABLE = ("yandex_maps_url", "short_review", "description", "rating_text", "rating_checked_at", "updated_at")
_HEX = frozenset("0123456789abcdefABCDEF")
_DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}\Z")


def _quoted(value: object) -> str:
    """Preserve exact CLI context while escaping terminal/newline controls."""
    return json.dumps(str(value), ensure_ascii=True)


def format_diagnostic(diagnostic: CatalogDiagnostic) -> str:
    """Deliberate CLI context; bot callers must instead emit fixed safe codes."""
    d = diagnostic
    parts = [d.error_class, "path=" + _quoted(d.path), "field=" + _quoted(d.field)]
    if d.record_id is not None:
        parts.append("id=" + _quoted(d.record_id))
    parts.append("index=" + (str(d.index) if d.index is not None else "N/A"))
    if d.conflicting_index is not None:
        parts.append("conflicting_index=" + str(d.conflicting_index))
    if d.line is not None:
        parts.append("line=" + str(d.line))
    if d.column is not None:
        parts.append("column=" + str(d.column))
    if d.error_class == "configuration/file":
        parts.append("check CATALOG_PATH, file existence and permissions")
    return "; ".join(parts)


class CatalogError(Exception):
    """Failure with an immutable diagnostic; never an accepted partial snapshot."""

    def __init__(self, diagnostic: CatalogDiagnostic) -> None:
        self.diagnostic = diagnostic
        super().__init__(format_diagnostic(diagnostic))


class _InvalidJSON(ValueError):
    """Internal marker without raw member names, constants or input values."""


def _pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise _InvalidJSON()
        result[key] = value
    return result


def _constant(value: str) -> None:
    raise _InvalidJSON()


def _check_unicode(value: object) -> None:
    # Check keys and nested values before schema errors can hide invalid Unicode.
    if isinstance(value, str):
        if any(0xD800 <= ord(c) <= 0xDFFF for c in value):
            raise _InvalidJSON()
    elif isinstance(value, dict):
        for key, child in value.items():
            _check_unicode(key)
            _check_unicode(child)
    elif isinstance(value, list):
        for child in value:
            _check_unicode(child)


def _valid_url(value: str) -> bool:
    # Inspect raw input BEFORE urlsplit, which silently strips some controls.
    if any(c in _TRIM or ord(c) < 32 or ord(c) == 127 or c == "\\" for c in value):
        return False
    position = 0
    while position < len(value):
        if value[position] != "%":
            position += 1
            continue
        digits = value[position + 1:position + 3]
        if len(digits) != 2 or any(c not in _HEX for c in digits):
            return False
        byte = int(digits, 16)
        if byte < 32 or byte in (127, 92):
            return False
        position += 3
    try:
        parsed = urlsplit(value)
    except ValueError:
        return False
    if parsed.scheme.lower() != "https" or not parsed.netloc.isascii():
        return False
    # Full authority comparison deliberately excludes ALL userinfo and port variants.
    if parsed.netloc.lower() not in {"yandex.ru", "yandex.com", "yandex.ru:443", "yandex.com:443"}:
        return False
    path = parsed.path
    if path != "/maps" and not path.startswith("/maps/"):
        return False
    if re.search(r"%2[fF]", path):
        return False
    # One decode only; %252e and query/fragment slashes remain ordinary data.
    if any(unquote(segment) in (".", "..") for segment in path.split("/")):
        return False
    return True


def _record(entry: dict, path: Path, index: int, seen: dict[str, int]) -> Coworking:
    raw_id = entry.get("id")
    record_id = raw_id.strip(_TRIM) if type(raw_id) is str else None
    record_id = record_id or None

    def fail(error_class: DiagnosticClass, field: str, conflicting_index: int | None = None) -> None:
        raise CatalogError(CatalogDiagnostic(path, error_class, field, record_id, index, conflicting_index))

    for key in entry:
        if key not in _FIELDS:
            fail("unknown_field", key)

    normalized = {}
    for field in _REQUIRED_TEXT + _NULLABLE + ("rating_source",):
        value = entry.get(field)
        required = field in _REQUIRED_TEXT
        if required and (field not in entry or value is None):
            fail("required", field)
        if field == "rating_source" and field not in entry:
            value = "catalog"
        if value is None and field in _NULLABLE:
            normalized[field] = None
            continue
        if type(value) is not str:
            fail("type", field)
        value = value.strip(_TRIM)
        if not value:
            if required:
                fail("required", field)
            value = "catalog" if field == "rating_source" else None
        if value is not None and field in _LIMITS and len(value) > _LIMITS[field]:
            fail("length", field)
        normalized[field] = value

    if normalized["id"] in seen:
        fail("duplicate_id", "id", seen[normalized["id"]])

    for field, bound in (("latitude", 90), ("longitude", 180)):
        if field not in entry:
            fail("required", field)
        value = entry[field]
        if type(value) not in (int, float):
            fail("type", field)
        # Avoid converting arbitrary-size JSON integers to float.
        if type(value) is float and not math.isfinite(value):
            fail("number", field)
        if not -bound <= value <= bound:
            fail("range", field)
        normalized[field] = value

    active = entry.get("active", True)
    if type(active) is not bool:
        fail("type", "active")
    normalized["active"] = active
    if normalized["rating_source"] not in ("catalog", "yandex"):
        fail("type", "rating_source")
    for field in ("rating_checked_at", "updated_at"):
        value = normalized[field]
        if value is not None:
            if not _DATE.fullmatch(value):
                fail("date", field)
            try:
                normalized[field] = date.fromisoformat(value)
            except ValueError:
                fail("date", field)
    url = normalized["yandex_maps_url"]
    if url is not None and not _valid_url(url):
        fail("URL", "yandex_maps_url")
    if normalized["rating_text"] is not None and normalized["rating_source"] == "yandex":
        for field in ("yandex_maps_url", "rating_checked_at"):
            if normalized[field] is None:
                fail("conditional", field)
    seen[normalized["id"]] = index
    return Coworking(**normalized)


def load_catalog(path: str | Path) -> tuple[Coworking, ...]:
    """Read once and accept every record, including inactive, or raise CatalogError.

    Each call returns a new immutable snapshot in file order. No cache, partial
    return, fallback, address interpretation or external lookup is performed.
    """
    path = Path(path)
    try:
        raw = path.read_bytes()
    except (OSError, ValueError):
        raise CatalogError(CatalogDiagnostic(path, "configuration/file", "$file")) from None
    try:
        text = raw.decode("utf-8", errors="strict")
        if text.startswith("\ufeff"):
            raise UnicodeError()
    except UnicodeError:
        raise CatalogError(CatalogDiagnostic(path, "encoding", "$encoding")) from None
    try:
        root = json.loads(text, object_pairs_hook=_pairs, parse_constant=_constant)
        _check_unicode(root)
    except json.JSONDecodeError as error:
        diagnostic = CatalogDiagnostic(path, "JSON", "$json", line=error.lineno, column=error.colno)
        raise CatalogError(diagnostic) from None
    except (ValueError, RecursionError):
        raise CatalogError(CatalogDiagnostic(path, "JSON", "$json")) from None
    if type(root) is not list:
        raise CatalogError(CatalogDiagnostic(path, "root", "$root"))
    records = []
    seen = {}
    for index, entry in enumerate(root):
        if type(entry) is not dict:
            raise CatalogError(CatalogDiagnostic(path, "entry", "index", index=index))
        records.append(_record(entry, path, index, seen))
    return tuple(records)


def _arguments(argv: list[str] | None) -> argparse.Namespace:
    """Parse the standalone command using public stdlib argparse."""
    parser = argparse.ArgumentParser(description="Check a local coworking catalogue offline.")
    parser.add_argument("path", nargs="?", default="data/coworkings.json")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Offline CLI: success=0, catalogue failure=1, argparse usage error=2."""
    args = _arguments(argv)
    try:
        load_catalog(args.path)
    except CatalogError as error:
        print(format_diagnostic(error.diagnostic), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
