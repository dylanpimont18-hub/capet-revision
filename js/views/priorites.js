// app/js/views/priorites.js
import { charger } from "../store.js";
import { echapper } from "../card-render.js";
import { pluriel } from "../texte.js";
import { estDifficile } from "../scheduler.js";

const SEUIL_REPET = 2;
// 2,3 et non 2,4 : la facilité initiale VAUT 2,4, donc un unique « hésité »
// (−0,05) la fait tomber à 2,35 et la carte n'est plus comptée acquise,
// même après deux réussites. Le seuil doit être strictement sous l'initiale.
const SEUIL_FACILITE = 2.3;

export function calculerMaitrise(cartes, progression, maintenant = Date.now()) {
  const par = new Map();
  for (const c of cartes) {
    if (!par.has(c.theme)) par.set(c.theme, { vues: 0, acquises: 0, total: 0, dues: 0, difficiles: 0 });
    const e = par.get(c.theme);
    e.total += 1;
    const p = progression[c.id];
    if (p) {
      e.vues += 1;
      if (p.repetitions >= SEUIL_REPET && p.facilite >= SEUIL_FACILITE) e.acquises += 1;
      if (Number.isFinite(p.du) && p.du <= maintenant) e.dues += 1;
      if (estDifficile(p)) e.difficiles += 1;
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
      const m = maitrises.get(t.code) || { maitrise: 0, vues: 0, total: 0, dues: 0, acquises: 0, difficiles: 0 };
      return { ...t, ...m, urgence: (t.poids || 0) * (1 - m.maitrise) };
    })
    .sort((a, b) => b.urgence - a.urgence);
}

// La couleur ne doit jamais porter seule l'information : chaque pastille
// est doublée d'un libellé lisible, y compris par un lecteur d'écran.
// Un thème jamais ouvert n'est ni « prioritaire » ni « acquis » : il est
// simplement non commencé, et le dire évite un tableau tout rouge le premier jour.
export function niveau(t) {
  if (!t.vues) return { mot: "Non commencé", classe: "n-neutre" };
  if (t.urgence >= 0.5) return { mot: "Prioritaire", classe: "n-rate" };
  if (t.urgence >= 0.25) return { mot: "À revoir", classe: "n-hesite" };
  return { mot: "Acquis", classe: "n-su" };
}

export function vuePriorites(racine, data) {
  const m = calculerMaitrise(data.cards, charger());
  const themes = ordonnerThemes(data.themes, m);

  // Chaque ligne est un lien vers une session sur ce thème : un diagnostic
  // qu'on ne peut pas transformer en action n'est qu'un reproche.
  const lignes = themes.map(t => {
    const n = niveau(t);
    const pct = Math.round(t.maitrise * 100);
    const meta = [
      echapper(t.code),
      `${t.presence_n}/${t.presence_sur} sujets`,
      t.vues ? `${t.vues}/${t.total} vues` : pluriel(t.total, "carte"),
      t.dues ? `<strong>${pluriel(t.dues, "due")}</strong>` : "",
      t.difficiles ? `<em>${pluriel(t.difficiles, "difficile")}</em>` : "",
    ].filter(Boolean).join(" · ");
    const maitrise = t.vues
      ? `<span class="pct">${pct}&nbsp;%</span>
         <span class="barre-maitrise" aria-hidden="true"><i style="width:${pct}%"></i></span>`
      : `<span class="pct neutre" aria-label="Maîtrise non mesurée">—</span>`;
    return `
    <li>
      <a class="ligne-theme" href="#/reviser?theme=${encodeURIComponent(t.code)}">
        <span class="pastille ${n.classe}" role="img" aria-label="${n.mot}"></span>
        <span class="corps">
          <span class="theme">${echapper(t.titre)}</span>
          <span class="meta">${meta}</span>
        </span>
        <span class="maitrise">${maitrise}</span>
        <svg class="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor"
             stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="m9 6 6 6-6 6"/>
        </svg>
      </a>
    </li>`;
  }).join("");

  const commences = themes.filter(t => t.vues > 0);
  const prioritaires = commences.filter(t => t.urgence >= 0.5).length;
  const titre = commences.length === 0
    ? `${pluriel(themes.length, "thème")} à découvrir`
    : `${pluriel(prioritaires, "thème")} à travailler`;
  const sousTitre = commences.length === 0
    ? "Classés par fréquence au concours. Touchez un thème pour le réviser directement."
    : "Fréquence au concours croisée avec votre maîtrise. Les premiers tombent souvent et sont mal maîtrisés. Touchez un thème pour le réviser.";

  const nbDifficiles = themes.reduce((n, t) => n + t.difficiles, 0);
  const lienDifficiles = nbDifficiles
    ? `<a class="lien-difficiles" href="#/reviser?mode=difficiles">
         ${pluriel(nbDifficiles, "carte difficile", "cartes difficiles")} à reprendre
         <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 6 6 6-6 6"/></svg>
       </a>` : "";

  racine.innerHTML = `
    <div class="carte carte-liste">
      <p class="consigne">Priorités</p>
      <p class="vedette">${titre}</p>
      <p class="sous-titre">${sousTitre}</p>
      ${lienDifficiles}
      <ol class="liste-themes" aria-label="Thèmes classés par urgence décroissante">${lignes}</ol>
    </div>`;
}
