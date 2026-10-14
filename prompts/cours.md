# Prompt : génération du cours (génie électrique, informatique et automatique)

> Mode d'emploi : dans une nouvelle session Claude Code sur ce dépôt, écrire
> `/loop lance prompts/cours.md` (sans durée : le rythme est réglé
> automatiquement, un chapitre par tour). La progression vit dans
> `cours/PROGRES.md` : relancer la même commande reprend au bon chapitre.
> Pour ajouter la thermique (T05) ou les renouvelables (T16), ajouter leur code
> à la liste « Périmètre » ci-dessous.

---

Tu travailles dans le dépôt capet-revision : la PWA de révision du CAPET SII
option Ingénierie électrique, utilisée uniquement sur iPhone 17 (393×852).
Mission : rédiger, chapitre par chapitre, le meilleur cours possible pour le
génie électrique et le génie informatique et automatique. Le cours doit être
lisible sur téléphone, contenir un maximum de schémas et être intégré à l'app.

## 0. À chaque itération, commence ici
1. Lis cours/PROGRES.md. S'il n'existe pas, fais l'étape 1, commit, push, et
   termine l'itération.
2. Prends le premier chapitre au statut « à faire ». Un seul chapitre par
   itération.
3. Quand plus aucun chapitre n'est « à faire », fais la passe finale
   (étape 6), puis arrête la boucle.

## 1. Plan (première itération seulement)
Lis avant d'écrire quoi que ce soit :
- cards.json : thèmes, formules, pièges, schémas. C'est le socle : chaque
  formule et chaque piège du thème doit apparaître dans le cours.
