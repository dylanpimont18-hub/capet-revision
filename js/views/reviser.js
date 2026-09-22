// app/js/views/reviser.js
import { fileDuJour, noter, etatInitial } from "../scheduler.js";
import { charger, majCarte } from "../store.js";
import { rendreRecto, rendreVerso } from "../card-render.js";

const TAILLE_FILE = 30;
const JOUR_MS_VUE = 86400000;

export function vueReviser(racine, data) {
  const progression = charger();
  const file = fileDuJour(data.cards, progression, Date.now(), TAILLE_FILE);

  if (file.length === 0) {
    racine.innerHTML = `<div class="carte">
      <p class="vedette">Rien à réviser pour l'instant.</p>
      <p class="consigne">Toutes les cartes échues ont été vues. Revenez demain.</p>
    </div>`;
    return;
  }

  let i = 0;
  let notees = 0;
  const total = file.length;          // figé : les reprises ne le gonflent pas
  const reprises = new Set();         // cartes ratées, rejouées en fin de file

  function afficher() {
    if (i >= file.length) {
      racine.innerHTML = `<div class="carte">
        <p class="vedette">Session terminée</p>
        <p class="consigne">${notees} carte(s) révisée(s).</p>
      </div>`;
      return;
    }
    const c = file[i];
    const restantes = Math.max(0, file.length - i);
    racine.innerHTML = `
      <p class="progression-file">${Math.min(i + 1, total)} / ${total}${
        restantes > total - i ? " (+ reprises)" : ""}</p>
      <div class="carte">${rendreRecto(c)}</div>
      <div id="verso" hidden></div>
      <div id="commandes"><button class="revelateur" id="reveler">Révéler</button></div>`;

    document.getElementById("reveler").onclick = () => {
      const v = document.getElementById("verso");
      v.innerHTML = `<div class="carte">${rendreVerso(c)}</div>`;
      v.hidden = false;
      document.getElementById("commandes").innerHTML = `
        <div class="actions">
          <button class="b-rate"   data-n="rate">Raté</button>
          <button class="b-hesite" data-n="hesite">Hésité</button>
          <button class="b-su"     data-n="su">Su</button>
        </div>`;
      document.querySelectorAll("[data-n]").forEach(b => {
        b.onclick = () => {
          const note = b.dataset.n;
          const estReprise = reprises.has(c.id);
          let enregistre = true;  // sauver() peut échouer (quota, navigation privée)

          if (estReprise) {
            // Deuxième passage dans la même session : la carte a DÉJÀ été
            // notée « raté » (repetitions remis à 0). La renoter ici la
            // pénaliserait une seconde fois — un « su » donnerait 1 jour au
            // lieu de 3. On planifie donc sans repasser par noter().
            reprises.delete(c.id);
            if (note !== "rate") {
              const etat = progression[c.id] || etatInitial();
              progression[c.id] = { ...etat, du: Date.now() + JOUR_MS_VUE };
              enregistre = majCarte(c.id, progression[c.id]);
            } else {
              // Ratée de nouveau : elle repart en fin de file sans être
              // repénalisée. Voulu — une carte ratée deux fois de suite doit
              // revenir jusqu'à ce qu'elle passe. La session se termine quand
              // l'utilisateur quitte l'écran ; le compteur `total` reste figé.
              file.push(c);
              reprises.add(c.id);
            }
          } else {
            const suivant = noter(progression[c.id] || etatInitial(), note);
            progression[c.id] = suivant;
            enregistre = majCarte(c.id, suivant);
            notees += 1;
            // Une carte ratée revient en fin de file, dans la même session.
            if (note === "rate") {
              file.push(c);
              reprises.add(c.id);
            }
          }
          i += 1;
          afficher();
          // L'échec ne doit jamais rester silencieux : sans ce bandeau,
          // l'utilisateur croit sa session enregistrée alors que
          // localStorage a refusé l'écriture (quota, navigation privée) —
          // mieux vaut un bandeau moche qu'une heure de révision perdue.
          if (!enregistre) {
            racine.insertAdjacentHTML("afterbegin",
              `<div class="carte alerte-stockage">
                 <p class="consigne">⚠ Progression non enregistrée
                   (stockage indisponible). Pensez à exporter depuis Réglages.</p>
               </div>`);
          }
        };
      });
    };
  }

  afficher();
}
