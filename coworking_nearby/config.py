"""Strict, secret-safe configuration; environment access occurs only on request."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


type ConfigField = Literal["BOT_TOKEN", "CATALOG_PATH", "RESULTS_LIMIT", "LOG_LEVEL", "ADMIN_IDS", "STATE_PATH"]
type ConfigCode = Literal["required", "invalid"]
type LogLevel = Literal["CRITICAL", "FATAL", "ERROR", "WARNING", "WARN", "INFO", "DEBUG", "NOTSET"]

_LOG_LEVELS = frozenset({"CRITICAL", "FATAL", "ERROR", "WARNING", "WARN", "INFO", "DEBUG", "NOTSET"})


class ConfigurationError(ValueError):
    """Fixed field/code only; never attach the input mapping or offending value."""

    def __init__(self, field: ConfigField, code: ConfigCode) -> None:
        self.field = field
        self.code = code
        super().__init__(f"{field}: {code}")


@dataclass(frozen=True, slots=True, repr=False)
class Settings:
    bot_token: str = field(repr=False)
    catalog_path: Path = Path("data/coworkings.json")
    results_limit: int = 3
    log_level: LogLevel = "INFO"
    admin_ids: tuple[int, ...] = field(default=(), repr=False)
    state_path: Path = Path("state/community.sqlite3")

    def __repr__(self) -> str:
        return "Settings(<redacted>)"


def load_mapping(environment: Mapping[str, object]) -> Settings:
    """Validate string configuration without coercion, mutation or environment I/O."""
    token = environment.get("BOT_TOKEN")
    if type(token) is not str or not token.strip():
        raise ConfigurationError("BOT_TOKEN", "required")

    path = environment.get("CATALOG_PATH", "data/coworkings.json")
    if type(path) is not str or not path.strip() or "\x00" in path:
        raise ConfigurationError("CATALOG_PATH", "invalid")

    limit = environment.get("RESULTS_LIMIT", "3")
    if type(limit) is not str or len(limit) != 1 or limit not in "12345":
        raise ConfigurationError("RESULTS_LIMIT", "invalid")

    level = environment.get("LOG_LEVEL", "INFO")
    if type(level) is not str or level not in _LOG_LEVELS:
        raise ConfigurationError("LOG_LEVEL", "invalid")

    raw_ids = environment.get("ADMIN_IDS", "")
    if type(raw_ids) is not str:
        raise ConfigurationError("ADMIN_IDS", "invalid")
    pieces = raw_ids.split(",") if raw_ids.strip() else []
    if any(not piece.strip().isascii() or not piece.strip().isdigit()
           or len(piece.strip()) > 19 for piece in pieces):
        raise ConfigurationError("ADMIN_IDS", "invalid")
    admin_ids = tuple(int(piece.strip()) for piece in pieces)
    if any(not 0 < identity < 2**63 for identity in admin_ids) or len(set(admin_ids)) != len(admin_ids):
        raise ConfigurationError("ADMIN_IDS", "invalid")
    state_path = environment.get("STATE_PATH", "state/community.sqlite3")
    if type(state_path) is not str or not state_path.strip() or "\x00" in state_path:
        raise ConfigurationError("STATE_PATH", "invalid")
    return Settings(token, Path(path), int(limit), level, admin_ids, Path(state_path))


def load_settings(environment: Mapping[str, object] | None = None) -> Settings:
    """Read os.environ at call time unless an explicit mapping (even {}) is given."""
    if environment is None:
        import os

        environment = os.environ
    return load_mapping(environment)
