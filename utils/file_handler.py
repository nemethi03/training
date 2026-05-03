"""Fájlkezelés: JSON mentés/betöltés és CSV exportálás."""

import csv
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Az adatfájlok helye (a utils/ mappából egy szinttel feljebb, aztán data/)
DATA_DIR: Path = Path(__file__).resolve().parent.parent / "data"
DEFAULT_FILE: Path = DATA_DIR / "workouts.json"
DEFAULT_CSV: Path = DATA_DIR / "workouts_export.csv"


def save_to_file(
    data: list[dict], filepath: Path = DEFAULT_FILE
) -> bool:
    """Elmenti a gyakorlatokat JSON fájlba. True ha sikerült, False ha nem."""
    try:
        # Mappa létrehozása, ha nem létezik
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info("Adatok sikeresen mentve: %s", filepath)
        return True

    except (IOError, OSError, TypeError) as e:
        logger.error("Hiba a mentés során: %s", e)
        return False


def load_from_file(filepath: Path = DEFAULT_FILE) -> list[dict]:
    """Betölti a gyakorlatokat JSON fájlból. Ha nincs fájl, üres listával tér vissza."""
    if not filepath.exists():
        logger.info(
            "Adatfájl nem található: %s. Üres naplóval indulunk.",
            filepath,
        )
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        logger.info(
            "Adatok sikeresen betöltve: %s (%d elem)",
            filepath,
            len(data),
        )
        return data

    except json.JSONDecodeError as e:
        logger.warning("Hibás JSON formátum: %s - %s", filepath, e)
        return []
    except (IOError, OSError) as e:
        logger.warning("Hiba a betöltés során: %s", e)
        return []


def export_to_csv(
    exercises: list, filepath: Path = DEFAULT_CSV
) -> bool:
    """Gyakorlatok kiírása CSV fájlba (pl. Excelben megnyitható)."""
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            # Fejléc sor
            writer.writerow([
                "Sorszám", "Dátum", "Típus", "Név", "Részletek"
            ])

            # Adatsorok
            for i, exercise in enumerate(exercises, 1):
                details = _get_exercise_details(exercise)
                writer.writerow([
                    i,
                    exercise.exercise_date.isoformat(),
                    exercise.exercise_type.value,
                    exercise.name,
                    details,
                ])

        logger.info(
            "CSV sikeresen exportálva: %s (%d sor)",
            filepath,
            len(exercises),
        )
        return True

    except (IOError, OSError) as e:
        logger.error("Hiba a CSV exportálás során: %s", e)
        return False


def _get_exercise_details(exercise) -> str:
    """A gyakorlat részleteit adja vissza szövegként (a CSV-hez kell)."""
    from models.exercise import CardioExercise, StrengthExercise

    if isinstance(exercise, CardioExercise):
        return f"{exercise.duration_minutes} perc"
    elif isinstance(exercise, StrengthExercise):
        return f"{exercise.sets}x{exercise.reps} @ {exercise.weight_kg} kg"
    return "-"
