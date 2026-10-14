#!/usr/bin/env python3
"""Index du cours : lit le plan de cours/PROGRES.md et les fragments
cours/textes/TXX.html, écrit cours/index.json et sw-cours.js.

    python3 scripts/indexer_cours.py

Le plan (ordre, titre, prérequis, statut) vient du tableau de PROGRES.md ;
le sommaire (titres h2/h3 munis d'un id) et le nombre de schémas (figures
contenant un SVG) viennent des fragments. Un chapitre sans fragment reste
dans l'index avec "disponible": false : la liste du cours l'annonce, le
lecteur ne le propose pas en précédent/suivant.

Après l'avoir lancé, mettre à jour la version du cache :
    python3 scripts/version_cache.py
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
PROGRES = RACINE / "cours" / "PROGRES.md"
TEXTES = RACINE / "cours" / "textes"
INDEX = RACINE / "cours" / "index.json"
SW = RACINE / "sw-cours.js"

LIGNE_PLAN = re.compile(
    r"^\|\s*(\d+)\.\s*(.+?)\s*\|\s*(T\d\d)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|")
TITRE = re.compile(r"<h([23])\b[^>]*\bid=\"([^\"]+)\"[^>]*>(.*?)</h\1>", re.S)
FIGURE = re.compile(r"<figure\b[^>]*>.*?</figure>", re.S)


def texte_brut(fragment: str) -> str:
    """Texte d'un titre : balises retirées, entités décodées, espaces réduits."""
    sans = re.sub(r"<[^>]+>", "", fragment)
    return re.sub(r"\s+", " ", html.unescape(sans)).strip()


def lire_plan() -> list[dict]:
    plan = []
    for ligne in PROGRES.read_text(encoding="utf-8").splitlines():
        m = LIGNE_PLAN.match(ligne)
        if not m:
            continue
        ordre, titre, theme, prerequis, statut = m.groups()
        plan.append({
            "id": theme,
            "theme": theme,
            "ordre": int(ordre),
            "titre": titre,
            "prerequis": re.findall(r"T\d\d", prerequis),
            "statut": statut,
        })
    if not plan:
        raise SystemExit("Aucun chapitre trouvé dans le tableau de PROGRES.md")
    return sorted(plan, key=lambda c: c["ordre"])


def decrire(chapitre: dict) -> dict:
    chemin = TEXTES / f"{chapitre['theme']}.html"
    if not chemin.exists():
        return {**chapitre, "disponible": False, "sommaire": [], "schemas": 0}
    corps = chemin.read_text(encoding="utf-8")
    sommaire = [{"niveau": int(n), "texte": texte_brut(t), "id": i}
                for n, i, t in TITRE.findall(corps)]
    schemas = sum(1 for f in FIGURE.findall(corps) if "<svg" in f)
    return {**chapitre, "disponible": True, "sommaire": sommaire,
            "schemas": schemas}


def main() -> None:
    chapitres = [decrire(c) for c in lire_plan()]
    INDEX.write_text(json.dumps({"chapitres": chapitres}, ensure_ascii=False,
                                indent=1) + "\n", encoding="utf-8")
    fichiers = ["./cours/index.json"] + [
        f"./cours/textes/{c['theme']}.html" for c in chapitres if c["disponible"]]
    # SVG de cartes redessinés pour le cours (redirigés par
    # corrections/cartes.json) : build_cards.py ne les connaît pas, donc
    # sw-assets.js ne les précache pas.
    deja = set(re.findall(r'"(\./svg/[^"]+)"', (RACINE / "sw-assets.js").read_text(encoding="utf-8")))
    cartes = json.loads((RACINE / "cards.json").read_text(encoding="utf-8"))["cards"]
    fichiers += sorted({f"./{c['svg']}" for c in cartes if c.get("svg")} - deja)
    SW.write_text(
        "// Généré par scripts/indexer_cours.py — ne pas modifier à la main.\n"
        "self.ASSETS_COURS = " + json.dumps(fichiers, indent=1) + ";\n",
        encoding="utf-8")
    dispo = [c for c in chapitres if c["disponible"]]
    n = len(dispo)
    print(f"{len(chapitres)} chapitres au plan, {n} rédigé{'s' if n > 1 else ''}, "
          f"{sum(c['schemas'] for c in dispo)} schémas.")


if __name__ == "__main__":
    main()
