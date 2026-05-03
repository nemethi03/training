"""Gyakorlat osztályok definíciói: alap, kardió és erőnléti."""

from dataclasses import dataclass
from datetime import date
from enum import Enum


class ExerciseType(Enum):
    """Gyakorlat típusok felsorolása."""

    CARDIO = "kardió"
    STRENGTH = "erőnléti"


@dataclass
class Exercise:
    """Egy gyakorlat alap adatai.

    Ebből származik a CardioExercise és StrengthExercise.
    A from_dict() a típus alapján a megfelelő alosztályt hozza létre.
    """

    name: str
    exercise_date: date
    exercise_type: ExerciseType = ExerciseType.CARDIO

    def to_dict(self) -> dict:
        """Szótárrá alakítás, JSON mentéshez."""
        return {
            "name": self.name,
            "exercise_date": self.exercise_date.isoformat(),
            "exercise_type": self.exercise_type.value,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Exercise":
        """Szótárból visszaállítja a gyakorlatot.

        A típus mező alapján eldönti, hogy kardió vagy erőnléti
        objektumot kell-e létrehozni.
        """
        exercise_type = ExerciseType(data["exercise_type"])
        exercise_date = date.fromisoformat(data["exercise_date"])

        if exercise_type == ExerciseType.CARDIO:
            return CardioExercise(
                name=data["name"],
                exercise_date=exercise_date,
                duration_minutes=data.get("duration_minutes", 0),
            )
        elif exercise_type == ExerciseType.STRENGTH:
            return StrengthExercise(
                name=data["name"],
                exercise_date=exercise_date,
                sets=data.get("sets", 0),
                reps=data.get("reps", 0),
                weight_kg=data.get("weight_kg", 0.0),
            )

        return cls(
            name=data["name"],
            exercise_date=exercise_date,
            exercise_type=exercise_type,
        )

    def format_row(self, index: int) -> str:
        """Egy sor a táblázathoz. Az alosztályok felülírják a saját adataikkal."""
        return (
            f"  {index:>3}. | {self.exercise_date} | "
            f"{self.exercise_type.value:8s} | "
            f"{self.name:20s} | -"
        )

    def __str__(self) -> str:
        """A gyakorlat szöveges megjelenítése."""
        return (
            f"{self.name} ({self.exercise_type.value}) - "
            f"{self.exercise_date}"
        )


@dataclass
class CardioExercise(Exercise):
    """Kardió gyakorlat, pl. futás, kerékpár, úszás. Az időtartamot percben tároljuk."""

    duration_minutes: int = 0

    def __post_init__(self) -> None:
        """Típus beállítása kardióra."""
        self.exercise_type = ExerciseType.CARDIO

    def to_dict(self) -> dict:
        """Szótárrá alakítás az időtartammal együtt."""
        data = super().to_dict()
        data["duration_minutes"] = self.duration_minutes
        return data

    def format_row(self, index: int) -> str:
        """Táblázat sor az időtartammal."""
        return (
            f"  {index:>3}. | {self.exercise_date} | "
            f"{self.exercise_type.value:8s} | "
            f"{self.name:20s} | {self.duration_minutes} perc"
        )

    def __str__(self) -> str:
        """Szöveges megjelenítés, pl.: Futás (kardió) - 2025-03-15 - 30 perc"""
        return (
            f"{self.name} ({self.exercise_type.value}) - "
            f"{self.exercise_date} - {self.duration_minutes} perc"
        )


@dataclass
class StrengthExercise(Exercise):
    """Erőnléti gyakorlat, pl. fekvenyomás, guggolás.
    Sorozatszám, ismétlés és súly (kg) tartozik hozzá.
    """

    sets: int = 0
    reps: int = 0
    weight_kg: float = 0.0

    def __post_init__(self) -> None:
        """Típus beállítása erőnlétire."""
        self.exercise_type = ExerciseType.STRENGTH

    def to_dict(self) -> dict:
        """Szótárrá alakítás a sorozat/ismétlés/súly adatokkal."""
        data = super().to_dict()
        data["sets"] = self.sets
        data["reps"] = self.reps
        data["weight_kg"] = self.weight_kg
        return data

    def format_row(self, index: int) -> str:
        """Táblázat sor a sorozat/ismétlés/súly adatokkal."""
        details = f"{self.sets}x{self.reps} @ {self.weight_kg} kg"
        return (
            f"  {index:>3}. | {self.exercise_date} | "
            f"{self.exercise_type.value:8s} | "
            f"{self.name:20s} | {details}"
        )

    def __str__(self) -> str:
        """Szöveges megjelenítés, pl.: Fekvenyomás (erőnléti) - 2025-03-15 - 3x10 @ 60.0 kg"""
        return (
            f"{self.name} ({self.exercise_type.value}) - "
            f"{self.exercise_date} - "
            f"{self.sets}x{self.reps} @ {self.weight_kg} kg"
        )
