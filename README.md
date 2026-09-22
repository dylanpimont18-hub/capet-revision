# Révision CAPET SII — Ingénierie Électrique

Application web de révision par rappel actif, pour la préparation au CAPET SII
option Ingénierie Électrique (session 2026).

**→ [Ouvrir l'application](https://dylanpimont18-hub.github.io/capet-revision/)**

## Ce que c'est

574 cartes de révision extraites automatiquement d'un corpus de fiches
personnelles et des sujets officiels 2013–2026 :

| Type | Nombre | Contenu |
|---|---:|---|
| Formules | 344 | relation à énoncer, avec unités et conditions d'application |
| Pièges | 199 | une application de formule à juger légitime ou non |
| Schémas | 31 | montage à reconnaître, rendu en SVG depuis les sources LaTeX |

Chaque carte est pondérée par la **fréquence d'apparition de son thème au
concours** (relevé sur 13 sujets), de sorte que la file quotidienne fait
remonter d'abord ce qui tombe souvent.

## Utilisation

Ouvrir le lien ci-dessus. Sur iPhone : Safari → Partager → **Ajouter à
l'écran d'accueil**. L'app fonctionne ensuite hors-ligne, en mode Avion.

L'ajout à l'écran d'accueil n'est pas cosmétique : Safari purge les données
d'un site simplement visité après 7 jours d'inactivité, mais pas celles d'une
application installée. La progression est stockée sur l'appareil, sans serveur
ni compte — l'export JSON de l'écran Réglages en est la seule sauvegarde.

## Trois écrans

- **Réviser** — la file du jour (~30 cartes, 20 min). On formule mentalement,
  on révèle, on s'auto-note *su / hésité / raté*. Répétition espacée SM-2
  plafonnée à 60 jours, pour que rien ne sorte de l'horizon de l'épreuve.
- **Priorités** — les 30 thèmes croisés fréquence au concours × maîtrise réelle.
  En rouge : ce qui tombe souvent et qu'on rate.
- **Réglages** — export et import de la progression, réinitialisation.

## Technique

Page statique : JavaScript sans dépendance ni étape de compilation, KaTeX
embarqué localement, service worker pour le hors-ligne. Aucune requête réseau
à l'exécution, aucune donnée transmise.

Le contenu est un artefact régénéré depuis les sources LaTeX du dépôt de
travail (privé) par un pipeline Python ; il n'est pas rédigé ici.
Voir `README-app.md` pour la régénération.
