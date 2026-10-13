// app/js/views/reviser.js
import {
  fileDuJour, fileFiltre, fileLibre, fileDifficiles, bilanEcheances, noter, etatInitial,
  estDifficile,
} from "../scheduler.js";
import { genieParCode, categorieParCode, typeParCode, filtreCartes } from "../categories.js";
import {
  charger, majCarte, retirerCarte, enregistrerNotation, annulerNotation,
  chargerActivite, calculerSerie, lireDateEcrit, joursAvant, chargerPrefs, majPrefs,
} from "../store.js";
import { rendreRecto, rendreVerso, hydraterSchemas, echapper } from "../card-render.js";
import { pluriel, formaterJours, formaterEcheance } from "../texte.js";

const TAILLE_FILE = 30;
const TAILLE_LIBRE = 10;
const JOUR_MS_VUE = 86400000;
const DUREE_ANNULATION = 6000;   // fenêtre d'annulation après une notation
const MAX_INDICES_GESTE = 3;     // sessions pendant lesquelles le geste est expliqué
const LIBELLE = { su: "Su", hesite: "Hésité", rate: "Raté" };

/* Modes, choisis par l'URL :
   #/reviser                   la file du jour (échues + nouvelles), thèmes entrelacés
   #/reviser?theme=T06         un thème (écrans Priorités et Catégories)
   #/reviser?genie=electrique  un génie entier
   #/reviser?cat=puissance     une catégorie de thèmes ; cat=toutes pour tout le programme
   #/reviser?type=piege        combiné aux précédents : un seul type de carte
   #/reviser?mode=libre        rien n'est dû : les cartes les plus proches de l'échéance
   #/reviser?mode=difficiles   les cartes ratées au moins trois fois */
