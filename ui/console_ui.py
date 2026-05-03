"""A program felhasználói felülete: menük, bevitel, megjelenítés."""

import logging
from datetime import date

from models.exercise import (
    CardioExercise,
    Exercise,
    ExerciseType,
    StrengthExercise,
)
from models.workout_log import WorkoutLog
from utils.file_handler import (
    export_to_csv,
    load_from_file,
    save_to_file,
)
from utils.validators import (
    get_valid_input,
    validate_date,
    validate_menu_choice,
    validate_positive_float,
    validate_positive_integer,
)

logger = logging.getLogger(__name__)

MENU_SEPARATOR: str = "=" * 45
TABLE_SEPARATOR: str = "-" * 75
MENU_OPTIONS: int = 8


class ConsoleUI:
    """A konzolos menürendszer. A WorkoutLog-on keresztül kezeli az adatokat."""

    def __init__(self, workout_log: WorkoutLog) -> None:
        """Felhasználói felület inicializálása az edzésnaplóval."""
        self._workout_log = workout_log

    def run(self) -> None:
        """Elindítja a programot: betöltés, menü ciklus, kilépéskor mentés."""
        self._load_data()
        print("\n  Üdvözlünk az Edzésterv Naplóban!")

        running = True
        while running:
            self._show_main_menu()
            choice = get_valid_input(
                "  Válasszon (1-8): ",
                lambda x: validate_menu_choice(x, MENU_OPTIONS),
                f"Érvénytelen választás! Kérem 1-{MENU_OPTIONS} közötti számot.",
            )
            running = self._handle_menu_choice(choice)

        self._ask_save_on_exit()
        print("\n  Viszontlátásra!\n")

    def _show_main_menu(self) -> None:
        """A főmenü megjelenítése."""
        print(f"\n{MENU_SEPARATOR}")
        print("        EDZÉSTERV NAPLÓ")
        print(MENU_SEPARATOR)
        print("  1. Új gyakorlat rögzítése")
        print("  2. Gyakorlatok listázása")
        print("  3. Gyakorlatok szűrése")
        print("  4. Statisztikák")
        print("  5. Gyakorlat törlése")
        print("  6. Exportálás CSV-be")
        print("  7. Mentés")
        print("  8. Kilépés")
        print(MENU_SEPARATOR)

    def _handle_menu_choice(self, choice: int) -> bool:
        """Végrehajtja a választott menüpontot. False = kilépés."""
        menu_actions: dict = {
            1: self._add_exercise,
            2: self._list_exercises,
            3: self._filter_exercises,
            4: self._show_statistics,
            5: self._delete_exercise,
            6: self._export_csv,
            7: self._save_data,
        }

        if choice == MENU_OPTIONS:
            return False

        action = menu_actions.get(choice)
        if action:
            action()

        return True

    def _add_exercise(self) -> None:
        """Végigvezet egy új gyakorlat felvételén: típus, név, dátum, részletek."""
        print("\n  --- Új gyakorlat rögzítése ---")

        exercise_type = self._choose_exercise_type()

        name = ""
        while not name:
            name = input("  Gyakorlat neve: ").strip()
            if not name:
                print("  A név nem lehet üres!")

        exercise_date = self._ask_date()

        if exercise_type == ExerciseType.CARDIO:
            exercise = self._create_cardio_exercise(name, exercise_date)
        else:
            exercise = self._create_strength_exercise(name, exercise_date)

        self._workout_log.add_exercise(exercise)
        self._save_data()

        print("\n  Gyakorlat sikeresen rögzítve!")
        print(f"  {exercise}")

    def _choose_exercise_type(self) -> ExerciseType:
        """Gyakorlat típusának kiválasztása (kardió/erőnléti)."""
        print("  Gyakorlat típusa:")
        print("    1. Kardió (pl. futás, kerékpározás, úszás)")
        print("    2. Erőnléti (pl. fekvenyomás, guggolás)")

        choice = get_valid_input(
            "  Válasszon (1-2): ",
            lambda x: validate_menu_choice(x, 2),
            "Kérem 1 vagy 2 számot!",
        )

        return (
            ExerciseType.CARDIO if choice == 1
            else ExerciseType.STRENGTH
        )

    def _ask_date(self) -> date:
        """Dátum bekérése. Üres Enter = mai nap."""
        while True:
            date_input = input(
                "  Dátum (ÉÉÉÉ-HH-NN) [Enter = mai nap]: "
            ).strip()

            if date_input == "":
                today = date.today()
                print(f"  -> Mai dátum használata: {today}")
                return today

            result = validate_date(date_input)
            if result is not None:
                return result

            print("  Érvénytelen dátum! Használja: ÉÉÉÉ-HH-NN")

    def _create_cardio_exercise(
        self, name: str, exercise_date: date
    ) -> CardioExercise:
        """Bekéri az időtartamot és létrehozza a kardió gyakorlatot."""
        duration = get_valid_input(
            "  Időtartam (perc): ",
            validate_positive_integer,
            "Kérem pozitív egész számot!",
        )

        return CardioExercise(
            name=name,
            exercise_date=exercise_date,
            duration_minutes=duration,
        )

    def _create_strength_exercise(
        self, name: str, exercise_date: date
    ) -> StrengthExercise:
        """Bekéri a sorozat/ismétlés/súly adatokat és létrehozza a gyakorlatot."""
        sets = get_valid_input(
            "  Sorozatok száma: ",
            validate_positive_integer,
            "Kérem pozitív egész számot!",
        )
        reps = get_valid_input(
            "  Ismétlések száma: ",
            validate_positive_integer,
            "Kérem pozitív egész számot!",
        )
        weight = get_valid_input(
            "  Súly (kg): ",
            validate_positive_float,
            "Kérem pozitív számot!",
        )

        return StrengthExercise(
            name=name,
            exercise_date=exercise_date,
            sets=sets,
            reps=reps,
            weight_kg=weight,
        )

    def _list_exercises(self) -> None:
        """Az összes gyakorlat listázása vagy összesítése konkrét név szerint."""
        print("\n  --- Gyakorlatok listázása ---")

        if self._workout_log.exercise_count == 0:
            print("  Nincs rögzített gyakorlat.")
            return

        print("  Lista módja:")
        print("    1. Minden gyakorlat külön sorban")
        print("    2. Összesítés gyakorlatnév szerint")

        choice = get_valid_input(
            "  Válasszon (1-2): ",
            lambda x: validate_menu_choice(x, 2),
            "Kérem 1 vagy 2 számot!",
        )

        if choice == 1:
            exercises = self._workout_log.exercises
            self._display_exercise_table(exercises)
            print(f"  Összesen: {len(exercises)} gyakorlat")
            return

        self._display_name_summary()

    def _display_name_summary(self) -> None:
        """Összesítés konkrét gyakorlatnevek szerint."""
        stats = self._workout_log.get_exercise_name_statistics()

        if not stats:
            print("  Nincs rögzített gyakorlat.")
            return

        print(TABLE_SEPARATOR)
        print("    #  | Típus    | Gyakorlatnév         | Darab | Részletek")
        print(TABLE_SEPARATOR)
        for index, row in enumerate(stats, 1):
            print(
                f"  {index:>3}. | {row['type']:8s} | {row['name'][:20]:20s} | "
                f"{row['count']:>5} | {row['details']}"
            )
        print(TABLE_SEPARATOR)
        print(f"  Különböző gyakorlatnevek: {len(stats)}")

    def _filter_exercises(self) -> None:
        """Gyakorlatok szűrése dátum, típus, név vagy dátum tartomány szerint."""
        print("\n  --- Gyakorlatok szűrése ---")

        if self._workout_log.exercise_count == 0:
            print("  Nincs rögzített gyakorlat.")
            return

        print("  Szűrés módja:")
        print("    1. Dátum szerint")
        print("    2. Típus szerint")
        print("    3. Dátum tartomány szerint")
        print("    4. Konkrét gyakorlatnév szerint")

        choice = get_valid_input(
            "  Válasszon (1-4): ",
            lambda x: validate_menu_choice(x, 4),
            "Kérem 1, 2, 3 vagy 4 számot!",
        )

        if choice == 1:
            self._filter_by_date()
        elif choice == 2:
            self._filter_by_type()
        elif choice == 3:
            self._filter_by_date_range()
        else:
            self._filter_by_name()

    def _filter_by_date(self) -> None:
        """Gyakorlatok szűrése adott dátumra."""
        target_date = self._ask_date()
        results = self._workout_log.get_exercises_by_date(target_date)

        if not results:
            print(f"  Nincs gyakorlat ezen a napon: {target_date}")
            return

        self._display_exercise_table(results, "Szűrt eredmények")
        print(f"  Találatok: {len(results)} gyakorlat")

    def _filter_by_type(self) -> None:
        """Gyakorlatok szűrése típus szerint."""
        exercise_type = self._choose_exercise_type()
        results = self._workout_log.get_exercises_by_type(exercise_type)

        if not results:
            print(
                f"  Nincs {exercise_type.value} típusú gyakorlat."
            )
            return

        self._display_exercise_table(results, "Szűrt eredmények")
        print(f"  Találatok: {len(results)} gyakorlat")

    def _filter_by_name(self) -> None:
        """Gyakorlatok szűrése konkrét név vagy névrészlet alapján."""
        names = self._workout_log.get_available_exercise_names()
        if names:
            print("  Eddig rögzített gyakorlatnevek:")
            print(f"    {', '.join(names)}")

        search_term = ""
        while not search_term:
            search_term = input(
                "  Keresett gyakorlatnév vagy névrészlet: "
            ).strip()
            if not search_term:
                print("  A keresés nem lehet üres!")

        results = self._workout_log.get_exercises_by_name(search_term)

        if not results:
            print(f"  Nincs találat erre: {search_term}")
            return

        self._display_exercise_table(results, "Szűrt eredmények")
        print(f"  Találatok: {len(results)} gyakorlat")

    def _filter_by_date_range(self) -> None:
        """Gyakorlatok szűrése dátum tartomány szerint."""
        print("  Kezdő dátum:")
        start_date = get_valid_input(
            "    Dátum (ÉÉÉÉ-HH-NN): ",
            validate_date,
            "Érvénytelen dátum! Használja: ÉÉÉÉ-HH-NN",
        )
        print("  Záró dátum:")
        end_date = get_valid_input(
            "    Dátum (ÉÉÉÉ-HH-NN): ",
            validate_date,
            "Érvénytelen dátum! Használja: ÉÉÉÉ-HH-NN",
        )

        if start_date > end_date:
            print("  A kezdő dátum nem lehet későbbi, mint a záró dátum!")
            return

        results = self._workout_log.get_exercises_by_date_range(
            start_date, end_date
        )

        if not results:
            print(
                f"  Nincs gyakorlat ebben az időszakban: "
                f"{start_date} - {end_date}"
            )
            return

        self._display_exercise_table(results, "Szűrt eredmények")
        print(f"  Találatok: {len(results)} gyakorlat")

    def _show_statistics(self) -> None:
        """Statisztikák megjelenítése az edzésnaplóról."""
        print("\n  --- Statisztikák ---")

        if self._workout_log.exercise_count == 0:
            print("  Nincs rögzített gyakorlat.")
            return

        stats = self._workout_log.get_statistics()

        print(MENU_SEPARATOR)
        print(f"  Összes gyakorlat:            {stats['total_count']}")
        print(f"  Különböző gyakorlatnevek:    {stats['unique_name_count']}")
        print(
            f"  Leggyakoribb gyakorlat:      {stats['most_common_name']} "
            f"({stats['most_common_name_count']} db)"
        )
        print()
        print(f"  Kardió gyakorlatok:          {stats['cardio_count']}")
        if stats["cardio_count"] > 0:
            print(
                f"    Összes időtartam:          {stats['total_cardio_minutes']} perc"
            )
            print(
                f"    Átlagos időtartam:         {stats['avg_cardio_minutes']} perc"
            )
        print()
        print(f"  Erőnléti gyakorlatok:         {stats['strength_count']}")
        if stats["strength_count"] > 0:
            print(
                f"    Összes sorozat:            {stats['total_strength_sets']}"
            )
            print(
                f"    Átlagos súly:              {stats['avg_strength_weight']} kg"
            )
            print(
                f"    Átlagos ismétlésszám/sorozat:      {stats['avg_strength_reps']}"
            )
        print(MENU_SEPARATOR)

        print("  Gyakorlatnév szerinti statisztika:")
        self._display_name_summary()

    def _delete_exercise(self) -> None:
        """Gyakorlat törlése - kiválasztás sorszámmal, utána megerősítés."""
        print("\n  --- Gyakorlat törlése ---")

        exercises = self._workout_log.exercises
        if not exercises:
            print("  Nincs rögzített gyakorlat.")
            return

        self._display_exercise_table(exercises)

        max_index = len(exercises)
        print("  (0 = mégsem)")
        choice_str = input(
            f"  Törlendő gyakorlat sorszáma (1-{max_index}): "
        ).strip()

        try:
            choice = int(choice_str)
        except ValueError:
            print("  Érvénytelen sorszám!")
            return

        if choice == 0:
            print("  Törlés megszakítva.")
            return

        if choice < 1 or choice > max_index:
            print(
                f"  Érvénytelen sorszám! "
                f"Kérem 1-{max_index} közötti számot."
            )
            return

        exercise_to_delete = exercises[choice - 1]
        confirm = input(
            f"  Biztosan törli? {exercise_to_delete} (i/n): "
        ).strip().lower()

        if confirm == "i":
            try:
                self._workout_log.remove_exercise(choice - 1)
                self._save_data()
                print("  Gyakorlat sikeresen törölve!")
            except IndexError as e:
                print(f"  Hiba: {e}")
        else:
            print("  Törlés megszakítva.")

    def _export_csv(self) -> None:
        """Gyakorlatok exportálása CSV fájlba."""
        print("\n  --- Exportálás CSV-be ---")

        exercises = self._workout_log.exercises
        if not exercises:
            print("  Nincs rögzített gyakorlat az exportáláshoz.")
            return

        success = export_to_csv(exercises)
        if success:
            print("  Adatok sikeresen exportálva: data/workouts_export.csv")
        else:
            print("  Hiba történt az exportálás során!")

    def _save_data(self) -> None:
        """Adatok mentése JSON fájlba."""
        data = self._workout_log.to_dict_list()
        success = save_to_file(data)

        if success:
            logger.info("Adatok mentve.")
        else:
            print("  Hiba történt a mentés során!")
            logger.error("Mentés sikertelen.")

    def _load_data(self) -> None:
        """Adatok betöltése JSON fájlból indításkor."""
        data = load_from_file()
        self._workout_log.load_from_dict_list(data)

        count = self._workout_log.exercise_count
        if count > 0:
            print(f"  {count} gyakorlat betöltve a korábbi mentésből.")

    def _ask_save_on_exit(self) -> None:
        """Mentés felajánlása kilépéskor."""
        if self._workout_log.exercise_count == 0:
            return

        confirm = input(
            "\n  Menti a változásokat kilépés előtt? (i/n): "
        ).strip().lower()

        if confirm == "i":
            self._save_data()
            print("  Adatok sikeresen mentve!")

    @staticmethod
    def _display_exercise_table(
        exercises: list[Exercise], title: str = "Gyakorlatok"
    ) -> None:
        """Táblázat kirajzolása - ezt használjuk listázásnál, szűrésnél, törlésnél is."""
        print(f"  {title}:")
        print(TABLE_SEPARATOR)
        print(
            f"    #  | Dátum       | Típus    | "
            f"Név                  | Részletek"
        )
        print(TABLE_SEPARATOR)

        for i, exercise in enumerate(exercises, 1):
            print(exercise.format_row(i))

        print(TABLE_SEPARATOR)
