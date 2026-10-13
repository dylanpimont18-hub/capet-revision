// app/js/categories.js
// Huit familles qui regroupent les trente thèmes du corpus. Les thèmes sont
// l'unité du concours (fréquence relevée sujet par sujet) ; les catégories
// sont l'unité de révision choisie : « ce soir, l'électronique de puissance ».
// L'ordre suit la progression naturelle du programme.

export const CATEGORIES = [
  { code: "fondamentaux", titre: "Fondamentaux électriques",
    resume: "Lois de base, puissances, complexes, harmoniques",
    themes: ["T01", "T02", "T03", "T04"] },
  { code: "puissance", titre: "Électronique de puissance",
    resume: "Hacheurs, redresseurs, onduleurs",
    themes: ["T07", "T08", "T09"] },
  { code: "machines", titre: "Machines et entraînements",
    resume: "Transformateur, MCC, synchrone, asynchrone, variation de vitesse, mécanique",
    themes: ["T06", "T10", "T11", "T12", "T13", "T14"] },
  { code: "energie", titre: "Énergie, réseau et sécurité",
    resume: "Stockage, renouvelables, distribution, régimes de neutre",
    themes: ["T15", "T16", "T17"] },
  { code: "analogique", titre: "Électronique analogique",
    resume: "Composants, AOP, filtres",
    themes: ["T18", "T19", "T20"] },
  { code: "automatique", titre: "Automatique",
    resume: "Fonctions de transfert, Bode, modélisation, correcteurs",
    themes: ["T21", "T26", "T27"] },
  { code: "mesure", titre: "Mesure et acquisition",
    resume: "Thermique, capteurs, CAN/CNA, métrologie",
    themes: ["T05", "T22", "T23", "T30"] },
  { code: "numerique", titre: "Numérique et communication",
    resume: "Microcontrôleurs, transmissions, logique, GRAFCET",
    themes: ["T24", "T25", "T28", "T29"] },
];

// Types de cartes proposés au filtre. « tous » n'exclut rien.
export const TYPES = [
  { code: "tous", titre: "Toutes", pluriel: "cartes" },
  { code: "formule", titre: "Formules", pluriel: "formules" },
  { code: "piege", titre: "Pièges", pluriel: "pièges" },
  { code: "schema", titre: "Schémas", pluriel: "schémas" },
];

export function categorieParCode(code) {
  return CATEGORIES.find(c => c.code === code) || null;
}

export function typeParCode(code) {
  return TYPES.find(t => t.code === code) || TYPES[0];
}

// Prédicat de sélection : catégorie et/ou thème et/ou type. Chaque critère
// absent laisse passer tout le monde.
export function filtreCartes({ categorie = null, theme = null, type = "tous" } = {}) {
  const themes = categorie ? new Set(categorie.themes) : null;
  return c =>
    (!themes || themes.has(c.theme)) &&
    (!theme || c.theme === theme) &&
    (type === "tous" || c.type === type);
}
