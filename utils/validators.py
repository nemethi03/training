"""Felhasználói bemenet ellenőrzése: dátum, számok, menüválasztás."""

import logging
from datetime import date, datetime
from typing import Any, Callable

logger = logging.getLogger(__name__)


def validate_date(date_string: str) -> date | None:
    """Megpróbálja ÉÉÉÉ-HH-NN formátumban értelmezni. Ha sikerül, date-et ad, ha nem, None-t."""
    try:
        return datetime.strptime(date_string, "%Y-%m-%d").date()
    except ValueError:
        return None


def validate_positive_integer(value_string: str) -> int | None:
    """Pozitív egész szám ellenőrzése. None-t ad vissza ha nem jó."""
    try:
        value = int(value_string)
        return value if value > 0 else None
    except ValueError:
        return None


def validate_positive_float(value_string: str) -> float | None:
    """Pozitív szám (tizedes is lehet) ellenőrzése."""
    try:
        value = float(value_string)
        return value if value > 0 else None
    except ValueError:
        return None


def validate_menu_choice(value_string: str, max_choice: int) -> int | None:
    """Menüválasztás ellenőrzése: 1 és max_choice között kell lennie."""
    try:
        value = int(value_string)
        return value if 1 <= value <= max_choice else None
    except ValueError:
        return None


def get_valid_input(
    prompt: str,
    validator: Callable[[str], Any],
    error_message: str = "Érvénytelen bemenet! Próbáld újra.",
) -> Any:
    """Addig kérdezi a felhasználót, amíg érvényes választ nem ad.
    A validator függvény None-t ad vissza ha hibás a bemenet.
    """
    while True:
        user_input = input(prompt).strip()
        result = validator(user_input)
        if result is not None:
            return result
        print(f"  {error_message}")
