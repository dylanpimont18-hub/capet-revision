# App de révision CAPET SII·IE

PWA hors-ligne d'entraînement au rappel actif : formules, schémas,
conditions d'application. Le contenu est **généré** depuis `fiches/` —
ne jamais l'éditer à la main dans `app/` (`cards.json`, `svg/`,
`sw-assets.js` sont écrasés à chaque régénération et ne sont pas
versionnés, voir plus bas).

État courant (2026-09-21) : 574 cartes — 344 formules (191 en tableau
Markdown, 153 en bloc `$$`), 199 pièges, 31 schémas — réparties sur 30
thèmes, poids de 0,231 à 1,3. 31 SVG compilés depuis les fiches LaTeX
(0 échec). KaTeX 0.16.9 vendored dans `app/vendor/katex/` (62 fichiers,
dont les 20 polices `.woff2` précachées par le service worker). 66
entrées dans le cache du service worker.

## Régénérer le contenu

```bash
python scripts/build_cards.py            # avec compilation des schémas (lent)
python scripts/build_cards.py --sans-svg # texte seul, itération rapide
```

Produit `app/cards.json` et `app/svg/*.svg`, plus `app/sw-assets.js`
(liste des fichiers à précacher : SVG + polices KaTeX). En mode
`--sans-svg`, une carte schéma dont le SVG n'existe pas encore est
omise plutôt que de pointer vers une image cassée.

## Lancer en local

Un seul serveur, lancé depuis la **racine du dépôt** (pas depuis `app/`) :

```bash
python -m http.server 8765 --directory .
```

- app : `http://localhost:8765/app/`
- harnais de test HTML : `http://localhost:8765/tests/*.html`

Un serveur est nécessaire : les modules ES et le service worker ne
fonctionnent pas en `file://`. Servir uniquement `app/` (`--directory
app`) sortirait les harnais de test de la racine servie — ne pas le
faire.

## Tests

```bash
python -m pytest tests/ -v   # 74 tests — parseurs Python (scripts/)
```

Plus 4 harnais de test HTML, à ouvrir dans le navigateur une fois le
serveur ci-dessus lancé :
`tests/test_scheduler.html`, `tests/test_store.html`,
`tests/test_card_render.html`, `tests/test_priorites.html`.

## Après avoir corrigé une fiche

Relancer `build_cards.py`. Les identifiants de carte sont
**positionnels** : `T19-f-003` = 3ᵉ formule de T19 dans l'ordre du
fichier. Insérer une formule **au milieu** d'une section décale tous
les ids suivants de ce thème et désaligne la progression déjà
enregistrée (la progression est indexée par id dans `localStorage`,
voir `app/js/store.js`). Ajouter en **fin** de section est sans effet.
En cas de doute, exporter la progression depuis l'écran Réglages avant
de régénérer une fiche en profondeur.

## Ce qui n'est pas extrait, volontairement

La section `## 3. ATTENTES DU JURY` des fiches n'est **pas** extraite,
et ne doit pas l'être. Un audit de véracité du 2026-09-20 a établi que
54 % des citations de jury des fiches étaient défectueuses, dont 27
sans aucun support textuel (fabriquées). Importer ces encadrés dans
l'outil de révision propagerait des citations inventées sous une
forme — la carte flash — qui invite justement à les mémoriser telles
quelles. Voir `CLAUDE.md` (racine) pour le détail de l'audit.

## Qualité pédagogique (audit du 2026-10-12)

Les corrections de contenu vivent dans `corrections/cartes.json`, indexées
par id, et s'appliquent avec `python3 corrections/appliquer.py` (idempotent).
**Après toute régénération de `cards.json`, relancer ce script**, puis
vérifier avec `--verifier` qu'aucun id n'a disparu.

Ce que l'audit a corrigé dans les 574 cartes :

