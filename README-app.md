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
