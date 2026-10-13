// app/js/views/sujets.js
// Extraits d'épreuves : un exercice court par carte, avec schéma, données,
// question isolée et corrigé. Rédigés dans l'esprit des sujets, session par
// session ; l'avertissement du fichier le rappelle à l'écran.
import { charger } from "../store.js";
import { echapper } from "../card-render.js";
import { pluriel } from "../texte.js";
import { estDifficile } from "../scheduler.js";

export function vueSujets(racine, data) {
  const progression = charger();
  const exercices = data.cards.filter(c => c.type === "exercice");
  const annees = [...new Set(exercices.map(e => e.annee))].sort((a, b) => b - a);

  const etat = (e) => {
    const p = progression[e.id];
    if (!p) return `<span class="etat neutre">À faire</span>`;
    if (estDifficile(p)) return `<span class="etat rate">Ratée ${p.rates} fois</span>`;
    if (p.repetitions >= 1) return `<span class="etat su">Réussie</span>`;
    return `<span class="etat hesite">À refaire</span>`;
  };

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
            <span class="vedette-cat" id="s-${annee}">Session ${annee}</span>
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
    <div class="carte">
      <p class="consigne">Sujets</p>
      <p class="vedette">Extraits d'épreuves</p>
      <p class="texte-doux">${pluriel(exercices.length, "exercice")} courts, chacun avec son schéma, ses données et une
        question isolée, comme un extrait d'épreuve écrite. Révélez le corrigé, puis notez-vous sur la
        méthode et le résultat.</p>
      <p class="avertissement">${echapper(data.avertissementExercices || "")}</p>
      <a class="bouton-secondaire" href="#/reviser?type=exercice" style="margin-top:var(--e3)">Tous les extraits, toutes sessions</a>
    </div>
    ${sections}`;
}
