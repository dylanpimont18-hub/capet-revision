// app/js/store.js
// Persistance locale. Aucun serveur : l'export JSON est le seul backup.
// Quatre clés : la progression SM-2 (le trésor), le journal d'activité
// (série de jours), la date de l'écrit, et quelques préférences d'interface.

import { dateISO } from "./texte.js";

export const CLE = "capet.progression.v1";
export const CLE_ACTIVITE = "capet.activite.v1";
export const CLE_DATE_ECRIT = "capet.date_ecrit";
export const CLE_PREFS = "capet.prefs.v1";

function lireJSON(cle, defaut) {
  try {
    const brut = localStorage.getItem(cle);
    const val = brut ? JSON.parse(brut) : null;
    return val && typeof val === "object" ? val : defaut;
  } catch {
    return defaut;
  }
}

// Navigation privée Safari (quota à 0) ou quota dépassé : setItem lève.
// Ne jamais avaler l'échec en silence — l'appelant doit pouvoir prévenir
// l'utilisateur, sans quoi une session de révision se perd sans message
// (voir reviser.js). true/false plutôt qu'une exception : le flux normal
// de noter()/majCarte() ne doit pas devenir un try/catch à chaque appel.
function ecrireJSON(cle, val) {
  try {
    localStorage.setItem(cle, JSON.stringify(val));
    return true;
  } catch {
    return false;
  }
}

/* ─── Progression ──────────────────────────────────────────────────────── */

export function charger() {
  return lireJSON(CLE, {});
}

export function sauver(progression) {
  return ecrireJSON(CLE, progression);
}

export function majCarte(id, etat) {
  const p = charger();
  p[id] = etat;
  return sauver(p);
}

// Annulation d'une première notation : la carte redevient « jamais vue ».
export function retirerCarte(id) {
  const p = charger();
  delete p[id];
  return sauver(p);
}

/* ─── Activité : un compteur par jour et par note ──────────────────────── */

export function chargerActivite() {
  const a = lireJSON(CLE_ACTIVITE, { jours: {} });
  if (!a.jours || typeof a.jours !== "object") a.jours = {};
  return a;
}

export function enregistrerNotation(note, maintenant = Date.now()) {
  const a = chargerActivite();
  const j = dateISO(maintenant);
  const jour = a.jours[j] || (a.jours[j] = { su: 0, hesite: 0, rate: 0 });
  jour[note] = (jour[note] || 0) + 1;
  return ecrireJSON(CLE_ACTIVITE, a);
}

export function annulerNotation(note, maintenant = Date.now()) {
  const a = chargerActivite();
  const j = dateISO(maintenant);
  const jour = a.jours[j];
  if (!jour) return true;
  jour[note] = Math.max(0, (jour[note] || 0) - 1);
  if (!jour.su && !jour.hesite && !jour.rate) delete a.jours[j];
  return ecrireJSON(CLE_ACTIVITE, a);
}

// Jours consécutifs avec au moins une notation. Une journée sans révision
// n'est « perdue » qu'une fois passée : si rien n'a été fait aujourd'hui,
// on compte à partir d'hier, la série est encore rattrapable.
export function calculerSerie(activite, maintenant = Date.now()) {
  const jours = (activite && activite.jours) || {};
  const d = new Date(maintenant);
  d.setHours(12, 0, 0, 0);
  if (!jours[dateISO(d)]) d.setDate(d.getDate() - 1);
  let serie = 0;
  while (jours[dateISO(d)]) {
    serie += 1;
    d.setDate(d.getDate() - 1);
  }
  return serie;
}

/* ─── Date de l'écrit ──────────────────────────────────────────────────── */

export function lireDateEcrit() {
  try {
    const v = localStorage.getItem(CLE_DATE_ECRIT);
    return v && /^\d{4}-\d{2}-\d{2}$/.test(v) ? v : null;
  } catch {
    return null;
  }
}

export function ecrireDateEcrit(iso) {
  try {
    if (iso) localStorage.setItem(CLE_DATE_ECRIT, iso);
    else localStorage.removeItem(CLE_DATE_ECRIT);
    return true;
  } catch {
    return false;
  }
}

// Nombre de jours calendaires avant la date (négatif si passée).
export function joursAvant(iso, maintenant = Date.now()) {
  if (!iso) return null;
  const [a, m, j] = iso.split("-").map(Number);
  const cible = new Date(a, m - 1, j, 12);
  const auj = new Date(maintenant);
  auj.setHours(12, 0, 0, 0);
  return Math.round((cible - auj) / 86400000);
}

/* ─── Préférences d'interface ──────────────────────────────────────────── */

export function chargerPrefs() {
  return lireJSON(CLE_PREFS, {});
}

export function majPrefs(patch) {
  return ecrireJSON(CLE_PREFS, { ...chargerPrefs(), ...patch });
}

/* ─── Sauvegarde complète ──────────────────────────────────────────────── */

export function reinitialiser() {
  localStorage.removeItem(CLE);
  localStorage.removeItem(CLE_ACTIVITE);
}

export function exporter() {
  return JSON.stringify(
    {
      version: 2,
      exporte_le: new Date().toISOString(),
      progression: charger(),
      activite: chargerActivite(),
      date_ecrit: lireDateEcrit(),
    },
    null, 1
  );
}

// Accepte les exports v1 (progression seule) comme v2.
export function importer(texte) {
  let data;
  try {
    data = JSON.parse(texte);
  } catch {
    return false;
  }
  if (!data || typeof data !== "object") return false;
  if (!data.progression || typeof data.progression !== "object") return false;
  if (!sauver(data.progression)) return false;
  if (data.activite && typeof data.activite === "object") ecrireJSON(CLE_ACTIVITE, data.activite);
  if (typeof data.date_ecrit === "string") ecrireDateEcrit(data.date_ecrit);
  return true;
}