export function vueReviser(racine, data, ctx = {}) {
  const params = ctx.params || new URLSearchParams();
  const theme = params.get("theme")
    ? data.themes.find(t => t.code === params.get("theme")) : null;
  const genie = params.get("genie") ? genieParCode(params.get("genie")) : null;
  const categorie = params.get("cat") ? categorieParCode(params.get("cat")) : null;
  const toutes = params.get("cat") === "toutes";
  const type = typeParCode(params.get("type") || "tous");
  const filtre = !!(theme || genie || categorie || toutes || type.code !== "tous");
  const libre = params.get("mode") === "libre";
  const difficiles = params.get("mode") === "difficiles";
  const progression = charger();

  const construireFile = () => {
    const maintenant = Date.now();
    if (filtre) {
      const predicat = filtreCartes({ genie, categorie, theme: theme && theme.code, type: type.code });
      return fileFiltre(data.cards, progression, predicat, maintenant, TAILLE_FILE);
    }
    if (libre) return fileLibre(data.cards, progression, maintenant, TAILLE_LIBRE);
    if (difficiles) return fileDifficiles(data.cards, progression, TAILLE_FILE);
    return fileDuJour(data.cards, progression, maintenant, TAILLE_FILE);
  };

  // Libellé du filtre courant : « Électronique de puissance · Pièges »
  const libelleFiltre = () => {
    const parts = [];
    if (theme) parts.push(`${theme.code} · ${theme.titre}`);
    else if (categorie) parts.push(categorie.titre);
    else if (genie) parts.push(genie.titre);
    else if (toutes) parts.push("Tout le programme");
    if (type.code !== "tous") parts.push(type.titre);
    return parts.join(" · ");
  };

  // Ce que la vue laisse derrière elle (écouteur clavier, toast) et que la
  // vue suivante ne doit pas hériter.
  let demonter = () => {};
  const nettoyer = () => { demonter(); demonter = () => {}; cacherToast(); };

  /* ─── En-tête : repères du jour ou filtre courant ────────────────────── */

  function entete() {
    if (filtre) {
      return `<p class="filtre-theme">
        <span>${echapper(libelleFiltre())}</span>
        <a href="#/categories">Quitter</a></p>`;
    }
    if (libre) {
      return `<p class="filtre-theme">
        <span>Révision libre · échéances les plus proches</span>
        <a href="#/reviser">Quitter</a></p>`;
    }
    if (difficiles) {
      return `<p class="filtre-theme">
        <span>Cartes difficiles · ratées trois fois ou plus</span>
        <a href="#/reviser">Quitter</a></p>`;
    }
    const { dues } = bilanEcheances(data.cards, progression);
    const serie = calculerSerie(chargerActivite());
    const j = joursAvant(lireDateEcrit());
    const items = [];
    if (j === null) items.push(`<a class="repere" href="#/reglages">Date de l'écrit ?</a>`);
    else if (j >= 0) items.push(`<span class="repere${j <= 30 ? " proche" : ""}"><strong>J−${j}</strong></span>`);
    items.push(`<span class="repere"><strong>${dues}</strong> ${dues > 1 ? "dues" : "due"}</span>`);
    items.push(`<span class="repere">Série <strong>${pluriel(serie, "jour")}</strong></span>`);
    return `<p class="reperes">${items.join("")}</p>`;
  }

  /* ─── État vide ──────────────────────────────────────────────────────── */

  function rendreVide() {
    if (filtre || libre || difficiles) {
      racine.innerHTML = `<div class="session">${entete()}
        <div class="carte"><p class="vedette">Aucune carte ici</p>
        <p class="texte-doux">${difficiles
          ? "Aucune carte n'a été ratée trois fois : rien à reprendre."
          : "Cette sélection ne contient aucune carte."}</p></div></div>
        <div id="commandes"><a class="revelateur" href="${filtre ? "#/categories" : "#/reviser"}">${filtre ? "Choisir autre chose" : "Retour à la file du jour"}</a></div>`;
      return;
    }
    const { duesDemain, prochaine } = bilanEcheances(data.cards, progression);
    const suite = prochaine === null
      ? "Toutes les cartes ont été vues et aucune n'est due."
      : duesDemain > 0
        ? `Demain : ${pluriel(duesDemain, "carte")} à revoir.`
        : `Prochaine échéance ${formaterEcheance(prochaine)}.`;
    racine.innerHTML = `<div class="session">${entete()}
      <div class="carte">
        <p class="consigne">Réviser</p>
        <p class="vedette">Tout est à jour</p>
        <p class="texte-doux">${suite} Rien ne vous empêche de garder la main.</p>
      </div></div>
      <div id="commandes">
        <a class="revelateur" href="#/reviser?mode=libre">Réviser quand même ${TAILLE_LIBRE} cartes</a>
        <a class="bouton-secondaire" href="#/priorites">Voir les priorités</a>
      </div>`;
  }

  /* ─── Session ────────────────────────────────────────────────────────── */

  function demarrer(file) {
    demonter();
    let i = 0;
    let notees = 0;
    const total = file.length;          // figé : les reprises ne le gonflent pas
    const reprises = new Set();         // cartes ratées, rejouées en fin de file
    const bilan = { su: 0, hesite: 0, rate: 0 };
    let historique = null;              // dernière notation, annulable
    let revele = false;
    let indiceCompte = false;           // l'indice de geste ne se compte qu'une fois par session

    const surTouche = (e) => {
      if (e.target && e.target.matches && e.target.matches("input, textarea, select")) return;
      if (!revele && (e.key === " " || e.key === "Enter")) {
        if (document.getElementById("reveler")) { e.preventDefault(); reveler(); }
        return;
      }
      const notes = { "1": "rate", "2": "hesite", "3": "su",
                      ArrowLeft: "rate", ArrowUp: "hesite", ArrowRight: "su" };
      if (revele && notes[e.key]) { e.preventDefault(); appliquerNote(notes[e.key]); }
      else if (e.key === "Backspace" || e.key === "z") { e.preventDefault(); annuler(); }
    };
    window.addEventListener("keydown", surTouche);
    demonter = () => window.removeEventListener("keydown", surTouche);

    // Intervalle qu'obtiendrait la carte selon la note : affiché sous chaque
    // bouton, pour que l'ordonnanceur cesse d'être une boîte noire.
    function intervallePrevu(c, note) {
      if (reprises.has(c.id)) return note === "rate" ? 0 : 1;
      return noter(progression[c.id] || etatInitial(), note).intervalle;
    }

    function afficher() {
      revele = false;
      if (i >= file.length) { rendreFin(); return; }
      const c = file[i];
      const rang = Math.min(i + 1, total);
      const pourcent = Math.round((Math.min(i, total) / total) * 100);

      racine.innerHTML = `
        <div class="session">
          ${entete()}
          <div class="jauge" role="progressbar" aria-label="Avancement de la session"
               aria-valuemin="0" aria-valuemax="${total}" aria-valuenow="${Math.min(i, total)}">
            <i style="width:${pourcent}%"></i>
          </div>
          <p class="progression-file">
            <span>${rang} / ${total}</span>
            ${i >= total ? '<span class="reprise">reprise</span>' : ""}
          </p>
          <div class="pile" id="pile">
            <div class="carte recto" id="zone-carte" role="button" tabindex="0"
                 aria-label="Révéler la réponse">${rendreRecto(c, data)}</div>
            <div id="verso" hidden></div>
          </div>
        </div>
        <div id="commandes"><button class="revelateur" id="reveler">Révéler</button></div>`;
      hydraterSchemas(racine);

      document.getElementById("reveler").onclick = reveler;
      // Toute la carte révèle, pas seulement le bouton : la cible est bien
      // plus grande, et c'est la convention des applications de cartes.
      const zone = document.getElementById("zone-carte");
      zone.onclick = reveler;
      zone.onkeydown = (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); reveler(); } };
    }

    function reveler() {
      if (revele || i >= file.length) return;
      revele = true;
      const c = file[i];
      const zone = document.getElementById("zone-carte");
      const v = document.getElementById("verso");

      // Le recto s'efface au profit de la réponse : la question devient un
      // rappel discret, la carte de réponse prend le premier rôle.
      zone.classList.add("estompe");
      zone.onclick = null;
      zone.removeAttribute("role");
      zone.removeAttribute("tabindex");
      zone.removeAttribute("aria-label");

      // Une carte ratée trois fois ne se répare pas en la répétant : le
      // verso le dit, et renvoie à la source.
      const etatCourant = progression[c.id];
      const badge = estDifficile(etatCourant)
        ? `<p class="badge-difficile">Ratée ${pluriel(etatCourant.rates, "fois", "fois")} :
             relire la fiche avant de la renoter.</p>` : "";
      v.innerHTML = `<div class="carte verso">${badge}${rendreVerso(c)}</div>`;
      v.hidden = false;
      hydraterSchemas(v);

      const bouton = (note, classe) => `
        <button class="${classe}" data-n="${note}">
          ${LIBELLE[note]}<span class="touche">${formaterJours(intervallePrevu(c, note))}</span>
        </button>`;
      document.getElementById("commandes").innerHTML = `
        <div class="actions" role="group" aria-label="Noter la carte">
          ${bouton("rate", "b-rate")}${bouton("hesite", "b-hesite")}${bouton("su", "b-su")}
        </div>${indiceGeste()}`;
      document.querySelectorAll("[data-n]").forEach(b => {
        b.onclick = () => appliquerNote(b.dataset.n);
      });

      activerBalayage(document.getElementById("pile"), appliquerNote,
                      () => majPrefs({ aBalaye: true }));
      v.scrollIntoView({ block: "nearest", behavior: "smooth" });
    }

    // Une seule implémentation de la notation, appelée par les boutons, le
    // geste de balayage ET le clavier. Dupliquer cette logique la ferait diverger.
    function appliquerNote(note) {
      if (!revele || i >= file.length) return;
      const c = file[i];
      const estReprise = reprises.has(c.id);
      let enregistre = true;  // sauver() peut échouer (quota, navigation privée)
      let intervalle;

      // Instantané pour l'annulation : tout ce que la notation va toucher.
      historique = {
        i, id: c.id, note, estReprise, aPousse: false,
        etatAvant: progression[c.id], notees, bilan: { ...bilan },
      };

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
          intervalle = 1;
        } else {
          // Ratée de nouveau : elle repart en fin de file sans être
          // repénalisée. Voulu — une carte ratée deux fois de suite doit
          // revenir jusqu'à ce qu'elle passe.
          file.push(c);
          reprises.add(c.id);
          historique.aPousse = true;
          intervalle = 0;
        }
      } else {
        const suivant = noter(progression[c.id] || etatInitial(), note);
        progression[c.id] = suivant;
        enregistre = majCarte(c.id, suivant);
        notees += 1;
        bilan[note] += 1;
        intervalle = suivant.intervalle;
        // Une carte ratée revient en fin de file, dans la même session.
        if (note === "rate") {
          file.push(c);
          reprises.add(c.id);
          historique.aPousse = true;
        }
      }
      enregistrerNotation(note);
      i += 1;
      afficher();
      afficherToast(note, intervalle, annuler);

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
    }

    // Un balayage parti trop vite ne doit pas coûter une carte : on remet
    // exactement l'état d'avant, en mémoire comme sur disque.
    function annuler() {
      if (!historique) return;
      const h = historique;
      historique = null;
      if (h.aPousse) file.pop();
      if (h.estReprise) reprises.add(h.id); else reprises.delete(h.id);
      if (h.etatAvant === undefined) { delete progression[h.id]; retirerCarte(h.id); }
      else { progression[h.id] = h.etatAvant; majCarte(h.id, h.etatAvant); }
      annulerNotation(h.note);
      notees = h.notees;
      Object.assign(bilan, h.bilan);
      i = h.i;
      cacherToast();
      afficher();
    }

    // Le geste est invisible par nature : on l'explique sous les boutons
    // pendant les premières sessions, jusqu'à ce qu'il ait servi une fois.
    function indiceGeste() {
      if (!window.matchMedia("(pointer: coarse)").matches) return "";
      const prefs = chargerPrefs();
      if (prefs.aBalaye || (prefs.indiceGesteVu || 0) >= MAX_INDICES_GESTE) return "";
      if (!indiceCompte) {
        indiceCompte = true;
        majPrefs({ indiceGesteVu: (prefs.indiceGesteVu || 0) + 1 });
      }
      return `<p class="indice-geste">Ou balayez la carte :
        <span>← Raté</span><span>↑ Hésité</span><span>Su →</span></p>`;
    }

    function rendreFin() {
      const suivante = construireFile();
      let suite;
      if (filtre) {
        suite = suivante.length
          ? `Il reste ${pluriel(suivante.length, "carte")} dans cette sélection.`
          : "Vous avez fait le tour de cette sélection pour aujourd'hui.";
      } else if (difficiles) {
        suite = "Ces cartes resteront marquées difficiles : le compteur d'échecs ne redescend pas, seule la régularité des réussites compte.";
      } else {
        const { dues, prochaine } = bilanEcheances(data.cards, progression);
        suite = dues > 0
          ? `Encore ${pluriel(dues, "carte due", "cartes dues")} aujourd'hui.`
          : prochaine === null
            ? "Plus rien n'est dû."
            : `Plus rien n'est dû aujourd'hui. Prochaine échéance ${formaterEcheance(prochaine)}.`;
      }
      racine.innerHTML = `
        <div class="session">
          ${entete()}
          <div class="carte fin">
            <p class="consigne">Session terminée</p>
            <p class="vedette">${pluriel(notees, "carte révisée", "cartes révisées")}</p>
            <ul class="bilan" aria-label="Bilan de la session">
              <li class="su"><strong>${bilan.su}</strong><span>su</span></li>
              <li class="hesite"><strong>${bilan.hesite}</strong><span>hésité</span></li>
              <li class="rate"><strong>${bilan.rate}</strong><span>raté</span></li>
            </ul>
            <p class="texte-doux">${suite}</p>
          </div>
        </div>
        <div id="commandes">
          ${suivante.length ? `<button class="revelateur" id="encore">Encore ${pluriel(suivante.length, "carte")}</button>` : ""}
          <a class="bouton-secondaire" href="${filtre ? "#/categories" : "#/priorites"}">${filtre ? "Autre catégorie" : "Voir les priorités"}</a>
        </div>`;
      const encore = document.getElementById("encore");
      if (encore) encore.onclick = () => demarrer(suivante);
    }

    afficher();
  }

  const file = construireFile();
  if (file.length === 0) rendreVide();
  else demarrer(file);
  return nettoyer;
}

