"""Immutable, framework-neutral values shared by future consumers.

Coworking represents an already normalized and validated SPEC-001 record.
Construction is not catalogue acceptance: the future shared loader must enforce
ALL C01–C08 rules, including URL grammar and conditional provenance. These types
do not parse input, trim/coerce values, load files or consult the environment.
Nullable fields use None internally; to_mapping omits their absent keys.
Dates are datetime.date (not datetime), serialized with isoformat as the stable
ASCII, zero-padded Gregorian YYYY-MM-DD, including years 0001 and 9999.
"""

from dataclasses import dataclass, fields
from datetime import date
from enum import StrEnum
from pathlib import Path
from typing import Literal


type RatingSource = Literal["catalog", "yandex"]
type DiagnosticClass = Literal[
    "configuration/file", "encoding", "JSON", "root", "entry", "unknown_field",
    "required", "type", "length", "duplicate_id", "number", "range", "date",
    "URL", "conditional",
]
type CatalogValue = str | int | float | bool


@dataclass(frozen=True, slots=True)
class Coworking:
    id: str
    name: str
    address: str
    latitude: int | float
    longitude: int | float
    active: bool = True
    yandex_maps_url: str | None = None
    short_review: str | None = None
    description: str | None = None
    rating_text: str | None = None
    rating_source: RatingSource = "catalog"
    rating_checked_at: date | None = None
    updated_at: date | None = None

    def to_mapping(self) -> dict[str, CatalogValue]:
        """Return a detached normalized mapping; absent nullable keys are omitted."""
        result: dict[str, CatalogValue] = {}
        for field in fields(self):
            value = getattr(self, field.name)
            if value is not None:
                result[field.name] = value.isoformat() if isinstance(value, date) else value
        return result


@dataclass(frozen=True, slots=True)
class Origin:
    latitude: int | float
    longitude: int | float


@dataclass(frozen=True, slots=True)
class SearchResult:
    record: Coworking
    distance_m: float


class RouteMode(StrEnum):
    WALK = "pd"
    TRANSIT = "mt"
    CAR = "auto"


@dataclass(frozen=True, slots=True)
class UrlButton:
    text: str
    url: str


@dataclass(frozen=True, slots=True)
class Card:
    text: str
    button_rows: tuple[tuple[UrlButton, ...], ...]

    def __post_init__(self) -> None:
        # Reject mutable containers rather than retaining or coercing them.
        if type(self.button_rows) is not tuple or any(
            type(row) is not tuple or any(type(button) is not UrlButton for button in row)
            for row in self.button_rows
        ):
            raise TypeError("button_rows must contain immutable URL button tuples")


@dataclass(frozen=True, slots=True)
class CatalogDiagnostic:
    """C03 context value, not an exception or a bot-log serialization format.

Bot callers must map this to fixed safe codes; path/id are CLI-only context.
None denotes unavailable pre-entry context. index is zero-based; a duplicate
may additionally identify its earlier conflicting_index. No raw value/message.
"""

    path: Path
    error_class: DiagnosticClass
    field: str
    record_id: str | None = None
    index: int | None = None
    conflicting_index: int | None = None
    line: int | None = None
    column: int | None = None
