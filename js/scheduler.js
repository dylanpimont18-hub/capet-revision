// Ordonnanceur SM-2 simplifié, pondéré par la fréquence d'apparition au concours.

const FACILITE_INIT = 2.4;
const FACILITE_MIN = 1.3;
const FACILITE_MAX = 2.8;
const JOUR_MS = 86400000;

// Plafond d'intervalle, en jours. Sans lui, la suite des « su » donne
// 1, 3, 8, 22, 62, 174, 487, 1364… : dès la 6e répétition la carte sort de
// l'horizon de révision (l'écrit est en mars). Avec 60 jours, une carte
// acquise revient au moins trois fois d'ici l'épreuve.
const INTERVALLE_MAX = 60;

// Places réservées aux cartes jamais vues dans chaque file quotidienne.
// Sans ce quota, les cartes échues (toujours prioritaires) saturent la file
// dès qu'il y en a 30, et la découverte du corpus s'arrête définitivement.
const QUOTA_NOUVELLES = 8;

// Au-delà de ce nombre d'échecs cumulés, la carte est « récalcitrante » :
// la répéter ne suffit plus, il faut retourner à la source (fiche, cours).
export const SEUIL_DIFFICILE = 3;

export function etatInitial() {
  return { intervalle: 0, facilite: FACILITE_INIT, repetitions: 0, du: 0, vues: 0, rates: 0 };
}

export function estDifficile(etat) {
  return !!etat && (etat.rates || 0) >= SEUIL_DIFFICILE;
}

function borner(f) {
  return Math.min(FACILITE_MAX, Math.max(FACILITE_MIN, Math.round(f * 100) / 100));
}

export function noter(etat, note, maintenant = Date.now()) {
  const e = { ...etat };
  // Compteurs cumulés (jamais remis à zéro) : ils servent au diagnostic des
  // cartes récalcitrantes, pas à la planification.
  e.vues = (e.vues || 0) + 1;
  e.rates = e.rates || 0;

  if (note === "rate") {
    e.repetitions = 0;
    e.intervalle = 0;
    e.rates += 1;
    e.facilite = borner(e.facilite - 0.2);
  } else if (note === "hesite") {
    e.repetitions += 1;
    e.intervalle = Math.max(1, Math.round(e.intervalle * 1.2));
    e.facilite = borner(e.facilite - 0.05);
  } else {
    // "su"
    if (e.repetitions === 0) e.intervalle = 1;
    else if (e.repetitions === 1) e.intervalle = 3;
    else e.intervalle = Math.min(INTERVALLE_MAX, Math.round(e.intervalle * e.facilite));
    e.repetitions += 1;
    e.facilite = borner(e.facilite + 0.1);
  }

  e.du = maintenant + e.intervalle * JOUR_MS;
  return e;
}

// Une carte à prérequis (ex. « tracer de mémoire » un schéma) n'entre dans
// la rotation qu'une fois le prérequis réussi au moins une fois : on
// reconnaît avant de reproduire. Sans prérequis, toujours disponible.
export function prerequisAcquis(c, progression) {
  if (!c.prerequis) return true;
  const p = progression[c.prerequis];
  return !!p && (p.repetitions || 0) >= 1;
}

// Entrelacement : les cartes sont choisies par poids, mais présentées en
// alternant les thèmes (tourniquet). Enchaîner trente cartes du même thème
// facilite la session et appauvrit l'apprentissage : alterner force à
// retrouver le contexte à chaque carte, ce qui est précisément l'exercice
// de l'épreuve.
export function entrelacer(cartes) {
  const groupes = new Map();
  for (const c of cartes) {
    if (!groupes.has(c.theme)) groupes.set(c.theme, []);
    groupes.get(c.theme).push(c);
  }
  const files = [...groupes.values()].sort((a, b) => b.length - a.length);
  const sortie = [];
  while (sortie.length < cartes.length) {
    for (const f of files) if (f.length) sortie.push(f.shift());
  }
  return sortie;
}