/* ─── Toast d'annulation ───────────────────────────────────────────────
   Dans la zone des commandes, pas en superposition : un toast flottant
   finirait par masquer la réponse d'une carte longue. Ici il ne recouvre
   rien, il pousse simplement le bouton d'un cran pendant six secondes.  */

let minuteurToast = null;

function afficherToast(note, intervalle, annuler) {
  cacherToast(true);
  const commandes = document.getElementById("commandes");
  if (!commandes) return;
  const t = document.createElement("div");
  t.id = "toast";
  t.className = "toast";
  t.setAttribute("role", "status");
  t.dataset.note = note;
  const quand = note === "rate" ? "revient en fin de session" : `revient ${formaterJours(intervalle)}`;
  t.innerHTML = `<span><strong>${LIBELLE[note]}</strong> · ${quand}</span>
                 <button type="button" id="annuler">Annuler</button>`;
  t.querySelector("#annuler").onclick = annuler;
  commandes.prepend(t);
  requestAnimationFrame(() => t.classList.add("visible"));
  minuteurToast = setTimeout(() => cacherToast(), DUREE_ANNULATION);
}

function cacherToast(immediat = false) {
  clearTimeout(minuteurToast);
  const t = document.getElementById("toast");
  if (!t) return;
  if (immediat) { t.remove(); return; }
  t.classList.remove("visible");
  setTimeout(() => t.remove(), 240);
}

/* ─── Balayage ──────────────────────────────────────────────────────────
   Gauche = raté, droite = su, haut = hésité. Utilisable d'une seule main
   dans les transports, ce qui est l'usage réel visé. Les boutons restent
   la voie principale : le geste ne remplace rien, il double.            */

const SEUIL_PX = 70;        // au-delà, le geste vaut notation

function activerBalayage(zone, appliquerNote, surGeste) {
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
    // Une formule plus large que la carte se fait défiler au doigt : ce
    // défilement horizontal n'est pas une notation.
    const defilable = e.target.closest && e.target.closest(".katex-display");
    if (defilable && defilable.scrollWidth > defilable.clientWidth + 2) return;
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
    if (surGeste) surGeste();
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
