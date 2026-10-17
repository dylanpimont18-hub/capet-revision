#!/usr/bin/env python3
"""Applique corrections/cartes.json sur cards.json (idempotent).

Usage, depuis la racine de l'app :
    python3 corrections/appliquer.py            # applique
    python3 corrections/appliquer.py --verifier # liste ce qui changerait, sans écrire

Les corrections sont indexées par id de carte (clé « cartes ») ou par code de
thème (clé « themes ») : elles survivent à une régénération de
cards.json par build_cards.py tant que les ids restent stables. Un id absent
de cards.json est signalé et ignoré.
"""
import json, sys, pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent
CARTES = RACINE / "cards.json"
CORRECTIONS = RACINE / "corrections" / "cartes.json"

def main():
    verifier = "--verifier" in sys.argv
    data = json.loads(CARTES.read_text(encoding="utf-8"))
    tout = json.loads(CORRECTIONS.read_text(encoding="utf-8"))
    corr = tout["cartes"]
    par_id = {c["id"]: c for c in data["cards"]}
    # Les thèmes se corrigent comme les cartes, indexés par leur code (« T12 »).
    par_id.update({f"thème {t['code']}": t for t in data["themes"]})
    corr = {**{f"thème {k}": v for k, v in tout.get("themes", {}).items()}, **corr}
    modifiees, champs, absents = 0, 0, []
    for id, patch in corr.items():
        c = par_id.get(id)
        if c is None:
            absents.append(id)
            continue
        diff = {k: v for k, v in patch.items() if c.get(k) != v}
        if diff:
            modifiees += 1
            champs += len(diff)
            if verifier:
                print(f"{id}: {', '.join(diff)}")
            else:
                c.update(diff)
    if absents:
        print(f"ATTENTION : {len(absents)} id(s) introuvable(s) : {', '.join(absents)}", file=sys.stderr)
    if verifier:
        print(f"{modifiees} carte(s) à modifier, {champs} champ(s).")
        return
    if modifiees:
        CARTES.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{modifiees} carte(s) modifiée(s), {champs} champ(s).")

if __name__ == "__main__":
    main()
