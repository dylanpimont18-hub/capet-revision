#!/usr/bin/env python3
"""Typographie française des chapitres du cours (idempotent).

    python3 scripts/typo_cours.py cours/textes/T01.html [...]
    python3 scripts/typo_cours.py --verifier cours/textes/*.html

Dans le texte courant seulement (ni balises, ni SVG, ni code, ni formules
$…$ et $$…$$), remplace l'espace ordinaire par une espace fine insécable
(U+202F) :
  - avant ; : ! ? et à l'intérieur des guillemets « » ;
  - entre un nombre et son unité (7,2 kW, 5 %) ;
  - entre les tranches de trois chiffres (1 395).
Avec --verifier, ne modifie rien et sort en erreur s'il reste à faire.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

FINE = " "
PROTEGE = re.compile(
    r"(<svg\b[\s\S]*?</svg>|<code\b[\s\S]*?</code>|<[^>]+>"
    r"|\$\$[\s\S]*?\$\$|\$[^$\n]*?\$)")
UNITES = (
    "kWc|Wc|kWh|MWh|Wh|mAh|Ah|kVA|VA|kvar|var|MW|kW|mW|W|kV|mV|µV|nV|V|kA|mA|µA|nA|A|"
    "MJ|kJ|J|MΩ|kΩ|mΩ|µΩ|Ω|mF|µF|nF|F|mH|µH|H|MHz|kHz|Hz|ms|µs|s|min|h|"
    "tr/min|rad/s|rad|kN|N|dB|m³/h|m³|hPa|bar|mol|mS/cm|µS/cm|µm/m|GPa|km|cm|µm|mkg|mm²|mm|m²|m|kg|g|L|°C|%|M€|k€|€")
REGLES = [
    (re.compile(r" ([;:!?])"), FINE + r"\1"),
    (re.compile(r"« "), "«" + FINE),
    (re.compile(r" »"), FINE + "»"),
    (re.compile(r"(\d) (?=\d{3}(?!\d))"), r"\1" + FINE),
    (re.compile(r"(\d) (?=(?:" + UNITES + r")(?![\wÀ-ÿ]))"), r"\1" + FINE),
]


def corriger_texte(texte: str) -> str:
    for motif, remplacement in REGLES:
        texte = motif.sub(remplacement, texte)
    return texte


APRES_NOMBRE = re.compile(r"^ (?=(?:" + UNITES + r"|µF|µH|µs|µΩ)(?![\wÀ-ÿ]))")


def corriger(html: str) -> str:
    morceaux = PROTEGE.split(html)
    sortie = []
    for i, m in enumerate(morceaux):
        if not i % 2:
            m = corriger_texte(m)
            # « $… 224$ µF » : l'unité suit une formule qui finit par un nombre.
            if i and re.search(r"[\d}]\$$", morceaux[i - 1]):
                m = APRES_NOMBRE.sub(FINE, m)
        sortie.append(m)
    return "".join(sortie)


def main() -> None:
    verifier = "--verifier" in sys.argv
    fichiers = [Path(a) for a in sys.argv[1:] if a != "--verifier"]
    a_faire = 0
    for f in fichiers:
        avant = f.read_text(encoding="utf-8")
        apres = corriger(avant)
        if apres != avant:
            a_faire += 1
            if verifier:
                print(f"{f} : typographie à corriger")
            else:
                f.write_text(apres, encoding="utf-8")
                print(f"{f} : corrigé")
    sys.exit(1 if verifier and a_faire else 0)


if __name__ == "__main__":
    main()
