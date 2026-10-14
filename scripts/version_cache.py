#!/usr/bin/env python3
"""Recalcule CACHE_VERSION (sw-assets.js) d'après le contenu précaché.

    python3 scripts/version_cache.py            # écrit la nouvelle version
    python3 scripts/version_cache.py --verifier # code 1 si elle est périmée

Le service worker ne se réinstalle (et ne purge l'ancien cache) que si un
octet de sw.js ou d'un script qu'il importe change. La version est donc le
hash de tout ce qu'il précache : le SOCLE de sw.js, plus les listes
self.ASSETS, self.ASSETS_SUJETS et self.ASSETS_COURS. Un fichier modifié
change la version ; un fichier inchangé la laisse identique.

build_cards.py (hors de ce dépôt) réécrit sw-assets.js en entier : relancer
ce script après lui.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SW_ASSETS = RACINE / "sw-assets.js"
LISTES = [RACINE / "sw-assets.js", RACINE / "sw-sujets.js", RACINE / "sw-cours.js"]
VERSION = re.compile(r'self\.CACHE_VERSION\s*=\s*"([^"]*)";')


def chemins_precaches() -> list[str]:
    sw = (RACINE / "sw.js").read_text(encoding="utf-8")
    socle = re.search(r"const SOCLE = \[(.*?)\];", sw, re.S)
    if not socle:
        raise SystemExit("SOCLE introuvable dans sw.js")
    chemins = re.findall(r'"(\./[^"]*)"', socle.group(1))
    for liste in LISTES:
        if liste.exists():
            chemins += re.findall(r'"(\./[^"]+)"', liste.read_text(encoding="utf-8"))
    return sorted(set("./index.html" if c == "./" else c for c in chemins))


def calculer() -> str:
    h = hashlib.sha256()
    for chemin in chemins_precaches():
        fichier = RACINE / chemin[2:]
        h.update(chemin.encode())
        h.update(fichier.read_bytes() if fichier.exists() else b"<absent>")
    return h.hexdigest()[:12]


def main() -> None:
    texte = SW_ASSETS.read_text(encoding="utf-8")
    actuelle = VERSION.search(texte)
    nouvelle = calculer()
    if "--verifier" in sys.argv:
        ok = actuelle and actuelle.group(1) == nouvelle
        print("CACHE_VERSION à jour" if ok else
              f"CACHE_VERSION périmée : {actuelle.group(1) if actuelle else '—'} ≠ {nouvelle}")
        sys.exit(0 if ok else 1)
    if actuelle:
        texte = VERSION.sub(f'self.CACHE_VERSION = "{nouvelle}";', texte)
    else:
        texte = texte.rstrip("\n") + f'\nself.CACHE_VERSION = "{nouvelle}";\n'
    SW_ASSETS.write_text(texte, encoding="utf-8")
    print(f"CACHE_VERSION = {nouvelle}")


if __name__ == "__main__":
    main()
