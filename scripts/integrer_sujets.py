#!/usr/bin/env python3
"""Intègre les sujets d'épreuves CAPET SII dans l'app.

Usage :
    python3 scripts/integrer_sujets.py CHEMIN/VERS/01_Sujets

Produit, dans sujets/ :
    index.json            métadonnées de chaque épreuve (année, épreuve, titre, sommaire)
    textes/<id>.html      texte de l'épreuve, Markdown converti, formules protégées
    img/<id>/<fig>.jpg    figures redimensionnées (1100 px max) pour l'écran d'un téléphone

Les formules $…$ et $$…$$ sont rendues par KaTeX dans le navigateur ; elles
sont protégées ici pour que le Markdown ne touche pas aux _ et aux *.
Les figures absentes de l'extraction sont remplacées par une mention
explicite, jamais par une image cassée.
"""
import json, re, shutil, sys, html
from pathlib import Path
import markdown
from PIL import Image

RACINE = Path(__file__).resolve().parent.parent
SORTIE = RACINE / "sujets"
LARGEUR_MAX = 1100
MOTS_EXCLUS = ("CAPET", "SESSION", "ÉPREUVE", "EPREUVE", "INFORMATION", "DOCUMENT", "DR", "NE RIEN")

# Titres lisibles, établis d'après le nom de chaque dossier source (accents
# et apostrophes rétablis). Les sujets « Commune », sans titre fiable dans
# le texte extrait, sont nommés d'après le système étudié.
TITRES = {
    "2015-E1": "Shelter déployable", "2015-E2": "École de Kolbsheim",
    "2016-E1": "Maison active", "2016-E2": "Ligne de tramway",
    "2017-E1": "Métro MF2000", "2017-E2": "Spa de Sydney Premium",
    "2018-E1": "Catamaran solaire", "2018-E2": "Éclairage public",
    "2019-E1": "Transport urbain par câble", "2019-E2": "Transformation d'une rame de métro",
    "2020-E1": "Préparation de commandes Exotec", "2020-E2": "Dessalinisateur d'eau de mer",
    "2021-E1": "Extraction du nickel", "2021-E2": "STEP, transfert d'énergie",
    "2022-E1": "Réseau de chaleur urbain", "2022-E2": "Banc d'essai automobile",
    "2023-E1": "Traitement de l'air d'une serre semi-fermée", "2023-E2": "Traitement de l'air d'une serre",
    "2024-E1": "Sujet commun 2024 (dossier technique et copies)", "2024-E2": "Extracteur d'air Urbanloop",
    "2025-E1": "Système scénique vidéo et lumière",
    "2025-E2": "Électrification d'un site isolé à La Réunion",
}

def titre_de(ident, nom_dossier):
    if ident in TITRES:
        return TITRES[ident]
    nom = re.sub(r"^(Epreuve[12]_|\d{4}_Epreuve[12]_)", "", nom_dossier).replace("_", " ")
    return nom[:1].upper() + nom[1:]

def proteger_maths(texte):
    morceaux = []
    def garder(m):
        morceaux.append(m.group(0))
        return f"MATHSPH{len(morceaux)-1}X"
    texte = re.sub(r"\$\$.+?\$\$", garder, texte, flags=re.S)
    texte = re.sub(r"\$[^$\n]+?\$", garder, texte)
    return texte, morceaux

def restaurer_maths(html_txt, morceaux):
    for i, m in enumerate(morceaux):
        html_txt = html_txt.replace(f"MATHSPH{i}X", html.escape(m, quote=False))
    return html_txt

def figure(src_dir, sortie_img, nom):
    source = src_dir / nom
    if not source.exists():
        return None
    sortie_img.mkdir(parents=True, exist_ok=True)
    cible = sortie_img / (Path(nom).stem + ".jpg")
    im = Image.open(source).convert("RGB")
    im.thumbnail((LARGEUR_MAX, LARGEUR_MAX))
    im.save(cible, "JPEG", quality=82, optimize=True)
    return cible.name

