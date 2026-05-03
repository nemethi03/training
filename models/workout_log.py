"""Az edzésnapló kezelése: gyakorlatok tárolása, szűrése, statisztikák."""

import logging
from collections import Counter
from datetime import date

from models.exercise import (
    CardioExercise,
    Exercise,
    ExerciseType,
    StrengthExercise,
)

logger = logging.getLogger(__name__)


class WorkoutLog:
    """Az edzésnapló: tárolja a gyakorlatokat, és lehet szűrni, statisztikát kérni belőlük."""

    def __init__(self) -> None:
        """Üres edzésnapló inicializálása."""
        self._exercises: list[Exercise] = []

    @property
    def exercises(self) -> list[Exercise]:
        """Az összes gyakorlat listája (másolatot ad vissza, hogy ne lehessen kívülről módosítani)."""
        return list(self._exercises)

    @property
    def exercise_count(self) -> int:
        """Az összes rögzített gyakorlat száma."""
        return len(self._exercises)

    def add_exercise(self, exercise: Exercise) -> None:
        """Új gyakorlat hozzáadása a naplóhoz."""
        self._exercises.append(exercise)
        logger.info("Gyakorlat hozzáadva: %s", exercise)

    def remove_exercise(self, index: int) -> Exercise:
        """Gyakorlat törlése index alapján. Ha rossz az index, IndexError-t dob."""
        if index < 0 or index >= len(self._exercises):
            raise IndexError(
                f"Érvénytelen sorszám: {index + 1}. "
                f"Érvényes tartomány: 1-{len(self._exercises)}"
            )
        removed = self._exercises.pop(index)
        logger.info("Gyakorlat törölve: %s", removed)
        return removed

    def get_exercises_by_date(self, target_date: date) -> list[Exercise]:
        """Adott dátumra szűrt gyakorlatok listája."""
        return [
            ex for ex in self._exercises
            if ex.exercise_date == target_date
        ]

    def get_exercises_by_type(
        self, exercise_type: ExerciseType
    ) -> list[Exercise]:
        """Adott típusra szűrt gyakorlatok listája."""
        return [
            ex for ex in self._exercises
            if ex.exercise_type == exercise_type
        ]

    def get_exercises_by_name(self, search_term: str) -> list[Exercise]:
        """Gyakorlatok szűrése név szerint. Kis- és nagybetűt nem különböztet meg."""
        normalized_term = search_term.strip().casefold()
        return [
            ex for ex in self._exercises
            if normalized_term in ex.name.casefold()
        ]

    def get_exercises_by_date_range(
        self, start_date: date, end_date: date
    ) -> list[Exercise]:
        """Két dátum közötti gyakorlatok (mindkét végpont benne van)."""
        return [
            ex for ex in self._exercises
            if start_date <= ex.exercise_date <= end_date
        ]

    def get_available_exercise_names(self) -> list[str]:
        """A naplóban szereplő egyedi gyakorlatnevek abc sorrendben."""
        return sorted({ex.name for ex in self._exercises}, key=str.casefold)

    def get_exercise_name_statistics(self) -> list[dict]:
        """Statisztika konkrét gyakorlatnevek szerint."""
        grouped: dict[str, list[Exercise]] = {}
        for exercise in self._exercises:
            grouped.setdefault(exercise.name, []).append(exercise)

        rows: list[dict] = []
        for name in sorted(grouped, key=str.casefold):
            items = grouped[name]
            cardio_items = [ex for ex in items if isinstance(ex, CardioExercise)]
            strength_items = [ex for ex in items if isinstance(ex, StrengthExercise)]

            row = {
                "name": name,
                "count": len(items),
                "type": items[0].exercise_type.value,
            }

            if cardio_items:
                total_minutes = sum(ex.duration_minutes for ex in cardio_items)
                row["details"] = (
                    f"összesen {total_minutes} perc, átlag {round(total_minutes / len(cardio_items), 1)} perc"
                )
            elif strength_items:
                total_sets = sum(ex.sets for ex in strength_items)
                avg_weight = round(
                    sum(ex.weight_kg for ex in strength_items) / len(strength_items), 1
                )
                avg_reps = sum(ex.reps for ex in strength_items) / len(strength_items) if strength_items else 0
                row["details"] = ( 
                    f"összesen {total_sets} sorozat, átlag: {avg_weight:.1f} kg, {avg_reps:.1f} ismétlés"
                )
            else:
                row["details"] = "-"

            rows.append(row)

        return rows

    def get_statistics(self) -> dict:
        """Összesített statisztikák: darabszámok, átlagok típusonként és név szerint."""
        cardio_exercises = [
            ex for ex in self._exercises
            if isinstance(ex, CardioExercise)
        ]
        strength_exercises = [
            ex for ex in self._exercises
            if isinstance(ex, StrengthExercise)
        ]

        total_cardio_minutes = sum(
            ex.duration_minutes for ex in cardio_exercises
        )
        avg_cardio_minutes = (
            total_cardio_minutes / len(cardio_exercises)
            if cardio_exercises
            else 0.0
        )

        total_strength_sets = sum(
            ex.sets for ex in strength_exercises
        )
        total_strength_reps = sum(
        ex.reps for ex in strength_exercises
        )
        avg_strength_weight = (
            sum(ex.weight_kg for ex in strength_exercises)
            / len(strength_exercises)
            if strength_exercises
            else 0.0
        )
        avg_strength_reps = (
            total_strength_reps / len(strength_exercises)
            if strength_exercises
            else 0.0
        )

        name_counts = Counter(ex.name for ex in self._exercises)
        most_common_name = "-"
        most_common_count = 0
        if name_counts:
            most_common_name, most_common_count = name_counts.most_common(1)[0]

        return {
            "total_count": len(self._exercises),
            "cardio_count": len(cardio_exercises),
            "strength_count": len(strength_exercises),
            "total_cardio_minutes": total_cardio_minutes,
            "avg_cardio_minutes": round(avg_cardio_minutes, 1),
            "total_strength_sets": total_strength_sets,
            "total_strength_reps": total_strength_reps,
            "avg_strength_weight": round(avg_strength_weight, 1),
            "avg_strength_reps": round(avg_strength_reps, 1),
            "unique_name_count": len(name_counts),
            "most_common_name": most_common_name,
            "most_common_name_count": most_common_count,
            "name_stats": self.get_exercise_name_statistics(),
        }

    def to_dict_list(self) -> list[dict]:
        """Összes gyakorlat szótárakká alakítva (mentéshez kell)."""
        return [ex.to_dict() for ex in self._exercises]

    def load_from_dict_list(self, data_list: list[dict]) -> None:
        """Szótárak listájából tölti vissza a gyakorlatokat.
        Ha valamelyik adat hibás, azt kihagyja és megy tovább.
        """
        self._exercises.clear()
        for data in data_list:
            try:
                exercise = Exercise.from_dict(data)
                self._exercises.append(exercise)
            except (KeyError, ValueError) as e:
                logger.warning("Hibás adat kihagyva: %s - %s", data, e)

        logger.info(
            "%d gyakorlat sikeresen betöltve.", len(self._exercises)
        )
