// app/js/views/sujets.js
// Deux usages. « Épreuves officielles » : les sujets complets, lisibles pas à
// pas (vueEpreuve). « Entraînement » : vingt extraits rédigés, un exercice par
// carte, pour la pratique au rappel actif.
import { charger } from "../store.js";
import { echapper, ouvrirPleinEcran, rendreMathsDans } from "../card-render.js";
import { pluriel } from "../texte.js";
import { estDifficile } from "../scheduler.js";

let INDEX = null;

// Index des épreuves, chargé une fois. Hors ligne sans cache, la liste reste
// vide plutôt que de casser l'écran.
export async function chargerIndexSujets() {
  if (!INDEX) {
    try {
      const r = await fetch("sujets/index.json");
      INDEX = r.ok ? (await r.json()).epreuves : [];
    } catch {
      INDEX = [];
    }
  }
  return INDEX;
}

export async function vueSujets(racine, data) {
  const progression = charger();
  const exercices = data.cards.filter(c => c.type === "exercice");
  const epreuves = await chargerIndexSujets();

  const officielles = epreuves.length ? `
    <section class="carte carte-liste" aria-labelledby="off">
      <p class="consigne" id="off">Épreuves officielles</p>
      <p class="texte-doux">${pluriel(epreuves.length, "épreuve")} écrites, de 2015 à 2025, en texte intégral
        avec les figures. Un sommaire par épreuve, et une navigation de session en session.</p>
      <ol class="liste-themes">${epreuves.map(e => `
        <li>
          <a class="ligne-sujet" href="#/epreuve?id=${encodeURIComponent(e.id)}">
            <span class="corps">
              <span class="theme">${e.annee} · ${echapper(e.libelle)}</span>
              <span class="meta">${echapper(e.titre)}</span>
            </span>
            <svg class="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                 stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 6 6 6-6 6"/></svg>
          </a>
        </li>`).join("")}
      </ol>
    </section>` : `
    <section class="carte"><p class="consigne">Épreuves officielles</p>
      <p class="texte-doux">Les textes des épreuves ne sont pas encore disponibles hors ligne.
        Ouvrez cet écran une fois en ligne pour les mettre en cache.</p></section>`;

  const etat = (e) => {
    const p = progression[e.id];
    if (!p) return `<span class="etat neutre">À faire</span>`;
    if (estDifficile(p)) return `<span class="etat rate">Ratée ${p.rates} fois</span>`;
    if (p.repetitions >= 1) return `<span class="etat su">Réussie</span>`;
    return `<span class="etat hesite">À refaire</span>`;
  };

  const annees = [...new Set(exercices.map(e => e.annee))].sort((a, b) => b - a);
  const sections = annees.map(annee => {
    const liste = exercices.filter(e => e.annee === annee);
    const faits = liste.filter(e => progression[e.id]).length;
    const lignes = liste.map(e => `
      <li>
        <a class="ligne-sujet" href="#/reviser?sujet=${encodeURIComponent(e.id)}">
          <span class="corps">
            <span class="theme">${echapper(e.titre)}</span>
            <span class="meta">${echapper(e.systeme)} · ${echapper(e.epreuve)}</span>
          </span>
          ${etat(e)}
          <svg class="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
               stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 6 6 6-6 6"/></svg>
        </a>
      </li>`).join("");
    return `
      <section class="carte carte-liste" aria-labelledby="s-${annee}">
        <a class="tete-session" href="#/reviser?annee=${annee}">
          <span class="corps">
            <span class="vedette-cat" id="s-${annee}">Entraînement ${annee}</span>
            <span class="meta">${pluriel(liste.length, "extrait")} · ${faits}/${liste.length} ${faits > 1 ? "faits" : "fait"}</span>
          </span>
          <span class="action">Enchaîner
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                 stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 6 6 6-6 6"/></svg>
          </span>
        </a>
        <ol class="liste-themes">${lignes}</ol>
      </section>`;
  }).join("");

  racine.innerHTML = `
    ${officielles}
    <div class="carte">
      <p class="consigne">Entraînement</p>
      <p class="texte-doux">${pluriel(exercices.length, "extrait")} rédigés, chacun avec son schéma, ses
        données et une question isolée. Révélez le corrigé, puis notez-vous sur la méthode et le résultat.</p>
      <p class="avertissement">${echapper(data.avertissementExercices || "")}</p>
      <a class="bouton-secondaire" href="#/reviser?type=exercice" style="margin-top:var(--e3)">Tous les extraits, toutes sessions</a>
    </div>
    ${sections}`;
}

