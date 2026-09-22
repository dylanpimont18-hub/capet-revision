// app/js/app.js
import { vueReviser } from "./views/reviser.js";
import { vuePriorites } from "./views/priorites.js";
import { vueReglages } from "./views/reglages.js";

const CLE_THEME = "capet.theme";

function appliquerTheme(t) {
  document.documentElement.dataset.theme = t;
  try { localStorage.setItem(CLE_THEME, t); } catch { /* mode privé */ }
}

let DATA = null;

async function donnees() {
  if (!DATA) DATA = await (await fetch("cards.json")).json();
  return DATA;
}

const ROUTES = {
  "#/reviser": vueReviser,
  "#/priorites": vuePriorites,
  "#/reglages": vueReglages,
};

async function naviguer() {
  const hash = location.hash || "#/reviser";
  const racine = document.getElementById("app");
  const vue = ROUTES[hash];

  document.querySelectorAll(".barre-bas a").forEach(a =>
    a.classList.toggle("actif", a.getAttribute("href") === hash));

  if (!vue) {
    racine.innerHTML = `<div class="carte"><p>Écran à venir.</p></div>`;
    return;
  }
  racine.innerHTML = `<div class="carte"><p class="consigne">Chargement…</p></div>`;
  try {
    vue(racine, await donnees());
  } catch (e) {
    racine.innerHTML = `<div class="carte"><p class="vedette">Données indisponibles</p>
      <p class="consigne">Lancez <code>python scripts/build_cards.py</code> puis rechargez.</p></div>`;
  }
}

window.addEventListener("hashchange", naviguer);
window.addEventListener("DOMContentLoaded", () => {
  let t = "clair";
  try { t = localStorage.getItem(CLE_THEME) || "clair"; } catch { /* ignore */ }
  appliquerTheme(t);
  document.getElementById("bascule-theme").onclick = () =>
    appliquerTheme(document.documentElement.dataset.theme === "sombre" ? "clair" : "sombre");
  if (!location.hash) location.hash = "#/reviser";
  naviguer();

  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("sw.js").catch(() => { /* hors https/localhost */ });
  }
});
