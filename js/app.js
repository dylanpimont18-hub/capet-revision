// app/js/app.js
import { vueReviser } from "./views/reviser.js";
import { vuePriorites } from "./views/priorites.js";
import { vueReglages } from "./views/reglages.js";

const CLE_THEME = "capet.theme";

// La barre d'état iOS et le chrome Safari suivent la couleur de fond réelle
// de chaque thème : un bleu fixe au-dessus d'un en-tête gris clair jure.
const COULEUR_BARRE = { sombre: "#0b0f17", clair: "#f7f8fa" };

// L'icône annonce le thème vers lequel on bascule, et le libellé le dit.
const ICONE = {
  clair: '<circle cx="12" cy="12" r="4"/><path d="M12 2.5v2M12 19.5v2M4.3 4.3l1.4 1.4M18.3 18.3l1.4 1.4M2.5 12h2M19.5 12h2M4.3 19.7l1.4-1.4M18.3 5.7l1.4-1.4"/>',
  sombre: '<path d="M12 3a9 9 0 1 0 9 9 7 7 0 0 1-9-9Z"/>',
};

function appliquerTheme(t) {
  document.documentElement.dataset.theme = t;
  const meta = document.querySelector('meta[name="theme-color"]');
  if (meta) meta.content = COULEUR_BARRE[t] || COULEUR_BARRE.sombre;
  const bouton = document.getElementById("bascule-theme");
  if (bouton) {
    const cible = t === "clair" ? "sombre" : "clair";
    bouton.querySelector("svg").innerHTML = ICONE[cible];
    bouton.setAttribute("aria-label", `Passer en thème ${cible}`);
  }
  try { localStorage.setItem(CLE_THEME, t); } catch { /* mode privé */ }
}

let DATA = null;

// Chaque schéma donne deux cartes : reconnaître (le SVG au recto), puis
// tracer de mémoire (le nom au recto, le SVG au verso). La seconde n'entre
// en rotation qu'après une réussite sur la première (prérequis) : produire
// un schéma est plus exigeant, et plus formateur, que le reconnaître.
function enrichir(data) {
  const traces = data.cards
    .filter(c => c.type === "schema" && c.svg && c.niveau !== "trace")
    .map(c => ({ ...c, id: `${c.id}-trace`, niveau: "trace", prerequis: c.id }));
  return { ...data, cards: [...data.cards, ...traces] };
}

async function donnees() {
  if (!DATA) DATA = enrichir(await (await fetch("cards.json")).json());
  return DATA;
}

const ROUTES = {
  "#/reviser": vueReviser,
  "#/priorites": vuePriorites,
  "#/reglages": vueReglages,
};

// « #/reviser?theme=T06 » : le chemin choisit la vue, la requête la paramètre.
function lireRoute() {
  const hash = location.hash || "#/reviser";
  const [chemin, requete = ""] = hash.split("?");
  return { chemin, params: new URLSearchParams(requete) };
}

// Ce que la vue précédente doit défaire avant de céder la place (écouteurs
// globaux, toast). Une vue qui n'a rien à défaire ne renvoie rien.
let demonterVue = null;

async function naviguer() {
  const { chemin, params } = lireRoute();
  const racine = document.getElementById("app");
  const vue = ROUTES[chemin];

  if (typeof demonterVue === "function") demonterVue();
  demonterVue = null;

  // La couleur seule ne suffit pas : aria-current expose l'onglet courant
  // aux lecteurs d'écran, qui ne perçoivent pas la mise en évidence visuelle.
  document.querySelectorAll(".barre-bas a").forEach(a => {
    const courant = a.getAttribute("href") === chemin;
    a.classList.toggle("actif", courant);
    if (courant) a.setAttribute("aria-current", "page");
    else a.removeAttribute("aria-current");
  });

  if (!vue) {
    location.hash = "#/reviser";
    return;
  }
  // Un changement d'écran repart du haut : sinon l'écran Priorités s'ouvre
  // à la hauteur où la carte précédente avait fait défiler la page.
  window.scrollTo(0, 0);
  racine.innerHTML = `<div class="carte"><p class="consigne">Chargement…</p></div>`;
  try {
    demonterVue = vue(racine, await donnees(), { params, naviguer });
  } catch (e) {
    racine.innerHTML = `<div class="carte"><p class="vedette">Données indisponibles</p>
      <p class="texte-doux">Lancez <code>python scripts/build_cards.py</code> puis rechargez.</p></div>`;
  }
}

window.addEventListener("hashchange", naviguer);
window.addEventListener("DOMContentLoaded", () => {
  // Ordre de décision : choix explicite de l'utilisateur, sinon réglage du
  // système, sinon sombre — la révision se fait surtout le soir.
  let t = null;
  try { t = localStorage.getItem(CLE_THEME); } catch { /* mode privé */ }
  if (!t) {
    t = window.matchMedia("(prefers-color-scheme: light)").matches ? "clair" : "sombre";
  }
  appliquerTheme(t);

  document.getElementById("bascule-theme").addEventListener("click", () => {
    appliquerTheme(document.documentElement.dataset.theme === "clair" ? "sombre" : "clair");
  });

  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("sw.js").catch(() => { /* hors ligne : déjà installé ou indisponible */ });
  }

  naviguer();
});