export function fileDuJour(cartes, progression, maintenant = Date.now(), taille = 30) {
  const enRetard = [];
  const nouvelles = [];

  for (const c of cartes) {
    const p = progression[c.id];
    // Un état corrompu (du = NaN/undefined — import retouché à la main, ou
    // noter() lui-même si facilite est corrompue) ne doit jamais rendre une
    // carte injoignable : ni échue ni nouvelle, elle disparaîtrait sinon
    // silencieusement et définitivement de la rotation. On la retraite
    // comme nouvelle : l'app se répare d'elle-même.
    if (!p || !Number.isFinite(p.du)) { if (prerequisAcquis(c, progression)) nouvelles.push(c); }
    else if (p.du <= maintenant) enRetard.push(c);
  }

  const parPoids = (a, b) => (b.poids || 0) - (a.poids || 0);
  enRetard.sort(parPoids);
  nouvelles.sort(parPoids);

  // Les cartes échues sont prioritaires, mais on garde des places pour les
  // cartes jamais vues : sinon, dès que 30 cartes sont échues, plus aucune
  // nouveauté n'entre et la découverte du corpus (~575 cartes) s'arrête.
  const placesRevisions = Math.max(0, taille - QUOTA_NOUVELLES);
  const retenues = enRetard.slice(0, placesRevisions);
  const neuves = nouvelles.slice(0, taille - retenues.length);

  // S'il reste de la place (peu de cartes neuves disponibles), on la rend
  // aux révisions en retard plutôt que de servir une file incomplète.
  const reste = taille - retenues.length - neuves.length;
  const complement = reste > 0 ? enRetard.slice(placesRevisions, placesRevisions + reste) : [];

  return entrelacer([...retenues, ...complement, ...neuves]);
}

/* ─── Vue d'ensemble des échéances ─────────────────────────────────────── */

function echeance(progression, c) {
  const p = progression[c.id];
  return (!p || !Number.isFinite(p.du)) ? null : p.du;
}

// Ce qui est dû maintenant, ce qui n'a jamais été vu, et la prochaine
// échéance à venir. Sert aux repères de l'écran Réviser et à l'état vide.
export function bilanEcheances(cartes, progression, maintenant = Date.now()) {
  let dues = 0, nouvelles = 0, prochaine = Infinity, duesDemain = 0;
  for (const c of cartes) {
    const du = echeance(progression, c);
    if (du === null) { if (prerequisAcquis(c, progression)) nouvelles += 1; }
    else if (du <= maintenant) dues += 1;
    else {
      prochaine = Math.min(prochaine, du);
      if (du <= maintenant + JOUR_MS) duesDemain += 1;
    }
  }
  return { dues, nouvelles, duesDemain, prochaine: Number.isFinite(prochaine) ? prochaine : null };
}

// File restreinte à un thème (depuis l'écran Priorités) : d'abord ce qui est
// dû, puis les cartes jamais vues, puis les autres par échéance croissante.
// On ne refuse jamais une carte « pas encore due » : l'utilisateur a choisi
// de travailler ce thème, l'ordonnanceur s'incline.
export function fileTheme(cartes, progression, code, maintenant = Date.now(), taille = 30) {
  const dues = [], neuves = [], autres = [];
  for (const c of cartes) {
    if (c.theme !== code) continue;
    const du = echeance(progression, c);
    if (du === null) { if (prerequisAcquis(c, progression)) neuves.push(c); }
    else if (du <= maintenant) dues.push(c);
    else autres.push(c);
  }
  const parPoids = (a, b) => (b.poids || 0) - (a.poids || 0);
  dues.sort(parPoids);
  neuves.sort(parPoids);
  autres.sort((a, b) => echeance(progression, a) - echeance(progression, b));
  return [...dues, ...neuves, ...autres].slice(0, taille);
}

// Rien n'est dû et tout a été vu : révision libre des cartes dont l'échéance
// est la plus proche. Les noter avance leur échéance normalement.
export function fileLibre(cartes, progression, maintenant = Date.now(), taille = 10) {
  const du = c => echeance(progression, c) ?? -Infinity;
  return [...cartes]
    .sort((a, b) => (du(a) - du(b)) || ((b.poids || 0) - (a.poids || 0)))
    .slice(0, taille);
}

// Les cartes récalcitrantes, les plus ratées d'abord : une session dédiée,
// à faire après être retourné à la fiche, pas à la place.
export function fileDifficiles(cartes, progression, taille = 20) {
  return cartes
    .filter(c => estDifficile(progression[c.id]))
    .sort((a, b) => (progression[b.id].rates - progression[a.id].rates) || ((b.poids || 0) - (a.poids || 0)))
    .slice(0, taille);
}