- js/categories.js : génies et catégories.
- sujets/index.json et sujets/textes/*.html : les 22 épreuves 2015–2025.
  Relève où chaque thème tombe et sous quelle forme de question.
- exercices.json.
Périmètre :
- génie électrique : T01–T04, T06–T09, T11–T15, T17–T20, T22, T23, T30 ;
- génie informatique et automatique : T21, T24–T29.
Un chapitre = un thème. Ordonne-les du fondamental vers l'appliqué, en
mettant les prérequis d'abord. Écris le plan dans cours/PROGRES.md sous forme
de tableau : chapitre | thème | prérequis | statut | tours | notes |
défauts restants.

## 2. Contenu exigé pour chaque chapitre
Public : un candidat au CAPET (bac+5) qui révise. Vise la rigueur d'un cours
de préparation à l'agrégation et la clarté d'un excellent manuel. Le français
doit être irréprochable ; symboles normalisés (IEC 60617) et notations du
concours.
Structure fixe :
1. En bref : à quoi sert ce chapitre au concours, avec la fréquence tirée de
   cards.json (« tombe dans N sujets sur 13 »).
2. Prérequis : liens vers les chapitres concernés.
3. L'idée physique : l'intuition avant les équations, avec un schéma.
4. Cours : sections courtes. Chaque résultat est démontré ou justifié.
   Hypothèses et conventions (récepteur/générateur, sens des flèches)
   explicites.
5. Schémas : au moins un par section (montages, chronogrammes, diagrammes de
   Fresnel, caractéristiques, schémas-blocs, Bode, GRAFCET, trames de bus…).
   Toute grandeur dessinée est nommée dans le texte, et inversement.
6. Formules clés : encadré récapitulatif. Chaque formule avec ses unités, son
   domaine de validité et l'id de sa carte (ex. T07-f-003).
7. Méthode concours : la démarche pas à pas pour les questions qui tombent,
   appuyée sur des questions réelles des sujets. Cite l'épreuve et l'année,
   avec un lien #/epreuve?id=2021-E2.
8. Pièges : tous ceux du thème dans cards.json, reformulés (l'erreur, puis la
   bonne règle).
9. Exemple chiffré résolu : un problème complet de niveau concours, avec des
   données réalistes. Chaque calcul est détaillé avec ses unités, et l'ordre
   de grandeur commenté.
10. Auto-test : 4 à 6 questions de difficulté croissante, réponses dans
    <details>.
11. Pour réviser : lien #/reviser?theme=TXX.

## 3. Format technique (iPhone 17)
- Fichiers : un fragment HTML par chapitre dans cours/textes/TXX.html, plus
  cours/index.json (id, thème, titre, sommaire niveaux 2–3, nombre de
  schémas).
- Hors ligne : précache via un nouveau sw-cours.js importé par sw.js (même
  modèle que sw-sujets.js). Mets à jour CACHE_VERSION dans sw-assets.js
  (commande documentée dans README-app.md).
- Lecteur : réutilise le modèle de vueEpreuve (js/views/sujets.js) : sommaire
  replié, rendreMathsDans, schémas agrandissables avec ouvrirPleinEcran,
  chapitre précédent/suivant.
- Accès : route #/cours?theme=TXX. Un bouton « Lire le cours » sur l'écran
  Catégories (par catégorie et par thème) et une liste des chapitres. Pas de
  nouvel onglet dans la barre du bas.
- Maths : $…$ et $$…$$ rendus par KaTeX. Aucune formule affichée ne dépasse
  340 px de large : coupe avec aligned ou sur plusieurs lignes.
- Schémas : SVG inline écrits à la main.
  - viewBox de 360 de large au maximum, affiché en width:100%.
  - Texte d'au moins 12 px une fois rendu.
  - stroke="currentColor" et var(--accent) pour la couleur d'accent.
  - Fond transparent, lisible en mode clair comme en mode sombre.
  - role="img", aria-label qui décrit le schéma, et un <figcaption>.
  - Aucune image ni ressource externe.
- Tableaux : 3 colonnes au maximum. Au-delà, une liste, ou un tableau dans
  .table-scroll.
- Mise en page :
  - aucun défilement horizontal de la page ;
  - cibles tactiles de 44 px au minimum ;
  - paragraphes de 6 lignes d'écran au plus ;
  - styles dans css/style.css avec les jetons de couleur existants (palette
    terracotta).

## 4. Boucle qualité (obligatoire pour chaque chapitre)
Après la rédaction, répète ce cycle jusqu'à la condition de sortie :
a. Vérifications automatiques. Lance Playwright à 393×852 avec isMobile, en
   mode clair ET en mode sombre :
   - 0 erreur KaTeX et 0 erreur console ;
   - largeur de défilement de la page = 393 ;
   - texte des SVG d'au moins 12 px une fois rendu ;
   - captures d'écran du chapitre entier, que tu regardes vraiment pour
     repérer chevauchements, textes coupés et contrastes faibles.
   Passe aussi le correcteur orthographique (pyspellchecker, français).
b. Vérification des calculs :
   - refais chaque application numérique en Python ;
   - contrôle l'homogénéité de chaque formule ;
   - compare chaque formule à cards.json. Toute contradiction est un défaut
     bloquant, à trancher en revenant à la physique.
c. Relecture adverse : lance un sous-agent relecteur qui n'a pas écrit le
   chapitre. Son rôle est de chercher les erreurs, pas de valider. Il note
   chaque critère sur 5 et liste les défauts avec leur gravité (bloquant,
   majeur, mineur). Critères :
   - exactitude scientifique ;
   - couverture (formules, pièges, forme réelle des questions de concours) ;
   - nombre et qualité des schémas ;
   - progression pédagogique ;
   - lisibilité sur iPhone ;
   - langue.
d. Corrige tous les défauts bloquants et majeurs, puis reprends en a.
Sortie : 0 défaut bloquant, 0 majeur, tous les critères à 4/5 ou plus, et
l'exactitude à 5/5.
Au bout de 5 tours sans sortie : statut « à reprendre », avec la liste des
défauts restants, puis passe au chapitre suivant.
Ne marque jamais un chapitre « validé » sans que a. et b. aient tourné sur
sa version finale.

## 5. Fin d'itération
Mets à jour cours/PROGRES.md (statut, tours, notes, défauts restants).
Commit en français (« Cours : T07 Hacheurs »), puis push sur main.

## 6. Passe finale
Quand plus aucun chapitre n'est « à faire » :
1. Retravaille les chapitres « à reprendre » avec la boucle de l'étape 4.
2. Vérifie la cohérence des notations entre chapitres et que tous les liens
   (prérequis, épreuves, cartes) fonctionnent.
3. Relance les vérifications automatiques sur tous les chapitres.
4. Documente le cours dans README-app.md, puis push.
5. Donne le lien du site et un bilan : chapitres validés, nombre de schémas,
   défauts connus.
