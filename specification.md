# Funkcionális Specifikáció: Edzésterv Napló

## 1. A program célja

A program egy parancssori edzésterv napló, amivel különböző típusú gyakorlatokat
lehet rögzíteni és nyomon követni. Kardió edzésekhez (pl. futás, kerékpár, úszás) az
időtartamot, súlyzós edzésekhez (pl. fekvenyomás, guggolás, felhúzás) a sorozatszámot,
ismétléseket és súlyt tartja nyilván. Az adatokat fájlban tárolja, így a korábban
rögzített edzések a program újraindítása után is elérhetőek maradnak.

A program nemcsak a két nagy kategóriát kezeli, hanem a gyakorlat nevét is külön
figyelembe veszi. Ezért a felhasználó később nemcsak azt tudja megnézni, hogy mennyi
kardió vagy súlyzós edzése volt, hanem például azt is, hogy hányszor futott, úszott,
guggolt vagy fekvenyomott.

## 2. Gyakorlat típusok

**Kardió**: Olyan gyakorlatok, ahol az időtartam a lényeg. Például futás 30 percig,
vagy kerékpározás 45 percig. Ezekhez a nevet, dátumot és az időtartamot kell
megadni percben.

**Súlyzós**: Olyan gyakorlatok, ahol a sorozatok, ismétlések és a súly számít.
Például fekvenyomás 3 sorozat, 10 ismétlés, 60 kg-mal. Ezeknél a nevet, dátumot,
sorozatszámot, ismétlésszámot és a súlyt kell rögzíteni.

## 3. Főbb funkciók listája

**Új gyakorlat rögzítése**: A felhasználó kiválasztja a típust (kardió vagy súlyzós),
megadja a gyakorlat nevét és dátumát, majd a típusnak megfelelő adatokat. A dátumnál
lehetőség van az aktuális nap automatikus használatára.

**Gyakorlatok listázása**: Az összes rögzített gyakorlat megtekinthető táblázatos
formában. Emellett elérhető egy összesített lista is, amely megmutatja a konkrét
feladatneveket, azok típusát, előfordulásuk számát és a hozzájuk tartozó egyszerű
összesítéseket.

**Gyakorlatok szűrése**: Lehetőség van szűrésre
- adott dátum szerint
- típus szerint (csak kardió vagy csak súlyzós)
- dátum tartomány alapján (mettől meddig)
- konkrét gyakorlatnév vagy névrészlet alapján (például "fut" vagy "gugg")

**Statisztikák megjelenítése**: A program összesített adatokat mutat az edzésekről.
Kardió esetén az összes és átlagos időtartamot, súlyzós esetén az összes sorozatszámot
és átlagos súlyt jeleníti meg. Ezen felül gyakorlatnév szerinti bontást is ad,
amelyből látszik, hogy melyik konkrét feladatból mennyi volt, és melyik fordult elő
leggyakrabban.

**Adatok mentése és betöltése**: Az edzésadatok JSON fájlban tárolódnak. A program
induláskor automatikusan betölti az előző munkamenetek adatait, és minden módosítás
után el is menti azokat. Ha a fájl nem létezik, üres naplóval indul.

**Gyakorlat törlése**: Lehetőség van egy korábban rögzített gyakorlat törlésére. A
program a törlés előtt megerősítést kér, nehogy véletlenül töröljünk valamit.

**Exportálás CSV fájlba**: Az adatok kimenthetők CSV formátumba, amit aztán
Excelben vagy más táblázatkezelőben meg lehet nyitni.

## 4. Felhasználói folyamat

1. A program indításakor betölti a korábban mentett edzésadatokat, ha vannak.
2. Megjelenik a főmenü, ahol számmal lehet választani a funkciók közül.
3. Új edzés rögzítésekor a felhasználó megadja a gyakorlat típusát, nevét, dátumát és a
   szükséges részleteket.
4. A felhasználó kérhet teljes listát, név szerinti összesítést, szűrést vagy statisztikát.
5. A kiválasztott funkció végrehajtása után a program visszatér a főmenübe.
6. Kilépéskor a program felajánlja a mentést, majd bezárul.
