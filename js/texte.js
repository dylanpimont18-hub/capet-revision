// app/js/texte.js
// Petits utilitaires de formulation. Regroupés ici pour que chaque vue cesse
// d'écrire « carte(s) » : un pluriel entre parenthèses est une interface qui
// avoue ne pas savoir compter.

// En français, 0 et 1 restent au singulier : « 0 carte », « 1 carte », « 2 cartes ».
export function pluriel(n, un, plusieurs = un + "s") {
  return `${n} ${n > 1 ? plusieurs : un}`;
}

// Intervalle de répétition, tel qu'affiché sous les boutons de notation.
export function formaterJours(n) {
  if (!Number.isFinite(n) || n <= 0) return "aujourd'hui";
  if (n === 1) return "demain";
  return `${n} j`;
}

// Date locale au format AAAA-MM-JJ. Pas toISOString() : à 1 h du matin à Paris,
// l'UTC est encore la veille, et la série de jours consécutifs se casserait.
export function dateISO(ts = Date.now()) {
  const d = new Date(ts);
  const p = n => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`;
}

const FORMAT_COURT = new Intl.DateTimeFormat("fr-FR", { weekday: "short", day: "numeric", month: "short" });

// « demain », « jeu. 16 oct. » : relatif quand c'est proche, daté sinon.
export function formaterEcheance(ts, maintenant = Date.now()) {
  const aujourdhui = dateISO(maintenant);
  const cible = dateISO(ts);
  if (cible <= aujourdhui) return "aujourd'hui";
  if (cible === dateISO(maintenant + 86400000)) return "demain";
  return FORMAT_COURT.format(new Date(ts));
}
