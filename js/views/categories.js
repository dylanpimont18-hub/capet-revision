// app/js/views/categories.js
// Choisir quoi réviser : un génie, une famille de thèmes, un thème, un type
// de carte. L'écran Réviser décide pour vous (la file du jour) ; celui-ci
// vous laisse décider. Les deux se rejoignent : une carte notée ici est
// planifiée comme les autres.
import { charger, chargerPrefs, majPrefs } from "../store.js";
import { GENIES, TYPES, categoriesDuGenie, filtreCartes } from "../categories.js";
import { compterFiltre } from "../scheduler.js";
import { echapper } from "../card-render.js";
import { pluriel } from "../texte.js";
import { chargerIndexCours, chapitresDisponibles, premierChapitre } from "./cours.js";

// Icône du cours : un livre ouvert, la même partout où l'on mène au cours.
const LIVRE = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"
  stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <path d="M12 6.5C10.3 5.2 7.8 4.6 4 4.8v13c3.8-.2 6.3.4 8 1.7 1.7-1.3 4.2-1.9 8-1.7v-13c-3.8-.2-6.3.4-8 1.7Z"/>
  <path d="M12 6.5v13"/></svg>`;

export async function vueCategories(racine, data) {
  // Le cours ne couvre pas tous les thèmes : un bouton « Lire le cours »
  // n'apparaît que là où un chapitre est rédigé.
  const cours = await chargerIndexCours();
  const chapitres = chapitresDisponibles(cours);
  const avecCours = new Set(chapitres.map(c => c.theme));
  const progression = charger();
  const prefs = chargerPrefs();
  const type = TYPES.some(t => t.code === prefs.typeChoisi) ? prefs.typeChoisi : "tous";
  const titreTheme = Object.fromEntries(data.themes.map(t => [t.code, t.titre]));
  const nomType = TYPES.find(t => t.code === type).pluriel;
  const nombre = (n) => pluriel(n, nomType.replace(/s$/, ""), nomType);

  const requete = (params) => {
    const q = new URLSearchParams(params);
    if (type !== "tous") q.set("type", type);
    return `#/reviser?${q}`;
  };

  // Barre de choix du type : un contrôle segmenté, mémorisé.
  const segments = TYPES.map(t => `
    <button type="button" class="segment${t.code === type ? " actif" : ""}"
            data-type="${t.code}" aria-pressed="${t.code === type}">${t.titre}</button>`).join("");

  const etat = (n) => {
    const pct = n.vues ? Math.round(100 * n.acquises / n.total) : null;
    return `${nombre(n.total)}${n.dues ? ` · <strong>${pluriel(n.dues, "due")}</strong>` : ""}${pct !== null ? ` · ${pct}&nbsp;% acquis` : ""}`;
  };

  const global = compterFiltre(data.cards, progression, filtreCartes({ type }));

  const blocs = GENIES.map(genie => {
    const ng = compterFiltre(data.cards, progression, filtreCartes({ genie, type }));
    if (ng.total === 0) return "";
    const categories = categoriesDuGenie(genie).map(cat => {
      const n = compterFiltre(data.cards, progression, filtreCartes({ categorie: cat, type }));
      if (n.total === 0) return "";
      const chips = cat.themes.map(code => {
        const nt = compterFiltre(data.cards, progression, filtreCartes({ theme: code, type }));
        if (nt.total === 0) return "";
        const puce = `<a class="chip" href="${requete({ theme: code })}">
                  <span class="chip-code">${code}</span>${echapper(titreTheme[code] || code)}
                  ${nt.dues ? `<b>${nt.dues}</b>` : ""}</a>`;
        if (!avecCours.has(code)) return puce;
        // Puce double : réviser les cartes du thème, ou lire son chapitre.
        return `<span class="chip-groupe">${puce}<a class="chip-cours" href="#/cours?theme=${code}"
                  aria-label="Lire le cours ${code} : ${echapper(titreTheme[code] || code)}">${LIVRE}Cours</a></span>`;
      }).join("");
      const premier = premierChapitre(cours, cat);
      const nbChap = cat.themes.filter(t => avecCours.has(t)).length;
      const lienCours = premier ? `
          <a class="lien-cours" href="#/cours?theme=${premier.theme}">${LIVRE}
            <span>Lire le cours</span>
            <span class="meta">${pluriel(nbChap, "chapitre")}</span></a>` : "";
      return `
        <section class="carte categorie" aria-labelledby="cat-${cat.code}">
          <a class="tete-categorie" href="${requete({ cat: cat.code })}">
            <span class="corps">
              <span class="vedette-cat" id="cat-${cat.code}">${echapper(cat.titre)}</span>
              <span class="meta">${etat(n)}</span>
            </span>
            <svg class="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                 stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 6 6 6-6 6"/></svg>
          </a>
          <div class="chips">${chips}</div>${lienCours}
        </section>`;
    }).join("");
    // L'en-tête de génie est lui-même un départ de session : tout le génie.
    return `
      <section class="genie" aria-labelledby="genie-${genie.code}">
        <a class="tete-genie" href="${requete({ genie: genie.code })}">
          <span class="corps">
            <span class="consigne" id="genie-${genie.code}">${echapper(genie.titre)}</span>
            <span class="meta">${echapper(genie.resume)}</span>
            <span class="meta chiffres">${etat(ng)}</span>
          </span>
          <span class="action">Tout réviser
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                 stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 6 6 6-6 6"/></svg>
          </span>
        </a>
        ${categories}
      </section>`;
  }).join("");

  racine.innerHTML = `
    <div class="carte">
      <p class="consigne">Catégories</p>
      <p class="vedette">Choisir quoi réviser</p>
      <p class="texte-doux">Un génie, une famille de thèmes, un thème, un type de carte. La session
        mélange ce qui est dû, ce qui est nouveau, puis le reste ; les notes comptent comme dans
        la file du jour.</p>
      <div class="segments" role="group" aria-label="Type de cartes">${segments}</div>
      <a class="bouton-secondaire" href="${requete({ cat: "toutes" })}"
         style="margin-top:var(--e3)">Tout le programme · ${nombre(global.total)}${global.dues ? ` · ${pluriel(global.dues, "due")}` : ""}</a>
      ${chapitres.length ? `<a class="bouton-secondaire bouton-cours" href="#/cours"
         style="margin-top:var(--e2)">${LIVRE}<span>Le cours · ${pluriel(chapitres.length, "chapitre")}</span></a>` : ""}
    </div>
    ${blocs}`;

  racine.querySelectorAll(".segment").forEach(b => {
    b.onclick = () => {
      majPrefs({ typeChoisi: b.dataset.type });
      vueCategories(racine, data);
    };
  });
}
