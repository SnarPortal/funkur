# Legg funkur afturat í Funkuframsýningina
#
#   python -I legg-funkur-afturat.py "C:\leið\til\funkur-6b.zip"     (ella ein mappu við .html-fílum, ella eina einstaka .html-fílu)
#
# Skriptið
#   1. tekur .html-fílurnar úr zip-fíluni (ella mappuni) og avritar tær í funkur/ (navnið verður gjørt trygt),
#   2. lesur viðmerkingina ovast í fíluni, sum Funkusmiðjan setir inn:
#        <!-- Funka: Teljari · Gjørd av: Ána, 6b · Koda og vitlíki, Snar -->
#   3. leggur eina linju afturat í funkur.json við "vis": false.
#
# FUNKURNAR SÍGGJAST IKKI, FYRR ENN TÚ HEVUR KANNAÐ TÆR: lat framsýningina upp lokalt, hygg at hvørjari funku
# (eingi eftirnøvn, eingin persónlig upplýsing, eingin leinkja út, hon riggar), skriva eitt gott "heiti" og "lysing",
# og set "vis": true. Legg so funkur/ og funkur.json upp á GitHub.
import io
import json
import os
import re
import sys
import zipfile
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "funkur")
JSON = os.path.join(HERE, "funkur.json")
SLAG = {"teljari": "teljari", "tilvildarligur spurningur": "spurningur", "spurningur": "spurningur", "lítið kviss": "kviss", "kviss": "kviss"}


def slug(t):
    t = t.lower()
    for a, b in (("ð", "d"), ("ø", "o"), ("æ", "ae"), ("á", "a"), ("í", "i"), ("ó", "o"), ("ú", "u"), ("ý", "y")):
        t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-") or "funka"


def files_from(src):
    if os.path.isdir(src):
        for n in sorted(os.listdir(src)):
            if n.lower().endswith(".html"):
                with io.open(os.path.join(src, n), encoding="utf-8", errors="replace") as f:
                    yield n, f.read()
    elif src.lower().endswith(".zip"):
        with zipfile.ZipFile(src) as z:
            for n in sorted(z.namelist()):
                if n.lower().endswith(".html") and not n.startswith("__MACOSX"):
                    yield os.path.basename(n), z.read(n).decode("utf-8", errors="replace")
    elif src.lower().endswith(".html"):
        with io.open(src, encoding="utf-8", errors="replace") as f:
            yield os.path.basename(src), f.read()


def main():
    if len(sys.argv) < 2:
        print(__doc__ or "Brúk: python -I legg-funkur-afturat.py <zip|mappa|fila.html>")
        sys.exit(1)
    os.makedirs(OUT, exist_ok=True)
    with io.open(JSON, encoding="utf-8") as f:
        data = json.load(f)
    known = {d["fila"] for d in data}
    added = 0
    for name, code in files_from(sys.argv[1]):
        m = re.search(r"<!--\s*Funka:\s*(.*?)\s*·\s*Gjørd av:\s*(.*?)\s*·", code)
        funka, who = (m.group(1), m.group(2)) if m else ("Funka", "")
        fornavn, _, flokkur = who.partition(",")
        fornavn = fornavn.strip().split(" ")[0] if fornavn.strip() else ""
        fn = slug(os.path.splitext(name)[0]) + ".html"
        base, i = fn[:-5], 2
        while "funkur/" + fn in known:
            fn = "%s-%d.html" % (base, i)
            i += 1
        with io.open(os.path.join(OUT, fn), "w", encoding="utf-8") as f:
            f.write(code)
        entry = {"fila": "funkur/" + fn, "heiti": funka, "slag": SLAG.get(funka.lower(), "annad"), "gjord_av": fornavn,
                 "flokkur": flokkur.strip(), "skuli": "", "dato": date.today().isoformat(),
                 "lysing": "", "vis": False}
        data.append(entry)
        known.add(entry["fila"])
        added += 1
        print("+ %-40s %s, %s" % (entry["fila"], fornavn or "?", entry["flokkur"] or "?"))
    with io.open(JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("\n%d funkur lagdar afturat við \"vis\": false. Kanna tær, skriva heiti og lýsing, og set \"vis\": true." % added)


if __name__ == "__main__":
    main()
