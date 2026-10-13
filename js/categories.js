// app/js/categories.js
// Deux niveaux de regroupement des trente thèmes du corpus :
//   génie      la discipline (électrique, énergétique et fluidique, mécanique,
//              informatique et automatique) ;
//   catégorie  une famille de thèmes à l'intérieur d'un génie.
// Les thèmes sont l'unité du concours (fréquence relevée sujet par sujet) ;
// génies et catégories sont les unités de révision choisies : « ce soir,
// l'électronique de puissance », « ce week-end, tout le génie mécanique ».

export const GENIES = [
  { code: "electrique", titre: "Génie électrique",
    resume: "Circuits, conversion de puissance, machines, réseau, électronique, mesure" },
  { code: "energetique", titre: "Génie énergétique et fluidique",
    resume: "Thermique, hydraulique, éolien, photovoltaïque" },
  { code: "mecanique", titre: "Génie mécanique",
    resume: "Cinématique, dynamique, transmission de puissance" },
  { code: "informatique", titre: "Génie informatique et automatique",
    resume: "Asservissements, systèmes embarqués, réseaux, logique" },
];

export const CATEGORIES = [
  // ── Génie électrique ──
  { code: "fondamentaux", genie: "electrique", titre: "Fondamentaux électriques",
    resume: "Lois de base, puissances, complexes, harmoniques",
    themes: ["T01", "T02", "T03", "T04"] },
  { code: "puissance", genie: "electrique", titre: "Électronique de puissance",
    resume: "Hacheurs, redresseurs, onduleurs",
    themes: ["T07", "T08", "T09"] },
  { code: "machines", genie: "electrique", titre: "Machines électriques",
    resume: "Transformateur, MCC, synchrone, asynchrone, variation de vitesse",
    themes: ["T06", "T11", "T12", "T13", "T14"] },
  { code: "reseau", genie: "electrique", titre: "Réseau, stockage et sécurité",
    resume: "Batteries, distribution, régimes de neutre",
    themes: ["T15", "T17"] },
  { code: "analogique", genie: "electrique", titre: "Électronique analogique",
    resume: "Composants, AOP, filtres",
    themes: ["T18", "T19", "T20"] },
  { code: "mesure", genie: "electrique", titre: "Mesure et acquisition",
    resume: "Capteurs, CAN/CNA, métrologie",
    themes: ["T22", "T23", "T30"] },
  // ── Génie énergétique et fluidique ──
  { code: "thermique", genie: "energetique", titre: "Phénomènes thermiques",
    resume: "Conduction, convection, résistances thermiques, capteurs de température",
    themes: ["T05"] },
  { code: "renouvelables", genie: "energetique", titre: "Énergies renouvelables et hydraulique",
    resume: "Photovoltaïque, retenue d'eau, STEP, éolien",
    themes: ["T16"] },
  // ── Génie mécanique ──
  { code: "mecanique", genie: "mecanique", titre: "Mécanique et transmission",
    resume: "Cinématique, dynamique, inerties, réducteurs, rendements",
    themes: ["T10"] },
  // ── Génie informatique et automatique ──
  { code: "automatique", genie: "informatique", titre: "Automatique",
    resume: "Fonctions de transfert, Bode, modélisation, correcteurs",
    themes: ["T21", "T26", "T27"] },
  { code: "numerique", genie: "informatique", titre: "Numérique et communication",
    resume: "Microcontrôleurs, transmissions, logique, GRAFCET",
    themes: ["T24", "T25", "T28", "T29"] },
];

// Types de cartes proposés au filtre. « tous » n'exclut rien.
export const TYPES = [
  { code: "tous", titre: "Toutes", pluriel: "cartes" },
  { code: "formule", titre: "Formules", pluriel: "formules" },
  { code: "piege", titre: "Pièges", pluriel: "pièges" },
  { code: "schema", titre: "Schémas", pluriel: "schémas" },
  { code: "exercice", titre: "Sujets", pluriel: "extraits de sujets" },
];

export function genieParCode(code) {
  return GENIES.find(g => g.code === code) || null;
}

export function categorieParCode(code) {
  return CATEGORIES.find(c => c.code === code) || null;
}

export function categoriesDuGenie(genie) {
  return CATEGORIES.filter(c => c.genie === genie.code);
}

export function themesDuGenie(genie) {
  return categoriesDuGenie(genie).flatMap(c => c.themes);
}

export function typeParCode(code) {
  return TYPES.find(t => t.code === code) || TYPES[0];
}

// Prédicat de sélection : génie et/ou catégorie et/ou thème et/ou type.
// Chaque critère absent laisse passer tout le monde.
export function filtreCartes({ genie = null, categorie = null, theme = null, type = "tous" } = {}) {
  const themesG = genie ? new Set(themesDuGenie(genie)) : null;
  const themesC = categorie ? new Set(categorie.themes) : null;
  return c =>
    (!themesG || themesG.has(c.theme)) &&
    (!themesC || themesC.has(c.theme)) &&
    (!theme || c.theme === theme) &&
    // « tous » désigne les cartes de révision ; les extraits d'épreuves, plus
    // longs, ne s'invitent que sur demande explicite.
    (type === "tous" ? c.type !== "exercice" : c.type === type);
}