- **Erreurs de fond** (une douzaine) : facteurs de puissance des redresseurs
  (PD2 0,90, P3 0,675, PD6 0,955 ; la formule « générale en $q$ » était
  fausse), THD théorique du pont triphasé (0,31, pas 0,48), ondulation de
  courant du Boost ($\alpha E/Lf$), couple MAS linéarisé (manquait un
  $\omega_s$), tension moyenne du P1 commandé ($/2\pi$), pertes fer et
  réactif à vide écrits en $I_0^2$ (faux dans le modèle parallèle), convention
  de la loi d'Ohm généralisée, application numérique de compensation
  (2,2 mF, pas 0,016 F), autonomie batterie (DoD$_{max}$), étiquette
  « P3 » sur une formule de PD6, filtre anti-repliement ($\le f_e/2$).
- **Unités** : 249 formules en étaient dépourvues ; le jury les exige.
- **Conditions d'application** : rédigées pour les 70 formules les plus
  fréquentes (hypothèses, domaine de validité, pièges associés).
- **Pièges** : un champ `forme` distingue les 127 cartes qui citent une
  erreur réelle (recto « pourquoi est-ce faux ? ») des 72 dont l'énoncé est
  une règle juste (recto « quel est le piège ? », l'énoncé devient la
  réponse). Avant, les 199 cartes demandaient de réfuter l'énoncé, y compris
  quand il était vrai. Une trentaine d'énoncés tronqués ou vagues
  (« Erreur fréquente. », « Ne pas confondre. ») ont été réécrits.

Ce que l'application fait en plus depuis cet audit :

- **Entrelacement** : la file du jour alterne les thèmes au lieu de les
  enchaîner par blocs (`entrelacer()` dans `scheduler.js`).
- **Tracer de mémoire** : chaque schéma génère une seconde carte
  (`<id>-trace`, dérivée au chargement dans `app.js`) qui montre le nom au
  recto et le schéma au verso. Elle n'entre en rotation qu'après une
  réussite sur la carte de reconnaissance (champ `prerequis`).
- **Cartes difficiles** : l'état d'une carte compte désormais `vues` et
  `rates` (cumulés). À trois échecs, le verso renvoie à la fiche, l'écran
  Priorités compte ces cartes par thème et propose une session dédiée
  (`#/reviser?mode=difficiles`).
- **Liste de vérification** au verso des formules : « pour su, il fallait :
  la relation · les unités · les conditions », pour lutter contre
  l'auto-évaluation indulgente.

Non corrigé, à vérifier à la source : la limite « THD < 25 % » attribuée à la
CEI 61000-2-2 (T04-f-011, T04-p-002) vient des sujets, pas de la norme ; les
coefficients du PI numérique (T27-f-008) dépendent d'une paramétrisation de
sujet non vérifiable ici.

## Catégories

`js/categories.js` regroupe les trente thèmes en onze catégories réparties
dans quatre génies (électrique, énergétique et fluidique, mécanique,
informatique et automatique) et définit les types filtrables. L'écran
`#/categories` lance `#/reviser?genie=<code>`, `?cat=<code>`, `?theme=<Txx>`,
`?cat=toutes`, chacun combinable avec `&type=formule|piege|schema`.
La file d'une sélection (`fileFiltre` dans `scheduler.js`) prend d'abord les
cartes dues, puis les nouvelles, puis les autres par échéance croissante, et
entrelace les thèmes. Le type choisi est mémorisé dans `capet.prefs.v1`.

## Extraits d'épreuves (`exercices.json`)

Fichier rédigé à la main, jamais écrasé par `build_cards.py`, chargé par
`app.js` et fusionné dans les cartes avec le type `exercice`. Chaque entrée :
`id` (`X-<année>-<n>`), `theme`, `annee`, `epreuve`, `systeme`, `titre`,
`donnees[]`, `schema` (SVG inline, `currentColor` et `var(--accent)`),
`question`, `reponse` (paragraphes séparés par `\n`), `attendus[]`.

Les sujets officiels ne sont pas accessibles depuis l'environnement où ces
exercices ont été rédigés : ils s'inspirent des systèmes supports et des
thèmes relevés dans les cartes (SPA 2017, COMPACTO II 2018, variateur 2021,
frein à courant de Foucault 2022, comparateur et modulateur 2023, chaîne
4–20 mA et robot 2024, îlotage et hacheur 2025, bus CAN, pont triphasé,
filtre et anti-repliement 2026). Pour des extraits authentiques, déposer les
PDF des sujets (devenirenseignant.gouv.fr, page « sujets et rapports des
jurys » de chaque session) dans un dossier `sujets/` du dépôt de travail :
les énoncés pourront alors être repris textuellement et les figures
redessinées.

