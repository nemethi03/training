"""Edzésterv Napló - a program belépési pontja."""

import logging
import sys
from pathlib import Path

from models.workout_log import WorkoutLog
from ui.console_ui import ConsoleUI

# Napló fájl helye
LOG_DIR: Path = Path(__file__).resolve().parent / "data"


def setup_logging() -> None:
    """Logging beállítása: fájlba minden, konzolra csak a WARNING szint felett."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / "app.log"

    # Fájl handler - részletes naplózás
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    # Konzol handler - csak figyelmeztetések
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)

    # Formátum beállítása
    log_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(log_format)
    console_handler.setFormatter(log_format)

    # Gyökér logger beállítása
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


def main() -> None:
    """Logging beállítás, edzésnapló létrehozás, UI indítás."""
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Program elindítva.")

    workout_log = WorkoutLog()
    ui = ConsoleUI(workout_log)

    try:
        ui.run()
    except KeyboardInterrupt:
        print("\n\n  Program megszakítva.")
        logger.info("Program megszakítva a felhasználó által (Ctrl+C).")
    finally:
        logger.info("Program leállítva.")


if __name__ == "__main__":
    main()