// Lecture d'une épreuve officielle : en-tête, sommaire replié, texte intégral
// (figures agrandissables, formules KaTeX), navigation vers les épreuves voisines.
export async function vueEpreuve(racine, data, ctx = {}) {
  const id = (ctx.params && ctx.params.get("id")) || "";
  const epreuves = await chargerIndexSujets();
  const i = epreuves.findIndex(e => e.id === id);
  if (i < 0) {
    racine.innerHTML = `<div class="carte"><p class="vedette">Épreuve introuvable</p>
      <a class="bouton-secondaire" href="#/sujets">Retour aux sujets</a></div>`;
    return;
  }
  const e = epreuves[i];
  // L'index est trié du plus récent au plus ancien : « suivante » dans le temps
  // est l'entrée précédente du tableau.
  const plusRecente = epreuves[i - 1];
  const plusAncienne = epreuves[i + 1];
  const lien = (x, sens) => x
    ? `<a class="bouton-secondaire" href="#/epreuve?id=${encodeURIComponent(x.id)}">${sens} ${x.annee} · ${echapper(x.libelle)}</a>`
    : `<span></span>`;

  racine.innerHTML = `
    <div class="carte entete-epreuve">
      <p class="consigne">Session ${e.annee} · ${echapper(e.libelle)}</p>
      <p class="vedette">${echapper(e.titre)}</p>
      ${e.sommaire.length ? `
      <details class="sommaire-epreuve">
        <summary>Sommaire · ${e.sommaire.length} rubriques</summary>
        <ol>${e.sommaire.map(s => `<li class="niv${s.niveau}"><a href="#" data-cible="${s.id}">${echapper(s.texte)}</a></li>`).join("")}</ol>
      </details>` : ""}
    </div>
    <article class="texte-epreuve" id="corps-epreuve" aria-label="Texte de l'épreuve">
      <p class="texte-doux">Chargement du texte…</p>
    </article>
    <nav class="pagination-epreuve" aria-label="Autres épreuves">
      ${lien(plusAncienne, "←")}
      <a class="bouton-secondaire" href="#/sujets">Toutes les épreuves</a>
      ${lien(plusRecente, "→")}
    </nav>`;

  const article = document.getElementById("corps-epreuve");
  let corps;
  try {
    const r = await fetch(`sujets/textes/${e.id}.html`);
    if (!r.ok) throw new Error(r.status);
    corps = await r.text();
  } catch {
    article.innerHTML = `<p class="avertissement">Le texte de cette épreuve n'est pas disponible hors ligne.
      Ouvrez-le une fois en ligne pour le mettre en cache.</p>`;
    return;
  }
  article.innerHTML = corps;

  // Tableaux trop larges : défilement dans leur seul cadre, jamais sur la page.
  article.querySelectorAll("table").forEach(t => {
    const cadre = document.createElement("div");
    cadre.className = "table-scroll";
    t.parentNode.insertBefore(cadre, t);
    cadre.appendChild(t);
  });
  rendreMathsDans(article);

  // Toucher une figure l'agrandit ; les figures absentes restent expliquées.
  article.addEventListener("click", (ev) => {
    if (ev.target.tagName === "IMG") ouvrirPleinEcran(ev.target.cloneNode(true), "Pincez pour zoomer · touchez pour fermer");
  });

  // Sommaire : défilement interne, sans toucher au fragment de l'URL (qui
  // est la route du routeur).
  racine.querySelectorAll(".sommaire-epreuve a").forEach(a => {
    a.onclick = (ev) => {
      ev.preventDefault();
      const cible = document.getElementById(a.dataset.cible);
      if (cible) cible.scrollIntoView({ behavior: "smooth", block: "start" });
      a.closest("details").open = false;
    };
  });
}
