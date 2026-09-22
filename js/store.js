// app/js/store.js
// Persistance de la progression. Aucun serveur : l'export JSON est le seul backup.

export const CLE = "capet.progression.v1";

export function charger() {
  try {
    const brut = localStorage.getItem(CLE);
    return brut ? JSON.parse(brut) : {};
  } catch {
    return {};
  }
}

// Navigation privée Safari (quota à 0) ou quota dépassé : setItem lève.
// Ne jamais avaler l'échec en silence — l'appelant doit pouvoir prévenir
// l'utilisateur, sans quoi une session de révision se perd sans message
// (voir reviser.js). true/false plutôt qu'une exception : le flux normal
// de noter()/majCarte() ne doit pas devenir un try/catch à chaque appel.
export function sauver(progression) {
  try {
    localStorage.setItem(CLE, JSON.stringify(progression));
    return true;
  } catch {
    return false;
  }
}

export function majCarte(id, etat) {
  const p = charger();
  p[id] = etat;
  return sauver(p);
}

export function reinitialiser() {
  localStorage.removeItem(CLE);
}

export function exporter() {
  return JSON.stringify(
    { version: 1, exporte_le: new Date().toISOString(), progression: charger() },
    null, 1
  );
}

export function importer(texte) {
  let data;
  try {
    data = JSON.parse(texte);
  } catch {
    return false;
  }
  if (!data || typeof data !== "object") return false;
  if (!data.progression || typeof data.progression !== "object") return false;
  sauver(data.progression);
  return true;
}
