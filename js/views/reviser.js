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
    const rang = Math.min(i + 1, total);
    const pourcent = Math.round((Math.min(i, total) / total) * 100);

    racine.innerHTML = `
      <div class="jauge" role="progressbar" aria-label="Avancement de la session"
           aria-valuemin="0" aria-valuemax="${total}" aria-valuenow="${Math.min(i, total)}">
        <i style="width:${pourcent}%"></i>
      </div>
      <p class="progression-file">
        <span>${rang} / ${total}</span>
        ${restantes > total - i ? '<span class="reprise">reprise</span>' : ""}
      </p>
      <div class="carte zone-swipe" id="zone-carte">${rendreRecto(c, data)}</div>
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
      // Une seule implémentation de la notation, appelée par les boutons ET
      // par le geste de balayage. Dupliquer cette logique la ferait diverger.
      const appliquerNote = (note) => {
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
              `<div class="carte alerte-stockage" role="alert">
                 <p class="consigne">
                   <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
                        stroke-width="1.9" stroke-linecap="round"
                        stroke-linejoin="round" aria-hidden="true">
                     <path d="M12 9v4.5M12 17h.01"/>
                     <path d="M10.3 3.9 2.4 17.6A2 2 0 0 0 4.1 20.6h15.8a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z"/>
                   </svg>
                   Progression non enregistrée (stockage indisponible).
                   Pensez à exporter depuis Réglages.
                 </p>
               </div>`);
          }
      };

      document.querySelectorAll("[data-n]").forEach(b => {
        b.onclick = () => appliquerNote(b.dataset.n);
      });

      activerBalayage(document.getElementById("zone-carte"), appliquerNote);
    };
  }

  afficher();
}

/* ─── Balayage ──────────────────────────────────────────────────────────
   Gauche = raté, droite = su, haut = hésité. Utilisable d'une seule main
   dans les transports, ce qui est l'usage réel visé. Les boutons restent
   la voie principale : le geste ne remplace rien, il double.            */

const SEUIL_PX = 70;        // au-delà, le geste vaut notation
const LIBELLE = { su: "Su", hesite: "Hésité", rate: "Raté" };

function activerBalayage(zone, appliquerNote) {
  if (!zone || !window.matchMedia("(pointer: coarse)").matches) return;

  let x0 = 0, y0 = 0, dx = 0, dy = 0, actif = false;

  const indice = document.createElement("div");
  indice.className = "indice-swipe";
  indice.setAttribute("aria-hidden", "true");
  document.body.appendChild(indice);

  const noteDuGeste = () => {
    if (dy < -SEUIL_PX && Math.abs(dy) > Math.abs(dx)) return "hesite";
    if (dx > SEUIL_PX) return "su";
    if (dx < -SEUIL_PX) return "rate";
    return null;
  };

  const nettoyer = () => {
    indice.classList.remove("visible");
    indice.remove();
  };

  zone.addEventListener("touchstart", (e) => {
    if (e.touches.length !== 1) return;
    actif = true;
    x0 = e.touches[0].clientX;
    y0 = e.touches[0].clientY;
    dx = dy = 0;
    zone.classList.remove("glisse");
  }, { passive: true });

  zone.addEventListener("touchmove", (e) => {
    if (!actif) return;
    dx = e.touches[0].clientX - x0;
    dy = e.touches[0].clientY - y0;

    // Un défilement vertical vers le bas n'est pas un geste de notation :
    // on rend la main au navigateur plutôt que de capturer le scroll.
    if (dy > 24 && Math.abs(dy) > Math.abs(dx)) { actif = false; return; }

    const monte = dy < 0 && Math.abs(dy) > Math.abs(dx);
    zone.style.transform = monte
      ? `translateY(${Math.max(dy, -120)}px)`
      : `translateX(${dx}px) rotate(${dx / 28}deg)`;
    zone.style.opacity = String(
      Math.max(0.45, 1 - Math.max(Math.abs(dx), Math.abs(dy)) / 320)
    );

    const n = noteDuGeste();
    if (n) {
      indice.dataset.note = n;
      indice.textContent = LIBELLE[n];
      indice.classList.add("visible");
    } else {
      indice.classList.remove("visible");
    }
  }, { passive: true });

  zone.addEventListener("touchend", () => {
    if (!actif) return;
    actif = false;
    const n = noteDuGeste();
    zone.classList.add("glisse");

    if (!n) {                       // en deçà du seuil : la carte revient
      zone.style.transform = "";
      zone.style.opacity = "";
      indice.classList.remove("visible");
      return;
    }

    // La carte sort dans la direction du geste, puis la notation s'applique.
    zone.style.transform = n === "hesite"
      ? "translateY(-140%)"
      : `translateX(${n === "su" ? 140 : -140}%) rotate(${n === "su" ? 12 : -12}deg)`;
    zone.style.opacity = "0";
    nettoyer();
    setTimeout(() => appliquerNote(n), 160);
  }, { passive: true });

  zone.addEventListener("touchcancel", () => {
    actif = false;
    zone.classList.add("glisse");
    zone.style.transform = "";
    zone.style.opacity = "";
    indice.classList.remove("visible");
  }, { passive: true });
}