def traiter(md_path, index):
    annee = int(re.search(r"(20\d\d|19\d\d)", str(md_path)).group(1))
    dossier = md_path.parent
    nom_dossier = dossier.name
    epreuve = "1" if "Epreuve1" in nom_dossier or re.search(r"Epreuve1|_Epreuve1", md_path.name) or "Commune" in nom_dossier else "2"
    ident = f"{annee}-E{epreuve}"
    texte = md_path.read_text(encoding="utf-8")
    texte = re.sub(r"\\_(\\_)+", "", texte)           # lignes de pointillés OCR
    texte = re.sub(r"\*\*NE RIEN ECRIRE DANS CE CADRE\*\*", "", texte)
    titre = titre_de(ident, nom_dossier)
    texte, morceaux = proteger_maths(texte)

    manquantes = []
    sortie_img = SORTIE / "img" / ident
    def remplacer_image(m):
        alt, src = m.group(1), m.group(2).strip()
        nom = Path(src).name
        cible = figure(dossier, sortie_img, nom)
        if cible is None:
            manquantes.append(nom)
            return f"\n\nMATHSPHFIGMANQ{html.escape(nom)}X\n\n"
        return f"\n\n![{alt}](sujets/img/{ident}/{cible})\n\n"
    texte = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", remplacer_image, texte)

    corps = markdown.markdown(texte, extensions=["tables", "sane_lists"])
    corps = restaurer_maths(corps, morceaux)
    corps = re.sub(r"<p>MATHSPHFIGMANQ(.+?)X</p>", r'<div class="figure-manquante">Figure non extraite du PDF : \1</div>', corps)
    corps = re.sub(r'<img alt="([^"]*)" src="([^"]+)" ?/?>', r'<img alt="\1" src="\2" loading="lazy" decoding="async">', corps)

    toc = []
    def ancre(m):
        n = len(toc) + 1
        niveau = int(m.group(1))
        texte_titre = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        if niveau <= 3 and len(texte_titre) > 2:
            toc.append({"niveau": niveau, "texte": texte_titre, "id": f"sec-{n}"})
            return f'<h{niveau} id="sec-{n}">{m.group(2)}</h{niveau}>'
        return m.group(0)
    corps = re.sub(r"<h([1-4])>(.*?)</h\1>", ancre, corps, flags=re.S)

    (SORTIE / "textes").mkdir(parents=True, exist_ok=True)
    (SORTIE / "textes" / f"{ident}.html").write_text(corps, encoding="utf-8")
    index.append({
        "id": ident, "annee": annee, "epreuve": int(epreuve),
        "libelle": f"Épreuve {epreuve}", "titre": titre,
        "source": str(md_path.relative_to(SOURCE)), "figures": len(list(sortie_img.glob("*.jpg"))) if sortie_img.exists() else 0,
        "figuresManquantes": len(manquantes), "sommaire": toc,
    })
    return ident, len(manquantes)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    SOURCE = Path(sys.argv[1]).resolve()
    if SORTIE.exists():
        shutil.rmtree(SORTIE)
    SORTIE.mkdir(parents=True)
    index = []
    for md in sorted(SOURCE.rglob("*.md")):
        ident, nm = traiter(md, index)
        print(f"{ident:10s} figures manquantes : {nm}")
    index.sort(key=lambda e: (-e["annee"], e["epreuve"]))
    (SORTIE / "index.json").write_text(json.dumps({"epreuves": index}, ensure_ascii=False, indent=1), encoding="utf-8")
    # Textes et index hors ligne ; les figures restent à la demande (poids).
    precache = ["./sujets/index.json"] + [f"./sujets/textes/{e['id']}.html" for e in index]
    (RACINE / "sw-sujets.js").write_text(
        "// Généré par scripts/integrer_sujets.py — ne pas modifier à la main.\n"
        "self.ASSETS_SUJETS = " + json.dumps(precache, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8")
    nfig = sum(e['figures'] for e in index)
    print(f"{len(index)} épreuves, {nfig} figures")
