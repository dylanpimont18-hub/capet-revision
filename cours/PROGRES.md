# Cours CAPET SII·IE — suivi de rédaction

Un chapitre par thème, rédigé puis passé à la boucle qualité. Une itération
traite **un seul** chapitre : le premier au statut « à faire » du tableau
ci-dessous, dans l'ordre du tableau. Statuts possibles : « à faire »,
« en cours », « validé », « à reprendre ».

Périmètre : génie électrique (T01–T04, T06–T09, T11–T15, T17–T20, T22, T23,
T30) et génie informatique et automatique (T21, T24–T29), soit 27 chapitres.
Hors périmètre : T05 (thermique), T10 (mécanique), T16 (renouvelables).

## Plan

L'ordre va du fondamental vers l'appliqué ; chaque chapitre ne suppose que
les chapitres placés avant lui (colonne « prérequis »). C'est aussi l'ordre de
lecture proposé dans l'app (chapitre précédent / suivant).

Colonne « notes » : fréquence tirée de `cards.json` (« N/13 » = tombe dans N
sujets sur 13, à citer telle quelle dans « En bref ») · relevé des 22 épreuves
de l'app (nombre d'épreuves et de questions qui mobilisent le thème, en
principal ou en secondaire, voir `cours/releve-sujets.json`) · cartes du thème
(F formules, P pièges, S schémas), toutes à couvrir · extraits rédigés de
`exercices.json` sur ce thème (ce ne sont **pas** des sujets officiels : ils
peuvent inspirer l'exemple chiffré, jamais être cités comme épreuve).

| chapitre | thème | prérequis | statut | tours | notes | défauts restants |
|---|---|---|---|---|---|---|
| 1. Électrocinétique et grandeurs fondamentales | T01 | — | à reprendre | 5 | 13/13 · relevé : 17 ép., 78 q. · 20 F, 6 P, 2 S · 23 schémas · cartes corrigées (corrections/cartes.json) : T01-p-004 (loi des nœuds aux entrées de l'ALI, pas à la sortie), T01-p-002 (S² = P² + Q²), T01-f-009 (φ = retard de i sur u), SVG de T01-s-001 et T01-s-002 redessinés (svg/T01-s-00N.svg) · notes des tours 1 à 5 en exactitude : 2, 4, 4, 4, 4 ; tour 5 : couverture, progression et lisibilité 5/5, schémas et langue 4/5 | Les défauts du tour 5 (1 majeur : sinus redressé sans « double alternance » dans la règle de p-003 ; 10 mineurs : sources commandées, hacheur série, glissement en moteur, R_ch, courants continus en majuscules, schémas de Millman et de J) sont corrigés mais n'ont pas été relus : faire un tour de relecture de confirmation en passe finale (exactitude à confirmer à 5/5). |
| 2. Représentation complexe et impédances | T03 | T01 | à faire | 0 | 12/13 · relevé : 3 ép., 4 q. · 19 F, 6 P, 1 S | — |
| 3. Puissances en régime sinusoïdal, monophasé et triphasé | T02 | T01, T03 | à faire | 0 | 13/13 · relevé : 8 ép., 26 q. · 35 F, 8 P, 1 S · extraits : X-2017-01, X-2017-02 | — |
| 4. Harmoniques, THD et puissance déformante | T04 | T02, T03 | à faire | 0 | 9/13 · relevé : 5 ép., 12 q. · 15 F, 6 P, 1 S · extraits : X-2018-01 | — |
| 5. Transformateur monophasé et triphasé | T06 | T02, T03 | à faire | 0 | 13/13 · relevé : 0 ép., 0 q. · 14 F, 6 P, 1 S · extraits : X-2020-02 | — |
| 6. Composants : diode, transistors, thyristor | T18 | T01 | à faire | 0 | 4/13 · relevé : 2 ép., 2 q. · 7 F, 7 P, 1 S | — |
| 7. Hacheurs | T07 | T01, T18 | à faire | 0 | 12/13 · relevé : 5 ép., 34 q. · 13 F, 6 P, 1 S · extraits : X-2025-02 | — |
| 8. Redresseurs | T08 | T02, T04, T06, T18 | à faire | 0 | 13/13 · relevé : 3 ép., 6 q. · 12 F, 6 P, 1 S · extraits : X-2026-02, X-2022-01 | — |
| 9. Onduleurs et MLI | T09 | T04, T07 | à faire | 0 | 12/13 · relevé : 5 ép., 11 q. · 13 F, 7 P, 1 S · extraits : X-2025-01 | — |
| 10. Filtres du 1er et du 2e ordre | T20 | T03 | à faire | 0 | 5/13 · relevé : 0 ép., 0 q. · 12 F, 7 P, 1 S · extraits : X-2026-03 | — |
| 11. Amplificateur opérationnel | T19 | T01, T20 | à faire | 0 | 4/13 · relevé : 3 ép., 16 q. · 12 F, 7 P, 1 S · extraits : X-2023-01 | — |
| 12. Modélisation des systèmes linéaires | T26 | T01, T20 | à faire | 0 | 9/13 · relevé : 8 ép., 29 q. · 10 F, 7 P, 1 S | — |
| 13. Fonctions de transfert et diagramme de Bode | T21 | T20, T26 | à faire | 0 | 8/13 · relevé : 2 ép., 5 q. · 13 F, 8 P, 1 S · extraits : X-2023-02 | — |
| 14. Systèmes bouclés, correcteurs, stabilité | T27 | T21, T26 | à faire | 0 | 9/13 · relevé : 9 ép., 31 q. · 9 F, 7 P, 1 S | — |
| 15. Machine à courant continu | T11 | T07, T26 | à faire | 0 | 10/13 · relevé : 1 ép., 2 q. · 15 F, 6 P, 1 S | — |
| 16. Machine asynchrone | T13 | T02, T06, T26 | à faire | 0 | 7/13 · relevé : 8 ép., 37 q. · 17 F, 7 P, 1 S · extraits : X-2019-01 | — |
| 17. Machine synchrone et brushless | T12 | T09, T13 | à faire | 0 | 4/13 · relevé : 3 ép., 5 q. · 11 F, 6 P, 1 S | — |
| 18. Variation de vitesse | T14 | T09, T11, T13, T27 | à faire | 0 | 5/13 · relevé : 6 ép., 18 q. · 9 F, 7 P, 1 S · extraits : X-2021-01 | — |
| 19. Stockage d'énergie électrique | T15 | T01, T07 | à faire | 0 | 5/13 · relevé : 11 ép., 58 q. · 10 F, 7 P, 1 S · extraits : X-2020-01 | — |
| 20. Distribution BT, protection et régimes de neutre | T17 | T02, T06 | à faire | 0 | 5/13 · relevé : 8 ép., 36 q. · 7 F, 7 P, 1 S | — |
| 21. Capteurs et conditionnement du signal | T23 | T19, T20 | à faire | 0 | 9/13 · relevé : 11 ép., 60 q. · 4 F, 6 P, 1 S · extraits : X-2024-01 | — |
| 22. CAN, CNA et échantillonnage | T22 | T20, T23 | à faire | 0 | 6/13 · relevé : 5 ép., 26 q. · 9 F, 6 P, 1 S · extraits : X-2026-04 | — |
| 23. Métrologie, instrumentation, schématisation | T30 | T01, T22, T23 | à faire | 0 | 12/13 · relevé : 9 ép., 12 q. · 7 F, 8 P, 1 S | — |
| 24. Logique combinatoire | T28 | — | à faire | 0 | 3/13 · relevé : 3 ép., 8 q. · 3 F, 6 P, 1 S | — |
| 25. Logique séquentielle, GRAFCET, automates | T29 | T28 | à faire | 0 | 5/13 · relevé : 7 ép., 12 q. · 0 F, 7 P, 1 S | — |
| 26. Systèmes embarqués : microcontrôleurs, API, FPGA | T24 | T22, T28, T29 | à faire | 0 | 6/13 · relevé : 17 ép., 49 q. · 2 F, 6 P, 1 S | — |
| 27. Transmission numérique et protocoles | T25 | T24, T28 | à faire | 0 | 4/13 · relevé : 8 ép., 48 q. · 10 F, 6 P, 1 S · extraits : X-2026-01 | — |

## Infrastructure construite avec le premier chapitre

Mise en place à l'itération du chapitre 1 (T01), documentée dans README-app.md
(section « Cours ») :

- [x] `cours/textes/TXX.html` : un fragment HTML par chapitre (pas de
      `<html>`, pas de `<body>`), titres `<h2>`/`<h3>` munis d'un `id`
      préfixé par le thème (`t01-bref`, `t01-ohm`…).
- [x] `cours/index.json` : `{"chapitres": [{"id", "theme", "ordre", "titre",
      "prerequis": [...], "sommaire": [{"niveau": 2|3, "texte", "id"}],
      "schemas": N}]}`, dans l'ordre du plan. À générer par un script
      (`scripts/indexer_cours.py`) qui lit les fragments, plutôt qu'à la main.
- [x] `js/views/cours.js` : liste des chapitres (`#/cours`) et lecteur
      (`#/cours?theme=TXX`) sur le modèle de `vueEpreuve`
      (`js/views/sujets.js`) : sommaire replié, `rendreMathsDans`, schémas SVG
      agrandissables par `ouvrirPleinEcran`, chapitre précédent / suivant.
- [x] Route `#/cours` dans `js/app.js` (rattachée à l'onglet Catégories pour
      `aria-current`, pas de nouvel onglet dans la barre du bas).
- [x] Écran Catégories (`js/views/categories.js`) : bouton « Lire le cours »
      par catégorie (premier chapitre de la catégorie) et par thème, plus un
      accès à la liste des chapitres. Thèmes hors périmètre : pas de bouton.
- [x] `sw-cours.js` (`self.ASSETS_COURS = [...]` : `cours/index.json` et les
      fragments), importé par `sw.js` comme `sw-sujets.js` ; ajouter
      `./js/views/cours.js` au `SOCLE`. Changer `CACHE_VERSION` dans
      `sw-assets.js` à chaque modification du cours. `build_cards.py`, qui
      générait ce fichier, n'est pas dans ce dépôt : écrire la commande de
      mise à jour (hash du contenu précaché) et la documenter dans
      `README-app.md`.
- [x] Styles du lecteur dans `css/style.css`, avec les jetons existants
      (`--accent`, `--ink`, `--surface`…) : encadré « Formules clés »,
      `<details>` de l'auto-test, `figure`/`figcaption`, `.table-scroll`.
- [x] Harnais de vérification réutilisable (`scripts/verifier_cours.mjs`,
      Playwright Node global 1.56.1 ; Chromium dans `/opt/pw-browsers`) :
      393×852, `isMobile`, thèmes clair et sombre, erreurs KaTeX et console,
      `scrollWidth` = 393, taille rendue des `<text>` SVG ≥ 12 px, largeur
      des formules ≤ 340 px, cibles tactiles ≥ 44 px, captures pleine page.
      Plus un script Python : orthographe (`pyspellchecker`, français) et
      contrôle des ids de cartes cités contre `cards.json`.
- [x] Liens vers une carte : tranché, route `#/reviser?carte=<id>` (une seule
      carte, « Retour au cours » ramène au chapitre). Écrire
      `<a class="id-carte" href="#/reviser?carte=T07-f-003">T07-f-003</a>`.

## Conventions communes à tous les chapitres

Fixées ici pour que la passe finale n'ait pas à harmoniser après coup.

- Structure fixe en onze rubriques (voir la consigne) : En bref, Prérequis,
  L'idée physique, Cours, Schémas, Formules clés, Méthode concours, Pièges,
  Exemple chiffré résolu, Auto-test, Pour réviser.
- Grandeurs : minuscule pour l'instantané ($v(t)$, $i(t)$), majuscule pour
  l'efficace ($V$, $I$), $\langle v\rangle$ pour la moyenne, $\hat V$ pour
  l'amplitude, soulignement pour le complexe ($\underline{V}$), $V$ tension
  simple et $U$ tension composée en triphasé, $\omega$ pulsation électrique,
  $\Omega$ vitesse angulaire en rad/s et $N$ en tr/min (notation des cartes), $p$ variable de
  Laplace (et nombre de paires de pôles en machines : le dire quand les deux
  se côtoient), $\alpha$ rapport cyclique (et angle d'amorçage en T08 : le
  signaler).
- Indices : descriptifs en romain (`\mathrm{}` dans les formules,
  `font-style="normal"` dans les SVG) : $V_\mathrm{s}$, $R_\mathrm{th}$,
  $P_\mathrm{J}$, $i_\mathrm{L1}$ ; indices variables en italique ($E_k$,
  $\varphi_i$) ; noms de points en romain ($\mathrm{A}$, $\mathrm{N}$) ; grandeur
  continue en majuscule (courant $I$, f.é.m. $E$), instantanée en minuscule
  (potentiels $v_\mathrm{A}$, f.é.m. $e$) ; charge notée $R_\mathrm{ch}$.
  Renvoyer à une figure d'un sujet par « sa figure N » ou « figure N du
  sujet », jamais « figure N » seul (confusion avec les figures du cours).
  Un schéma de carte faux se redessine dans `svg/TXX-s-00N.svg`
  et se redirige par le champ `svg` de `corrections/cartes.json` ;
  `indexer_cours.py` l'ajoute au précache.
- Conventions de signe : récepteur par défaut, générateur pour les sources ;
  la convention est dite dans le texte et visible sur le schéma (flèches de
  tension et de courant).
- Nombres : virgule décimale, espace fine avant l'unité, unités SI, puissance
  en W, var, VA (jamais « VAR » ni « kVAR »).
- Schémas : symboles IEC 60617 (résistance rectangulaire, inductance en
  demi-cercles, masse et terre distinctes), SVG inline écrit à la main,
  `viewBox` de 360 de large au plus, `stroke="currentColor"`, accent en
  `var(--accent)`, `role="img"`, `aria-label`, `<figcaption>`. Le corps du
  texte du lecteur fait environ 337 px de large sur l'iPhone 17 : une police
  de 13 unités dans un `viewBox` de 360 rend à environ 12,2 px. Viser 13 au
  minimum et mesurer.
- Citations d'épreuves : « [2024-E2, B7](#/epreuve?id=2024-E2) ». Les numéros
  de question sont ceux du sujet ; le détail de chaque question est dans
  `cours/releve-sujets.json`.
- Formules clés : chaque formule porte l'id de sa carte (ex. T07-f-003). En cas
  de désaccord entre le cours et une carte, revenir à la physique ; si la carte
  est fausse, la corriger dans `corrections/cartes.json` (voir README-app.md)
  et le noter dans la colonne « notes ».

## Constats du relevé des épreuves (2026-10-13)

- **2019-E2 est le mauvais sujet.** `sujets/textes/2019-E2.html` contient
  l'épreuve de l'option Ingénierie des constructions (Pont de la Citadelle,
  Strasbourg), et non « Transformation d'une rame de métro » annoncé par
  `sujets/index.json`. À corriger à la source (`scripts/integrer_sujets.py`
  et le dépôt des sujets, hors de ce dépôt). Ne pas citer 2019-E2 dans le
  cours.
- 2015-E2 et 2016-E2 sont des épreuves d'exploitation pédagogique (quatre
  questions chacune, sans calcul).
- Les épreuves 1 sont communes à toutes les options : mécanique (T10),
  thermique (T05) et questions hors programme électrique y dominent. Les
  questions d'électrotechnique se trouvent surtout dans les épreuves 2 de
  2017 à 2025.
- **Aucune question dédiée** au transformateur (T06) ni aux filtres (T20)
  dans les 22 épreuves de l'app : le transformateur n'y apparaît que comme
  « transformateur parfait » en contexte (2024-E2, B7–B9). Les 13 sujets
  sur lesquels `cards.json` compte les fréquences forment un autre corpus.
  Pour ces chapitres, la méthode concours s'appuie sur les questions voisines
  (chute de tension au secondaire, filtrage d'un conditionneur ou d'un
  anti-repliement) et le dit franchement.
- Formes dominantes, tous thèmes confondus : calcul, « établir une
  expression », compléter un document réponse, conclure sur une conformité à
  un cahier des charges. La méthode concours de chaque chapitre doit couvrir
  ces quatre gestes.

## Relevé par thème

Numéros de question tels qu'imprimés dans le sujet ; le thème est principal
sauf mention « secondaire ». 2019-E2 est listé pour mémoire (mauvais sujet).

### T01 — Grandeurs électriques fondamentales et électrocinétique

Cartes : tombe dans 13 sujets sur 13 · 20 formules, 6 pièges, 2 schéma(s).  
Relevé 2015–2025 : 17 épreuves, 78 questions (30 en thème principal).  
Formes : calcul 40 · établir une expression 24 · lecture de documentation 5 · compléter document réponse 3 · justifier/expliquer 3

- [2025-E1](#/epreuve?id=2025-E1) : — (secondaire : 56, 57)
- [2025-E2](#/epreuve?id=2025-E2) : Q1, Q2, Q25, Q26, Q36 (secondaire : Q4, Q8, Q21, Q27, Q31)
- [2024-E1](#/epreuve?id=2024-E1) : 37, 40 (secondaire : 4, 38, 39, 41)
- [2024-E2](#/epreuve?id=2024-E2) : — (secondaire : E1, E4, E6, E7, E8, E9)
- [2023-E2](#/epreuve?id=2023-E2) : B2 (secondaire : C1, C2, C3, C4, F2, F6, F7)
- [2022-E1](#/epreuve?id=2022-E1) : 4, 5
- [2022-E2](#/epreuve?id=2022-E2) : 25, 33, 34
- [2020-E1](#/epreuve?id=2020-E1) : 19
- [2020-E2](#/epreuve?id=2020-E2) : 9, 14 (secondaire : 3, 13)
- [2019-E1](#/epreuve?id=2019-E1) : 4, 16 (secondaire : 8, 18)
- [2019-E2](#/epreuve?id=2019-E2) : — (secondaire : 13)
- [2018-E1](#/epreuve?id=2018-E1) : — (secondaire : 18, 21, 22)
- [2018-E2](#/epreuve?id=2018-E2) : 11, 28, 29 (secondaire : 4, 5, 10, 27)
- [2017-E1](#/epreuve?id=2017-E1) : — (secondaire : 24)
- [2017-E2](#/epreuve?id=2017-E2) : C1.1, C1.2, C3.1, C3.3, C3.5, C3.7, C3.9, D2.3 (secondaire : C3.2, C3.4, C3.6, C3.8, C3.10, D1.1, D2.2, D2.4)
- [2016-E1](#/epreuve?id=2016-E1) : — (secondaire : 17, 18, 19)
- [2015-E1](#/epreuve?id=2015-E1) : 29

### T03 — Représentation complexe et impédances

Cartes : tombe dans 12 sujets sur 13 · 19 formules, 6 pièges, 1 schéma(s).  
Relevé 2015–2025 : 3 épreuves, 4 questions (1 en thème principal).  
Formes : calcul 3 · établir une expression 1

- [2025-E2](#/epreuve?id=2025-E2) : — (secondaire : Q22)
- [2024-E2](#/epreuve?id=2024-E2) : — (secondaire : A4)
- [2018-E2](#/epreuve?id=2018-E2) : 10 (secondaire : 11)

### T02 — Puissance en régime alternatif sinusoïdal (AC)

Cartes : tombe dans 13 sujets sur 13 · 35 formules, 8 pièges, 1 schéma(s).  
Relevé 2015–2025 : 8 épreuves, 26 questions (18 en thème principal).  
Formes : calcul 16 · justifier/expliquer 3 · choix/dimensionnement 3 · établir une expression 2 · lecture de documentation 2

- [2025-E2](#/epreuve?id=2025-E2) : Q22
- [2024-E1](#/epreuve?id=2024-E1) : — (secondaire : 46)
- [2024-E2](#/epreuve?id=2024-E2) : B1, B2, B3, B4, B6, B7 (secondaire : A5, B8)
- [2021-E1](#/epreuve?id=2021-E1) : — (secondaire : 18)
- [2020-E2](#/epreuve?id=2020-E2) : — (secondaire : 19, 20)
- [2018-E2](#/epreuve?id=2018-E2) : 13, 14, 15, 27 (secondaire : 7, 8)
- [2017-E2](#/epreuve?id=2017-E2) : B1.1, B1.2, B2.1, B2.2, B2.3
- [2015-E1](#/epreuve?id=2015-E1) : 28, 30

### T04 — Harmoniques réseau, THD et puissance déformante

Cartes : tombe dans 9 sujets sur 13 · 15 formules, 6 pièges, 1 schéma(s).  
Relevé 2015–2025 : 5 épreuves, 12 questions (8 en thème principal).  
Formes : justifier/expliquer 6 · compléter document réponse 2 · calcul 2 · conclure/valider 1 · lecture de documentation 1

- [2025-E2](#/epreuve?id=2025-E2) : Q23
- [2024-E1](#/epreuve?id=2024-E1) : — (secondaire : 47)
- [2024-E2](#/epreuve?id=2024-E2) : B10, B11, B12 (secondaire : B13)
- [2023-E1](#/epreuve?id=2023-E1) : — (secondaire : 16, 17)
- [2018-E2](#/epreuve?id=2018-E2) : 7, 8, 9, 12

### T06 — Transformateur (monophasé et triphasé)

Cartes : tombe dans 13 sujets sur 13 · 14 formules, 6 pièges, 1 schéma(s).  
Relevé 2015–2025 : aucune question dédiée dans les 22 épreuves de l'app.

### T18 — Circuits électroniques - composants (diode, transistor)

Cartes : tombe dans 4 sujets sur 13 · 7 formules, 7 pièges, 1 schéma(s).  
Relevé 2015–2025 : 2 épreuves, 2 questions (1 en thème principal).  
Formes : compléter document réponse 1 · justifier/expliquer 1

- [2025-E2](#/epreuve?id=2025-E2) : — (secondaire : Q24)
- [2022-E1](#/epreuve?id=2022-E1) : 27

### T07 — Hacheurs (1, 2 et 4 quadrants)

Cartes : tombe dans 12 sujets sur 13 · 13 formules, 6 pièges, 1 schéma(s).  
Relevé 2015–2025 : 5 épreuves, 34 questions (23 en thème principal).  
Formes : établir une expression 12 · compléter document réponse 6 · justifier/expliquer 6 · calcul 4 · tracé/chronogramme 2

- [2025-E2](#/epreuve?id=2025-E2) : Q14, Q19, Q24, Q27, Q28, Q29, Q30, Q31, Q32, Q35 (secondaire : Q15, Q18, Q25, Q26, Q37, Q38, Q39, Q40)
- [2024-E1](#/epreuve?id=2024-E1) : — (secondaire : 48)
- [2023-E2](#/epreuve?id=2023-E2) : C3, C4, C5, C6, C7, C8 (secondaire : B3)
- [2022-E1](#/epreuve?id=2022-E1) : 21, 22
- [2022-E2](#/epreuve?id=2022-E2) : 30, 31, 35, 36, 37 (secondaire : 32)

### T08 — Redresseurs (monophasé et triphasé)

Cartes : tombe dans 13 sujets sur 13 · 12 formules, 6 pièges, 1 schéma(s).  
Relevé 2015–2025 : 3 épreuves, 6 questions (3 en thème principal).  
Formes : compléter document réponse 3 · justifier/expliquer 1 · conclure/valider 1 · pédagogie 1

- [2024-E1](#/epreuve?id=2024-E1) : 47, 48, 49
- [2023-E1](#/epreuve?id=2023-E1) : — (secondaire : 16)
- [2022-E2](#/epreuve?id=2022-E2) : — (secondaire : 31, 32)

### T09 — Onduleurs (monophasé et triphasé)

Cartes : tombe dans 12 sujets sur 13 · 13 formules, 7 pièges, 1 schéma(s).  
Relevé 2015–2025 : 5 épreuves, 11 questions (5 en thème principal).  
Formes : justifier/expliquer 4 · compléter document réponse 2 · choix/dimensionnement 2 · tracé/chronogramme 1 · calcul 1

- [2025-E2](#/epreuve?id=2025-E2) : Q20, Q21 (secondaire : Q14, Q23)
- [2024-E2](#/epreuve?id=2024-E2) : B13 (secondaire : B12)
- [2023-E1](#/epreuve?id=2023-E1) : 16, 17
- [2021-E2](#/epreuve?id=2021-E2) : — (secondaire : 13)
- [2016-E1](#/epreuve?id=2016-E1) : — (secondaire : 29, 30)

### T20 — Filtres RC/RL - 1er et 2e ordre

Cartes : tombe dans 5 sujets sur 13 · 12 formules, 7 pièges, 1 schéma(s).  
Relevé 2015–2025 : aucune question dédiée dans les 22 épreuves de l'app.

### T19 — AOP (amplificateur opérationnel)

Cartes : tombe dans 4 sujets sur 13 · 12 formules, 7 pièges, 1 schéma(s).  
Relevé 2015–2025 : 3 épreuves, 16 questions (15 en thème principal).  
Formes : établir une expression 8 · calcul 4 · conclure/valider 2 · compléter document réponse 1 · tracé/chronogramme 1

- [2025-E1](#/epreuve?id=2025-E1) : — (secondaire : 59)
- [2024-E2](#/epreuve?id=2024-E2) : E1, E2, E3, E4, E5, E6, E7, E8, E9, E10
- [2023-E2](#/epreuve?id=2023-E2) : F6, F7, F8, F9, F10

### T26 — Modélisation des systèmes linéaires (automatique)

Cartes : tombe dans 9 sujets sur 13 · 10 formules, 7 pièges, 1 schéma(s).  
Relevé 2015–2025 : 8 épreuves, 29 questions (17 en thème principal).  
Formes : établir une expression 11 · calcul 5 · justifier/expliquer 4 · compléter document réponse 4 · conclure/valider 3

- [2025-E2](#/epreuve?id=2025-E2) : Q37, Q38, Q39, Q40, Q41 (secondaire : Q42)
- [2024-E2](#/epreuve?id=2024-E2) : C3, C4, C6 (secondaire : C5, C7)
- [2023-E1](#/epreuve?id=2023-E1) : — (secondaire : 45)
- [2023-E2](#/epreuve?id=2023-E2) : D6 (secondaire : D4, D5)
- [2021-E1](#/epreuve?id=2021-E1) : 14, 15, 31, 32 (secondaire : 19, 20)
- [2017-E1](#/epreuve?id=2017-E1) : 23 (secondaire : 22, 25)
- [2017-E2](#/epreuve?id=2017-E2) : — (secondaire : C1.1)
- [2015-E1](#/epreuve?id=2015-E1) : 10, 11, 12 (secondaire : 13)

### T21 — Fonctions de transfert - Diagramme de Bode

Cartes : tombe dans 8 sujets sur 13 · 13 formules, 8 pièges, 1 schéma(s).  
Relevé 2015–2025 : 2 épreuves, 5 questions (2 en thème principal).  
Formes : lecture de documentation 3 · tracé/chronogramme 1 · calcul 1

- [2024-E2](#/epreuve?id=2024-E2) : — (secondaire : C10, C12)
- [2023-E2](#/epreuve?id=2023-E2) : D4, D7 (secondaire : D8)

### T27 — Systèmes bouclés, correcteurs, stabilité

Cartes : tombe dans 9 sujets sur 13 · 9 formules, 7 pièges, 1 schéma(s).  
Relevé 2015–2025 : 9 épreuves, 31 questions (23 en thème principal).  
Formes : conclure/valider 9 · justifier/expliquer 5 · établir une expression 5 · lecture de documentation 4 · calcul 3

- [2025-E1](#/epreuve?id=2025-E1) : 18 (secondaire : 28)
- [2025-E2](#/epreuve?id=2025-E2) : Q42
- [2024-E2](#/epreuve?id=2024-E2) : C5, C7, C8, C9, C10, C11, C12, C13 (secondaire : C6)
- [2023-E1](#/epreuve?id=2023-E1) : 45, 48, 49 (secondaire : 50)
- [2023-E2](#/epreuve?id=2023-E2) : D8, D9 (secondaire : D6, D7)
- [2022-E2](#/epreuve?id=2022-E2) : 26, 27, 28, 29 (secondaire : 37)
- [2021-E1](#/epreuve?id=2021-E1) : 33
- [2019-E1](#/epreuve?id=2019-E1) : — (secondaire : 13)
- [2015-E1](#/epreuve?id=2015-E1) : 13, 14, 15 (secondaire : 11)

### T11 — Machine à courant continu (MCC)

Cartes : tombe dans 10 sujets sur 13 · 15 formules, 6 pièges, 1 schéma(s).  
Relevé 2015–2025 : 1 épreuves, 2 questions (0 en thème principal).  
Formes : justifier/expliquer 1 · choix/dimensionnement 1

- [2020-E2](#/epreuve?id=2020-E2) : — (secondaire : 16, 18)

### T13 — Machine asynchrone (MAS)

Cartes : tombe dans 7 sujets sur 13 · 17 formules, 7 pièges, 1 schéma(s).  
Relevé 2015–2025 : 8 épreuves, 37 questions (23 en thème principal).  
Formes : calcul 12 · conclure/valider 9 · établir une expression 5 · choix/dimensionnement 3 · justifier/expliquer 3

- [2025-E1](#/epreuve?id=2025-E1) : 54 (secondaire : 60)
- [2024-E2](#/epreuve?id=2024-E2) : A3, A4, A5, A6, A7, A8, C1, C2, D15, D16, D17 (secondaire : A2)
- [2023-E1](#/epreuve?id=2023-E1) : 18, 19 (secondaire : 20, 40)
- [2022-E1](#/epreuve?id=2022-E1) : — (secondaire : 11, 13, 15)
- [2021-E1](#/epreuve?id=2021-E1) : 13, 16, 17, 18, 19, 20, 40 (secondaire : 12, 14)
- [2021-E2](#/epreuve?id=2021-E2) : — (secondaire : 15, 16)
- [2017-E1](#/epreuve?id=2017-E1) : 8 (secondaire : 6)
- [2015-E1](#/epreuve?id=2015-E1) : 19 (secondaire : 18, 22)

### T12 — Machine synchrone et brushless (PMSM,/,BLDC)

Cartes : tombe dans 4 sujets sur 13 · 11 formules, 6 pièges, 1 schéma(s).  
Relevé 2015–2025 : 3 épreuves, 5 questions (3 en thème principal).  
Formes : justifier/expliquer 2 · compléter document réponse 1 · calcul 1 · choix/dimensionnement 1

- [2025-E1](#/epreuve?id=2025-E1) : — (secondaire : 18)
- [2024-E1](#/epreuve?id=2024-E1) : 45, 46 (secondaire : 44)
- [2020-E1](#/epreuve?id=2020-E1) : 8

### T14 — Variation de vitesse et de couple des machines

Cartes : tombe dans 5 sujets sur 13 · 9 formules, 7 pièges, 1 schéma(s).  
Relevé 2015–2025 : 6 épreuves, 18 questions (8 en thème principal).  
Formes : compléter document réponse 4 · établir une expression 3 · choix/dimensionnement 3 · conclure/valider 2 · justifier/expliquer 2

- [2024-E1](#/epreuve?id=2024-E1) : 44 (secondaire : 49)
- [2024-E2](#/epreuve?id=2024-E2) : — (secondaire : B13, C1, C2, C4)
- [2023-E1](#/epreuve?id=2023-E1) : 20, 21 (secondaire : 15, 19, 25)
- [2023-E2](#/epreuve?id=2023-E2) : A7
- [2021-E2](#/epreuve?id=2021-E2) : 15, 16, 18, 19 (secondaire : 17)
- [2017-E1](#/epreuve?id=2017-E1) : — (secondaire : 7)

### T15 — Stockage d'énergie électrique

Cartes : tombe dans 5 sujets sur 13 · 10 formules, 7 pièges, 1 schéma(s).  
Relevé 2015–2025 : 11 épreuves, 58 questions (38 en thème principal).  
Formes : calcul 31 · conclure/valider 10 · choix/dimensionnement 5 · justifier/expliquer 5 · lecture de documentation 2

- [2025-E2](#/epreuve?id=2025-E2) : Q8, Q9, Q10, Q11, Q12, Q13, Q33, Q34 (secondaire : Q35)
- [2024-E1](#/epreuve?id=2024-E1) : 51, 52, 53 (secondaire : 50)
- [2023-E2](#/epreuve?id=2023-E2) : A8, A9, C1, C2, F1 (secondaire : B2, B3, B4, B5)
- [2022-E1](#/epreuve?id=2022-E1) : — (secondaire : 20, 26)
- [2021-E2](#/epreuve?id=2021-E2) : 1, 5, 6, 9, 10, 27, 28 (secondaire : 29)
- [2020-E1](#/epreuve?id=2020-E1) : 20, 21, 22 (secondaire : 16, 19, 30)
- [2020-E2](#/epreuve?id=2020-E2) : 12, 13, 15, 16 (secondaire : 9, 14)
- [2019-E1](#/epreuve?id=2019-E1) : 15, 17, 18, 19, 20 (secondaire : 16, 28)
- [2018-E1](#/epreuve?id=2018-E1) : 20, 21, 22 (secondaire : 23)
- [2016-E1](#/epreuve?id=2016-E1) : — (secondaire : 30)
- [2016-E2](#/epreuve?id=2016-E2) : — (secondaire : 1, 4)

### T17 — Distribution et sécurité électrique, régimes de neutre

Cartes : tombe dans 5 sujets sur 13 · 7 formules, 7 pièges, 1 schéma(s).  
Relevé 2015–2025 : 8 épreuves, 36 questions (26 en thème principal).  
Formes : choix/dimensionnement 11 · calcul 6 · justifier/expliquer 6 · schéma/câblage 5 · établir une expression 4

- [2024-E1](#/epreuve?id=2024-E1) : 38, 39, 41, 42, 43 (secondaire : 40)
- [2024-E2](#/epreuve?id=2024-E2) : B5, B8, B9 (secondaire : B7)
- [2022-E1](#/epreuve?id=2022-E1) : 13, 15 (secondaire : 14)
- [2021-E2](#/epreuve?id=2021-E2) : 17 (secondaire : 18, 19)
- [2020-E2](#/epreuve?id=2020-E2) : 17, 18, 19, 20, 21
- [2018-E2](#/epreuve?id=2018-E2) : 6, 16, 17, 18, 19, 20, 21, 22 (secondaire : 15, 23)
- [2017-E2](#/epreuve?id=2017-E2) : B1.3, B1.4 (secondaire : B2.3)
- [2015-E1](#/epreuve?id=2015-E1) : — (secondaire : 28, 30)

### T23 — Capteurs et Conditionnement du signal

Cartes : tombe dans 9 sujets sur 13 · 4 formules, 6 pièges, 1 schéma(s).  
Relevé 2015–2025 : 11 épreuves, 60 questions (40 en thème principal).  
Formes : calcul 15 · justifier/expliquer 10 · établir une expression 6 · choix/dimensionnement 6 · conclure/valider 6

- [2025-E1](#/epreuve?id=2025-E1) : 25, 26, 55, 56, 57, 58, 59 (secondaire : 29)
- [2024-E1](#/epreuve?id=2024-E1) : 22, 23, 24
- [2024-E2](#/epreuve?id=2024-E2) : D1, D2, D3, D4, D5 (secondaire : E5, E10)
- [2023-E1](#/epreuve?id=2023-E1) : 46, 47, 50 (secondaire : 49, 52)
- [2023-E2](#/epreuve?id=2023-E2) : D2, D3, D5, E1, E2, F2 (secondaire : F4, F10)
- [2022-E1](#/epreuve?id=2022-E1) : 26 (secondaire : 16, 17, 24)
- [2021-E1](#/epreuve?id=2021-E1) : 22, 25, 26 (secondaire : 21, 23, 27)
- [2021-E2](#/epreuve?id=2021-E2) : 20, 21, 22, 25 (secondaire : 23, 24)
- [2020-E1](#/epreuve?id=2020-E1) : 15 (secondaire : 12, 13)
- [2020-E2](#/epreuve?id=2020-E2) : 2, 3, 4, 5, 6, 7, 23 (secondaire : 8, 24)
- [2019-E1](#/epreuve?id=2019-E1) : — (secondaire : 6)

### T22 — CAN/CNA - Numérisation et échantillonnage

Cartes : tombe dans 6 sujets sur 13 · 9 formules, 6 pièges, 1 schéma(s).  
Relevé 2015–2025 : 5 épreuves, 26 questions (17 en thème principal).  
Formes : calcul 12 · compléter document réponse 3 · établir une expression 3 · tracé/chronogramme 2 · lecture de documentation 2

- [2025-E1](#/epreuve?id=2025-E1) : 19, 23, 24, 27, 65 (secondaire : 21, 26, 66)
- [2024-E2](#/epreuve?id=2024-E2) : D6, D7, D8, D9, D10, D11, D12 (secondaire : D14)
- [2023-E2](#/epreuve?id=2023-E2) : F3, F4 (secondaire : D2, D3)
- [2022-E1](#/epreuve?id=2022-E1) : 23, 24 (secondaire : 25, 27, 30)
- [2021-E2](#/epreuve?id=2021-E2) : 23

### T30 — Métrologie, instrumentation, schématisation

Cartes : tombe dans 12 sujets sur 13 · 7 formules, 8 pièges, 1 schéma(s).  
Relevé 2015–2025 : 9 épreuves, 12 questions (4 en thème principal).  
Formes : schéma/câblage 3 · calcul 3 · conclure/valider 3 · pédagogie 2 · justifier/expliquer 1

- [2025-E1](#/epreuve?id=2025-E1) : — (secondaire : 35)
- [2024-E1](#/epreuve?id=2024-E1) : — (secondaire : 54)
- [2022-E1](#/epreuve?id=2022-E1) : 14
- [2021-E2](#/epreuve?id=2021-E2) : — (secondaire : 21, 25)
- [2020-E2](#/epreuve?id=2020-E2) : 8 (secondaire : 7)
- [2019-E2](#/epreuve?id=2019-E2) : 20, 21
- [2018-E2](#/epreuve?id=2018-E2) : — (secondaire : 22)
- [2017-E2](#/epreuve?id=2017-E2) : — (secondaire : B1.4)
- [2015-E1](#/epreuve?id=2015-E1) : — (secondaire : 7)

### T28 — Logique combinatoire

Cartes : tombe dans 3 sujets sur 13 · 3 formules, 6 pièges, 1 schéma(s).  
Relevé 2015–2025 : 3 épreuves, 8 questions (3 en thème principal).  
Formes : compléter document réponse 3 · programmation/algorithme 2 · schéma/câblage 1 · tracé/chronogramme 1 · calcul 1

- [2024-E1](#/epreuve?id=2024-E1) : — (secondaire : 26, 29)
- [2024-E2](#/epreuve?id=2024-E2) : D13 (secondaire : D19, D20, D21)
- [2018-E1](#/epreuve?id=2018-E1) : 26, 27

### T29 — Logique séquentielle, GRAFCET, automates programmables

Cartes : tombe dans 5 sujets sur 13 · 0 formules, 7 pièges, 1 schéma(s).  
Relevé 2015–2025 : 7 épreuves, 12 questions (10 en thème principal).  
Formes : programmation/algorithme 4 · tracé/chronogramme 2 · lecture de documentation 2 · calcul 1 · conclure/valider 1

- [2024-E1](#/epreuve?id=2024-E1) : 69
- [2024-E2](#/epreuve?id=2024-E2) : D20, D21
- [2021-E1](#/epreuve?id=2021-E1) : 29 (secondaire : 30)
- [2021-E2](#/epreuve?id=2021-E2) : 3, 7
- [2019-E1](#/epreuve?id=2019-E1) : 3
- [2017-E1](#/epreuve?id=2017-E1) : 30, 31, 32
- [2017-E2](#/epreuve?id=2017-E2) : — (secondaire : A3)

### T24 — Systèmes embarqués - Microcontrôleurs, API, FPGA

Cartes : tombe dans 6 sujets sur 13 · 2 formules, 6 pièges, 1 schéma(s).  
Relevé 2015–2025 : 17 épreuves, 49 questions (33 en thème principal).  
Formes : programmation/algorithme 24 · schéma/câblage 5 · compléter document réponse 5 · calcul 4 · lecture de documentation 4

- [2025-E1](#/epreuve?id=2025-E1) : 21, 67, 68 (secondaire : 22)
- [2025-E2](#/epreuve?id=2025-E2) : Q5
- [2024-E1](#/epreuve?id=2024-E1) : 68 (secondaire : 23)
- [2024-E2](#/epreuve?id=2024-E2) : D14, D18, D19 (secondaire : D3, D6, D7, D10)
- [2023-E1](#/epreuve?id=2023-E1) : 56, 57 (secondaire : 51, 54)
- [2023-E2](#/epreuve?id=2023-E2) : — (secondaire : E3)
- [2022-E1](#/epreuve?id=2022-E1) : 9, 17, 25 (secondaire : 23)
- [2022-E2](#/epreuve?id=2022-E2) : 20, 21, 22 (secondaire : 23)
- [2021-E1](#/epreuve?id=2021-E1) : 27
- [2021-E2](#/epreuve?id=2021-E2) : 24 (secondaire : 19, 20)
- [2020-E1](#/epreuve?id=2020-E1) : 13, 14
- [2020-E2](#/epreuve?id=2020-E2) : 24, 25
- [2019-E1](#/epreuve?id=2019-E1) : 5, 6 (secondaire : 3, 4)
- [2018-E1](#/epreuve?id=2018-E1) : 23, 24, 25
- [2018-E2](#/epreuve?id=2018-E2) : 24
- [2017-E1](#/epreuve?id=2017-E1) : — (secondaire : 30)
- [2017-E2](#/epreuve?id=2017-E2) : A1, A2, A3, A4, A5

### T25 — Transmission numérique - Modulations et protocoles

Cartes : tombe dans 4 sujets sur 13 · 10 formules, 6 pièges, 1 schéma(s).  
Relevé 2015–2025 : 8 épreuves, 48 questions (42 en thème principal).  
Formes : calcul 15 · lecture de documentation 8 · justifier/expliquer 6 · conclure/valider 6 · compléter document réponse 4

- [2025-E1](#/epreuve?id=2025-E1) : 20, 22, 61, 62, 63, 64, 66, 69, 70, 71 (secondaire : 65, 68)
- [2024-E1](#/epreuve?id=2024-E1) : 25, 26, 27, 28, 29, 30, 31, 32 (secondaire : 33, 34)
- [2023-E1](#/epreuve?id=2023-E1) : 22, 23, 24, 25 (secondaire : 26, 27)
- [2023-E2](#/epreuve?id=2023-E2) : E3, E4, E5, E6, E7, E8
- [2022-E1](#/epreuve?id=2022-E1) : 16, 28, 29, 30, 31
- [2018-E2](#/epreuve?id=2018-E2) : 23, 25, 26
- [2017-E1](#/epreuve?id=2017-E1) : 29
- [2015-E1](#/epreuve?id=2015-E1) : 23, 24, 25, 26, 27

