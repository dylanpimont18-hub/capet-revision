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

# ── Nettoyage des coquilles d'extraction ─────────────────────────────────
# Les pages administratives (convocation, émargement, consignes, cadre
# « Ne rien écrire ») sont lues en désordre par l'extraction : elles ne
# contiennent pas de sujet et produisent des fragments illisibles. On retire
# les blocs qui les portent. Marqueurs tolérants aux espaces parasites.
ADMIN_I = re.compile(
    r"c\s?o\s?n\s?v\s?o\s?c\s?a\s?t\s?i\s?o\s?n|é\s?m\s?a\s?r\s?g\s?e\s?m|ne rien [eé]crire|"
    r"mod[eè]le\s+cmen|cadre\s+r[ée]serv|remplir\s+soign|n°\s*d.\s*inscription|"
    r"num[ée]ro\s*(<br>)?\s*candidat|nom de famille|n[ée]\(e\)\s*le|ne pas signer|"
    r"section/option|codes nécessaires|cocher une seule case|"
    r"encre\s+(bleue|noire)|stylo\s+plume", re.I)
ADMIN_S = re.compile(r"CONSIGNES|INFORMATION AUX CANDIDATS|NE RIEN ECRIRE|EDE STI \d")

def retirer_administratif(texte):
    blocs = re.split(r"\n\s*\n", texte)
    gardes = [b for b in blocs if not (ADMIN_I.search(b) or ADMIN_S.search(b))]
    return "\n\n".join(gardes), len(blocs) - len(gardes)

# Coquilles relevées une à une à la relecture (texte d'origine ou extraction).
CORRECTIONS = {
    "DSICIPLINAIRE": "DISCIPLINAIRE",
    "cidessous": "ci-dessous", "Cidessous": "Ci-dessous",
    "séguence": "séquence", "séauence": "séquence",
    "éve olutif": "évolutif",
}
# Corrections qui exigent des limites de mot.
CORRECTIONS_MOTS = [(r"\bctets\b", "octets"), (r"\biejuninq\b ?", "")]
# Commandes LaTeX restées hors des formules : on affiche le symbole.
HORS_MATHS = [(r"\\theta\b", "θ"), (r"\\times\b", "×"), (r"\\overrightarrow\{([^}]*)\}", "\\1\u20d7")]

try:
    from spellchecker import SpellChecker
    _DICO = SpellChecker(language="fr")
except Exception:          # sans dictionnaire, pas de recollage
    _DICO = None

def _connu(m):
    return _DICO is not None and m.lower() in _DICO

SUFFIXES = {"ques", "tion", "tions", "sion", "sions", "ment", "ments", "ble", "bles",
            "tique", "tiques", "trique", "triques", "teur", "teurs", "rice", "rices", "lité", "lités"}

def _fusionnable(a, b):
    if not (re.fullmatch(r"[A-Za-zÀ-ÿœ]{1,20}", a) and re.fullmatch(r"[a-zà-ÿœ]{2,12}", b)):
        return False
    if a[0].isupper() and len(a) <= 3:          # sigles et variables : TOR, CA, N, V…
        return False
    mot = (a + b).lower()
    if mot not in _DICO:
        return False
    freq = _DICO.word_frequency
    if len(a) == 1:                              # « c ontrôle » oui, « m et » non
        return not _connu(b)
    if not (_connu(a) and _connu(b)):            # « thermi ques », « vérifi cation »
        return True
    # Deux mots connus : seulement une fin de mot détachée dont le début, seul,
    # est plus rare que le mot entier (jamais « quel que », « par le »).
    return b.lower() in SUFFIXES and freq[a.lower()] < freq[mot]

def recoller(fragment):
    """Recolle les mots coupés par l'extraction (« thermi ques »), en
    examinant chaque paire de mots voisins, sans en sauter aucune. Texte
    seul, jamais les balises ni les formules."""
    if _DICO is None:
        return fragment
    parts = re.split(r"( +)", fragment)
    i = 0
    while i + 2 < len(parts):
        if parts[i + 1] == " " and _fusionnable(parts[i], parts[i + 2]):
            parts[i:i + 3] = [parts[i] + parts[i + 2]]   # le mot recollé peut se recoller encore
        else:
            i += 2
    return "".join(parts)

def recoller_html(corps):
    morceaux = re.split(r"(<[^>]+>|\$\$.+?\$\$|\$[^$\n]+?\$)", corps, flags=re.S)
    return "".join(m if (m.startswith("<") or m.startswith("$")) else recoller(m) for m in morceaux)

def proteger_maths(texte):
    morceaux = []
    def garder(m):
        if re.fullmatch(r"\$+[\s\\{}]*\$+", m.group(0)):
            return ""                         # formule vide, résidu d'extraction
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
    texte = re.sub(r"^\s*```[A-Za-z]*\s*$", "", texte, flags=re.M)     # blocs de code parasites
    texte, retires = retirer_administratif(texte)
    for faux, juste in CORRECTIONS.items():
        texte = texte.replace(faux, juste)
    for motif, juste in CORRECTIONS_MOTS:
        texte = re.sub(motif, juste, texte)
    texte = texte.replace("\\$", "DOLLARLITX")                        # $ littéral échappé
    titre = titre_de(ident, nom_dossier)
    texte, morceaux = proteger_maths(texte)
    texte = re.sub(r"\\n(?=[A-Za-zÀ-ÿ0-9(])", " ", texte)             # « \n » littéral
    for motif, rempl in HORS_MATHS:
        texte = re.sub(motif, rempl, texte)

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
    corps = recoller_html(corps)
    corps = corps.replace("DOLLARLITX", '<span class="lit">$</span>')
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
        "figuresManquantes": len(manquantes), "blocsAdministratifsRetires": retires, "sommaire": toc,
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
