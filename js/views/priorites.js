// app/js/views/priorites.js
import { charger } from "../store.js";
import { echapper } from "../card-render.js";

const SEUIL_REPET = 2;
// 2,3 et non 2,4 : la facilité initiale VAUT 2,4, donc un unique « hésité »
// (−0,05) la fait tomber à 2,35 et la carte n'est plus comptée acquise,
// même après deux réussites. Le seuil doit être strictement sous l'initiale.
const SEUIL_FACILITE = 2.3;

export function calculerMaitrise(cartes, progression) {
  const par = new Map();
  for (const c of cartes) {
    if (!par.has(c.theme)) par.set(c.theme, { vues: 0, acquises: 0, total: 0 });
    const e = par.get(c.theme);
    e.total += 1;
    const p = progression[c.id];
    if (p) {
      e.vues += 1;
      if (p.repetitions >= SEUIL_REPET && p.facilite >= SEUIL_FACILITE) e.acquises += 1;
    }
  }
  for (const e of par.values()) {
    e.maitrise = e.total ? e.acquises / e.total : 0;
  }
  return par;
}

export function ordonnerThemes(themes, maitrises) {
  return themes
    .map(t => {
      const m = maitrises.get(t.code) || { maitrise: 0, vues: 0, total: 0 };
      return { ...t, ...m, urgence: (t.poids || 0) * (1 - m.maitrise) };
    })
    .sort((a, b) => b.urgence - a.urgence);
}

function couleur(u) {
  if (u >= 0.5) return "var(--rate)";
  if (u >= 0.25) return "var(--hesite)";
  return "var(--su)";
}

export function vuePriorites(racine, data) {
  const m = calculerMaitrise(data.cards, charger());
  const lignes = ordonnerThemes(data.themes, m).map(t => `
    <tr>
      <td><span class="pastille" style="background:${couleur(t.urgence)}"></span></td>
      <td>${echapper(t.code)}</td>
      <td>${echapper(t.titre)}</td>
      <td>${t.presence_n}/${t.presence_sur}</td>
      <td>${Math.round(t.maitrise * 100)} %</td>
      <td>${t.vues}/${t.total}</td>
    </tr>`).join("");

  racine.innerHTML = `
    <div class="carte">
      <p class="vedette">Priorités</p>
      <p class="consigne">Croisement fréquence au concours × maîtrise.
        En rouge : tombe souvent, mal maîtrisé.</p>
      <table class="grille">
        <thead><tr><th></th><th>Code</th><th>Thème</th>
          <th>Sujets</th><th>Maîtrise</th><th>Vues</th></tr></thead>
        <tbody>${lignes}</tbody>
      </table>
    </div>`;
}
