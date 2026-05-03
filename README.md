# Edzésterv Napló

GitHub repository:
https://github.com/nemethi03/training

Parancssori alkalmazás edzések nyilvántartásához. Kardió és erőnléti gyakorlatokat
lehet rögzíteni dátummal, majd visszanézni, szűrni és statisztikákat készíteni belőlük.
A program nemcsak nagy csoportok szerint dolgozik, hanem konkrét gyakorlatnevek
szerint is, például futás, úszás, guggolás vagy fekvenyomás.

## Telepítés

Python 3.12 vagy újabb verzió szükséges.

```
pip install -r requirements.txt
```

(A projekt csak beépített könyvtárakat használ, külső függőség nincs.)

## Futtatás

```
python main.py
```

Windows alatt használható ez is:

```
py main.py
```

## Funkciók

- **Új gyakorlat rögzítése** - kardió (időtartam percben) vagy erőnléti (sorozat/ismétlés/súly)
- **Listázás** - minden gyakorlat külön sorban vagy összesítve gyakorlatnév szerint
- **Szűrés** - dátum, típus, időszak vagy konkrét gyakorlatnév szerint
- **Statisztikák** - összesítés típusonként és gyakorlatnév szerint
- **Törlés** - edzés eltávolítása megerősítéssel
- **CSV export** - adatok kimentése táblázatkezelőhöz
- **Automatikus mentés** - az adatok JSON fájlban tárolódnak

## Mappaszerkezet

```
main.py              - belépési pont
models/
  exercise.py        - gyakorlat osztályok (alap gyakorlat osztály, kardió, erőnléti)
  workout_log.py     - edzésnapló kezelése, szűrés, statisztika
ui/
  console_ui.py      - menürendszer és képernyős megjelenítés
utils/
  file_handler.py    - fájl mentés/betöltés és CSV export
  validators.py      - bemenet ellenőrzés
data/
  workouts.json      - mentett adatok (futtatáskor jön létre)
```