Les exercices sont exclus de la file du jour, de la révision libre et des
totaux de l'écran Priorités (`revisable()` dans `scheduler.js`), et du type
« Toutes » des catégories. Ils se lancent depuis `#/sujets` :
`#/reviser?sujet=<id>`, `#/reviser?annee=<année>`, `#/reviser?type=exercice`.

## Stockage local

Quatre clés `localStorage`, toutes lues et écrites par `app/js/store.js` :

| Clé | Contenu |
|---|---|
| `capet.progression.v1` | état SM-2 par id de carte (+ compteurs `vues`, `rates`) — le trésor |
| `capet.activite.v1` | compteurs su/hésité/raté par jour (série de jours consécutifs) |
| `capet.date_ecrit` | date de l'écrit, `AAAA-MM-JJ` (compte à rebours) |
| `capet.prefs.v1` | préférences d'interface (indice de geste déjà vu, etc.) |

L'export (version 2) emporte les trois premières ; l'import accepte aussi
les exports version 1 (progression seule). « Effacer toute la progression »
vide la progression et l'activité, pas la date ni les préférences.

## Installer sur iPhone

Safari → icône Partager → « Ajouter à l'écran d'accueil ».

Ce n'est pas cosmétique : l'ajout à l'écran d'accueil est ce qui
**protège la progression**. Safari purge les données (dont
`localStorage`) d'un site simplement visité au bout de 7 jours
d'inactivité (ITP), mais pas celles d'une PWA installée via « Ajouter
à l'écran d'accueil ». Sans cette installation, deux semaines sans
réviser suffisent à perdre la progression.

Même installée, il n'y a **aucun serveur** derrière cette app :
l'export JSON de l'écran Réglages reste la seule vraie sauvegarde. À
faire avant tout changement d'appareil, réinstallation, ou refonte de
fiche (voir section précédente).

## Contenu rédigé directement dans `app/` (2026-09-30)

Trois séries de corrections ont été faites **dans les artefacts**, pas dans
les fiches, et seront écrasées par une régénération tant qu'elles n'auront
pas été reportées dans `fiches/` et `scripts/build_cards.py` :

- `cards.json` : les 31 cartes schéma ont reçu un `label` explicite, une
  `question` propre au recto et une `reponse` rédigée au verso (au lieu de
  « Schéma T01 n°1 », qui ne permettait pas de s'auto-évaluer). Les 99
  pièges dont `regle` était vide ont reçu une règle rédigée.
- `svg/` : cinq schémas à blocs (`7508afcdb633`, `cccbe6d24856`,
  `43760a397071`, `1904c70b8dd8`, `1d2627c9e27a`) avaient été compilés sans
  glyphes (`<defs>` vide) et leurs cases étaient muettes. Les libellés ont
  été reconstitués en `<text>` SVG. À corriger à la source dans
  `build_svg.py` (police des nœuds `\text{}` non embarquée par dvisvgm).
- `svg/` : les couleurs codées en dur (`#1d4ed8`, `#839eea`) ont été remplacées
  par `var(--accent, …)` et `var(--ink-faible, …)` pour suivre la palette
  terre cuite ; `build_svg.py` doit émettre ces variables plutôt que des hexa.
- `icons/` : icônes régénérées en terre cuite (aplat `#b85634`, carte crème).
- `js/card-render.js` : les SVG sont injectés inline et non plus via `<img>`,
  pour que leurs couleurs suivent le thème de l'app (un SVG dans `<img>` ne
  voit que `prefers-color-scheme` du système). La `<style>` interne du SVG
  est retirée à l'injection ; `build_svg.py` peut cesser de l'émettre.

Avant toute régénération : exporter la progression, puis reporter ces
contenus (un script de fusion par `id` suffit pour `cards.json`).
