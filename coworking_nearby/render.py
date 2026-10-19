"""Pure Russian UI and escaped cards for normalized catalogue values."""

from decimal import Decimal, ROUND_HALF_UP
from html import escape
from math import floor

from .models import Card, Origin, RouteMode, SearchResult, UrlButton
from .routes import build_yandex_route_url


LOCATION_BUTTON_TEXT = "📍 Отправить геопозицию"
INTRO_TEXT = "Ближайшие коворкинги из подборки. Расстояние указано по прямой; время в пути смотри в Яндекс Картах"
FALLBACK_TEXT = "Пришли геопозицию через кнопку ниже или через меню вложений Telegram"
INVALID_ORIGIN_TEXT = "Не получилось прочитать геопозицию. Отправь её ещё раз"
EMPTY_TEXT = "В подборке пока нет коворкингов"
HELP_TEXT = ("Пришли геопозицию через кнопку ниже или через меню вложений Telegram. "
             "Места, оценки и описания — из каталога владельца. Расстояние указано по прямой; "
             "маршрут и время в пути смотри в Яндекс Картах")
GROUP_TEXT = "Открой личный чат с ботом и отправь геопозицию"
SHORT_REVIEW_FALLBACK = "Краткая оценка пока не добавлена"
DESCRIPTION_FALLBACK = "Описание пока не добавлено"


def start_text(results_limit: int) -> str:
    """Substitute only the configured result count (1..5)."""
    return (f"Отправь геопозицию — покажу {results_limit} ближайших коворкинга из подборки "
            "с оценкой, описанием и маршрутами в Яндекс Картах")


def format_distance(distance_m: float) -> str:
    """Display nonnegative raw metres, using the raw 1000m threshold."""
    if distance_m < 1000:
        return f"{floor(distance_m + .5)} м"
    kilometres = (Decimal(str(distance_m)) / Decimal(1000)).quantize(
        Decimal("0.1"), rounding=ROUND_HALF_UP)
    return str(kilometres).replace(".", ",") + " км"


def render_card(result: SearchResult, position: int, origin: Origin) -> Card:
    """One escaped text and immutable URL rows; no I/O or distance selection.

    Result, position (1..5), and origin are validated caller inputs. Stored
    organization URLs stay unchanged, without a platform-delivery guarantee.
    """
    record = result.record
    lines = [
        f"{position}. {escape(record.name, quote=True)}",
        f"📍 {escape(record.address, quote=True)}",
        f"📏 Примерно {format_distance(result.distance_m)} по прямой",
    ]
    if record.rating_text is not None:
        rating = escape(record.rating_text, quote=True)
        if record.rating_source == "yandex":
            checked = record.rating_checked_at
            checked_text = f"{checked.day:02d}.{checked.month:02d}.{checked.year:04d}"
            lines.append(f"⭐ Рейтинг Яндекс Карт: {rating} · проверен {checked_text}")
        else:
            lines.append(f"⭐ Оценка из списка: {rating}")
    review = (escape(record.short_review, quote=True) if record.short_review is not None
              else SHORT_REVIEW_FALLBACK)
    description = (escape(record.description, quote=True) if record.description is not None
                   else DESCRIPTION_FALLBACK)
    lines.extend(("💬 " + review, description))
    rows = (
        (UrlButton("🚶 Пешком", build_yandex_route_url(origin, record, RouteMode.WALK)),
         UrlButton("🚇 Транспорт", build_yandex_route_url(origin, record, RouteMode.TRANSIT))),
        (UrlButton("🚗 На машине", build_yandex_route_url(origin, record, RouteMode.CAR)),),
    )
    if record.yandex_maps_url is not None:
        rows += ((UrlButton("📍 Место в Яндекс Картах", record.yandex_maps_url),),)
    return Card("\n".join(lines), rows)
