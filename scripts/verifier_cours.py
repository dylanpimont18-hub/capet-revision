#!/usr/bin/env python3
"""Vérifications statiques d'un chapitre du cours.

    python3 scripts/verifier_cours.py T01 [T07 ...]
    python3 scripts/verifier_cours.py --tous

Contrôle, sans navigateur :
  - structure : les onze rubriques (ids tXX-bref … tXX-reviser), titres h2/h3
    munis d'un id unique, auto-test de 4 à 6 questions ;
  - cartes : chaque id cité existe dans cards.json, et chaque formule, piège
    et schéma du thème est cité au moins une fois ;
  - liens : ancres internes, épreuves (sujets/index.json), chapitres
    (plan de PROGRES.md) ;
  - schémas : role="img", aria-label, figcaption, viewBox de 360 de large au
    plus, ni image ni ressource externe, couleurs en currentColor ou var(--…) ;
  - tableaux : 3 colonnes au plus hors .table-scroll ;
  - formules : $…$ équilibrés, jamais coupés par un retour à la ligne ;
  - typographie (scripts/typo_cours.py) et orthographe (pyspellchecker, fr,
    plus le lexique cours/lexique.txt).
Sortie : code 1 au moindre défaut bloquant ; les mots inconnus du
correcteur sont listés pour relecture, sans bloquer.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "scripts"))
import typo_cours  # noqa: E402

RUBRIQUES = ["bref", "prerequis", "idee", "cours", "schemas", "formules",
             "methode", "pieges", "exemple", "autotest", "reviser"]
COULEUR_OK = re.compile(r"^(none|currentColor|var\(--[\w-]+(,[^)]*)?\))$")


def charger_json(chemin: str):
    return json.loads((RACINE / chemin).read_text(encoding="utf-8"))


def texte_visible(corps: str) -> str:
    """Texte lisible : sans balises ni formules, aria-label compris."""
    labels = " ".join(re.findall(r'aria-label="([^"]*)"', corps))
    sans_maths = re.sub(r"\$\$[\s\S]*?\$\$|\$[^$\n]*?\$", " ", corps)
    sans_balises = re.sub(r"<[^>]+>", " ", sans_maths)
    return html.unescape(sans_balises + " " + labels)


def verifier(theme: str) -> tuple[list[str], list[str]]:
    defauts, remarques = [], []
    chemin = RACINE / "cours" / "textes" / f"{theme}.html"
    if not chemin.exists():
        return [f"{chemin} introuvable"], []
    corps = chemin.read_text(encoding="utf-8")
    t = theme.lower()

    # ── Structure ────────────────────────────────────────────────────────
    ids = re.findall(r'\bid="([^"]+)"', corps)
    doublons = {i for i in ids if ids.count(i) > 1}
    if doublons:
        defauts.append(f"ids en double : {sorted(doublons)}")
    h2 = re.findall(r'<h2 id="([^"]+)"', corps)
    attendus = [f"{t}-{r}" for r in RUBRIQUES]
    if h2 != attendus:
        defauts.append(f"rubriques h2 : {h2} ≠ {attendus}")
    for niveau in ("h2", "h3"):
        for m in re.finditer(rf"<{niveau}(?![^>]*\bid=)[^>]*>", corps):
            defauts.append(f"<{niveau}> sans id : {m.group(0)}")
    autotest = re.search(r'<ol class="autotest">([\s\S]*?)</ol>\s*<h2', corps)
    n_q = len(re.findall(r"<details>", autotest.group(1))) if autotest else 0
    if not 4 <= n_q <= 6:
        defauts.append(f"auto-test : {n_q} questions (4 à 6 attendues)")

    # ── Cartes ───────────────────────────────────────────────────────────
    cartes = {c["id"]: c for c in charger_json("cards.json")["cards"]}
    cites = set(re.findall(r"#/reviser\?carte=([\w-]+)", corps))
    for c in sorted(cites - set(cartes)):
        defauts.append(f"carte citée inexistante : {c}")
    du_theme = {i for i, c in cartes.items() if c["theme"] == theme}
    manquantes = sorted(du_theme - cites)
    if manquantes:
        defauts.append(f"cartes du thème non citées : {manquantes}")
    for c in sorted(cites):
        if f">{c}</a>" not in corps:
            defauts.append(f"lien de carte sans son id en texte : {c}")

    # ── Liens ────────────────────────────────────────────────────────────
    for ancre in re.findall(r'href="#(?!/)([^"]+)"', corps):
        if ancre not in ids:
            defauts.append(f"ancre interne cassée : #{ancre}")
    epreuves = {e["id"] for e in charger_json("sujets/index.json")["epreuves"]}
    for e in re.findall(r"#/epreuve\?id=([\w-]+)", corps):
        if e not in epreuves:
            defauts.append(f"épreuve inexistante : {e}")
        if e == "2019-E2":
            defauts.append("2019-E2 citée (mauvais sujet dans l'app)")
    plan = set(re.findall(r"\|\s*(T\d\d)\s*\|",
                          (RACINE / "cours" / "PROGRES.md").read_text(encoding="utf-8")))
    for c in re.findall(r"#/cours\?theme=(T\d\d)", corps):
        if c not in plan:
            defauts.append(f"chapitre hors plan : {c}")
    for r in re.findall(r"#/reviser\?theme=(T\d\d)", corps):
        if r != theme:
            remarques.append(f"lien de révision vers un autre thème : {r}")

    # ── Schémas ──────────────────────────────────────────────────────────
    figures = re.findall(r'<figure class="schema" id="([^"]+)">([\s\S]*?)</figure>', corps)
    if len(figures) != corps.count("<figure"):
        defauts.append("figure sans class=\"schema\" ou sans id")
    for num, (fid, fig) in enumerate(figures, 1):
        svg = re.search(r"<svg\b([^>]*)>", fig)
        if not svg:
            defauts.append(f"{fid} : pas de SVG")
            continue
        attrs = svg.group(1)
        if 'role="img"' not in attrs:
            defauts.append(f"{fid} : role=\"img\" manquant")
        if not re.search(r'aria-label="[^"]{20,}"', attrs):
            defauts.append(f"{fid} : aria-label absent ou trop court")
        vb = re.search(r'viewBox="([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)"', attrs)
        if not vb or float(vb.group(3)) > 360:
            defauts.append(f"{fid} : viewBox absente ou plus large que 360")
        if "<figcaption>" not in fig:
            defauts.append(f"{fid} : figcaption manquante")
        elif f"<b>Figure {num}.</b>" not in fig:
            defauts.append(f"{fid} : la légende devrait commencer par « Figure {num}. »")
        if re.search(r"<image\b|<img\b|href=\"http|url\(", fig):
            defauts.append(f"{fid} : image ou ressource externe")
        for prop, val in re.findall(r'\b(stroke|fill)="([^"]*)"', fig):
            if not COULEUR_OK.match(val):
                defauts.append(f"{fid} : {prop}=\"{val}\" (couleur codée en dur)")
        for taille in re.findall(r'font-size="([\d.]+)"', fig):
            if float(taille) < 13:
                defauts.append(f"{fid} : font-size {taille} < 13 (rendu < 12 px)")

    # ── Tableaux ─────────────────────────────────────────────────────────
    for m in re.finditer(r"<table>([\s\S]*?)</table>", corps):
        avant = corps[:m.start()]
        dans_cadre = avant.rfind('<div class="table-scroll">') > avant.rfind("</div>")
        lignes = re.findall(r"<tr>([\s\S]*?)</tr>", m.group(1))
        cols = max(len(re.findall(r"<t[hd]\b", l)) for l in lignes) if lignes else 0
        if cols > 3 and not dans_cadre:
            defauts.append(f"tableau de {cols} colonnes hors .table-scroll")

    # ── Formules ─────────────────────────────────────────────────────────
    sans_svg = re.sub(r"<svg\b[\s\S]*?</svg>", "", corps)
    sans_bloc = re.sub(r"\$\$[\s\S]*?\$\$", "", sans_svg)
    for n, ligne in enumerate(sans_bloc.splitlines(), 1):
        if ligne.count("$") % 2:
            defauts.append(f"$ déséquilibré (ligne {n} hors blocs) : {ligne.strip()[:70]}")

    # ── Typographie et orthographe ───────────────────────────────────────
    if typo_cours.corriger(corps) != corps:
        defauts.append("typographie : lancer python3 scripts/typo_cours.py")
    try:
        from spellchecker import SpellChecker
    except ImportError:
        remarques.append("pyspellchecker absent : orthographe non vérifiée")
    else:
        correcteur = SpellChecker(language="fr")
        lexique = RACINE / "cours" / "lexique.txt"
        if lexique.exists():
            correcteur.word_frequency.load_words(
                [l.strip().lower() for l in lexique.read_text(encoding="utf-8").splitlines()
                 if l.strip() and not l.startswith("#")])
        mots = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿœŒ]+(?:-[A-Za-zÀ-ÖØ-öø-ÿœŒ]+)*",
                          texte_visible(corps))
        candidats = set()
        for mot in mots:
            for partie in mot.split("-"):
                p = partie.lower().replace("œ", "oe")
                if len(p) > 2 and not partie.isupper() and not re.search(r"[A-Z]", partie[1:]):
                    candidats.add(p)
        inconnus = sorted(correcteur.unknown(candidats))
        if inconnus:
            remarques.append(f"mots inconnus du correcteur ({len(inconnus)}) : {', '.join(inconnus)}")
    return defauts, remarques


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--tous" in sys.argv:
        args = [c["theme"] for c in charger_json("cours/index.json")["chapitres"] if c["disponible"]]
    if not args:
        raise SystemExit(__doc__)
    total = 0
    for theme in args:
        defauts, remarques = verifier(theme)
        total += len(defauts)
        print(f"── {theme} : {len(defauts)} défaut(s)")
        for d in defauts:
            print(f"  ✗ {d}")
        for r in remarques:
            print(f"  · {r}")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
