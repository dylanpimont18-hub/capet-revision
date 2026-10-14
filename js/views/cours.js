// app/js/views/cours.js
// Le cours : un chapitre par thème, du fondamental vers l'appliqué (ordre du
// plan de cours/PROGRES.md, repris par cours/index.json).
//   #/cours                              liste des chapitres
//   #/cours?theme=T07                    lecture d'un chapitre
//   #/cours?theme=T07&section=t07-boost  lecture, ouverte sur une section
// La lecture suit le modèle de vueEpreuve (sujets.js) : sommaire replié,
// formules KaTeX, schémas agrandissables, chapitres précédent et suivant.
import { echapper, ouvrirPleinEcran, rendreMathsDans } from "../card-render.js";
import { CATEGORIES } from "../categories.js";
import { pluriel } from "../texte.js";

let INDEX = null;

// Index du cours, chargé une fois. Hors ligne sans cache, la liste reste vide
// plutôt que de casser l'écran (même règle que l'index des épreuves).
export async function chargerIndexCours() {
  if (!INDEX) {
    try {
      const r = await fetch("cours/index.json");
      INDEX = r.ok ? (await r.json()).chapitres : [];
    } catch {
      INDEX = [];
    }
  }
  return INDEX;
}

// Chapitres rédigés, dans l'ordre de lecture.
export function chapitresDisponibles(index) {
  return index.filter(c => c.disponible).sort((a, b) => a.ordre - b.ordre);
}

// Premier chapitre rédigé d'une catégorie (ordre du plan), ou null.
export function premierChapitre(index, categorie) {
  const themes = new Set(categorie.themes);
  return chapitresDisponibles(index).find(c => themes.has(c.theme)) || null;
}

const CHEVRON = `<svg class="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
  stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 6 6 6-6 6"/></svg>`;

export async function vueCours(racine, data, ctx = {}) {
  const theme = ctx.params && ctx.params.get("theme");
  const index = await chargerIndexCours();
  if (theme) return lireChapitre(racine, data, index, theme, ctx.params.get("section"));
  return listerChapitres(racine, index);
}

function listerChapitres(racine, index) {
  const dispo = chapitresDisponibles(index);
  if (!index.length) {
    racine.innerHTML = `<div class="carte"><p class="consigne">Cours</p>
      <p class="texte-doux">Le cours n'est pas encore disponible hors ligne.
        Ouvrez cet écran une fois en ligne pour le mettre en cache.</p>
      <a class="bouton-secondaire" href="#/categories">Retour aux catégories</a></div>`;
    return;
  }
  const categorie = (code) => CATEGORIES.find(c => c.themes.includes(code));
  const lignes = index.map(c => {
    const cat = categorie(c.theme);
    const meta = c.disponible
      ? `${c.theme} · ${cat ? echapper(cat.titre) + " · " : ""}${pluriel(c.schemas, "schéma")}`
      : `${c.theme} · à paraître`;
    const corps = `<span class="numero">${c.ordre}</span>
      <span class="corps"><span class="theme">${echapper(c.titre)}</span>
        <span class="meta">${meta}</span></span>`;
    return c.disponible
      ? `<li><a class="ligne-sujet ligne-chapitre" href="#/cours?theme=${encodeURIComponent(c.theme)}">${corps}${CHEVRON}</a></li>`
      : `<li><span class="ligne-sujet ligne-chapitre a-paraitre">${corps}</span></li>`;
  }).join("");

  racine.innerHTML = `
    <div class="carte">
      <p class="consigne">Cours</p>
      <p class="vedette">Génie électrique, informatique et automatique</p>
      <p class="texte-doux">${pluriel(dispo.length, "chapitre rédigé", "chapitres rédigés")} sur ${index.length}.
        L'ordre va du fondamental vers l'appliqué : chaque chapitre ne suppose que ceux qui le précèdent.
        Chaque chapitre se termine par un auto-test et un lien vers ses cartes.</p>
      ${dispo.length ? `<a class="revelateur" href="#/cours?theme=${encodeURIComponent(dispo[0].theme)}"
         style="margin-top:var(--e3)">Commencer : ${echapper(dispo[0].titre)}</a>` : ""}
    </div>
    <section class="carte carte-liste" aria-labelledby="plan-cours">
      <p class="consigne" id="plan-cours">Chapitres</p>
      <ol class="liste-themes">${lignes}</ol>
    </section>`;
}

async function lireChapitre(racine, data, index, theme, section) {
  const dispo = chapitresDisponibles(index);
  const i = dispo.findIndex(c => c.theme === theme);
  if (i < 0) {
    const prevu = index.find(c => c.theme === theme);
    racine.innerHTML = `<div class="carte"><p class="vedette">${prevu ? "Chapitre à paraître" : "Chapitre introuvable"}</p>
      <p class="texte-doux">${prevu ? `« ${echapper(prevu.titre)} » n'est pas encore rédigé.` : "Ce thème n'a pas de chapitre de cours."}</p>
      <a class="bouton-secondaire" href="#/cours">Tous les chapitres</a></div>`;
    return;
  }
  const c = dispo[i];
  const precedent = dispo[i - 1];
  const suivant = dispo[i + 1];
  const titreTheme = (data.themes.find(t => t.code === c.theme) || {}).titre || "";
  const lien = (x, sens) => x
    ? `<a class="bouton-secondaire" href="#/cours?theme=${encodeURIComponent(x.theme)}"
         aria-label="${sens === "←" ? "Chapitre précédent" : "Chapitre suivant"} : ${echapper(x.titre)}">${sens} ${x.ordre}. ${echapper(x.titre)}</a>`
    : `<span></span>`;
  const sections = c.sommaire.filter(s => s.niveau === 2).length;

  racine.innerHTML = `
    <div class="carte entete-epreuve entete-cours">
      <p class="consigne">Cours · chapitre ${c.ordre} · ${c.theme}</p>
      <p class="vedette">${echapper(c.titre)}</p>
      ${titreTheme ? `<p class="texte-doux">Thème ${c.theme} : ${echapper(titreTheme)}</p>` : ""}
      ${c.sommaire.length ? `
      <details class="sommaire-epreuve">
        <summary>Sommaire · ${pluriel(sections, "rubrique")}</summary>
        <ol>${c.sommaire.map(s => `<li class="niv${s.niveau}"><a href="#${s.id}" data-cible="${s.id}">${echapper(s.texte)}</a></li>`).join("")}</ol>
      </details>` : ""}
    </div>
    <article class="texte-cours" id="corps-cours" aria-label="Chapitre ${c.ordre} : ${echapper(c.titre)}">
      <p class="texte-doux">Chargement du chapitre…</p>
    </article>
    <nav class="pagination-epreuve" aria-label="Autres chapitres">
      ${lien(precedent, "←")}
      <a class="bouton-secondaire" href="#/cours">Tous les chapitres</a>
      ${lien(suivant, "→")}
    </nav>`;

  const article = document.getElementById("corps-cours");
  let corps;
  try {
    const r = await fetch(`cours/textes/${c.theme}.html`);
    if (!r.ok) throw new Error(r.status);
    corps = await r.text();
  } catch {
    article.innerHTML = `<p class="avertissement">Ce chapitre n'est pas disponible hors ligne.
      Ouvrez-le une fois en ligne pour le mettre en cache.</p>`;
    return;
  }
  // La vue a pu être quittée pendant le chargement.
  if (!document.body.contains(article)) return;
  article.innerHTML = corps;

  // Tableaux : défilement dans leur seul cadre, jamais sur la page.
  article.querySelectorAll("table").forEach(t => {
    if (t.parentElement.classList.contains("table-scroll")) return;
    const cadre = document.createElement("div");
    cadre.className = "table-scroll";
    t.parentNode.insertBefore(cadre, t);
    cadre.appendChild(t);
  });
  rendreMathsDans(article);
  souderFormules(article);
  souderEpreuves(article);

  // Schémas : un toucher (ou Entrée) ouvre la figure en plein écran.
  article.querySelectorAll("figure.schema").forEach(fig => {
    const svg = fig.querySelector(":scope > svg");
    if (!svg) return;
    fig.tabIndex = 0;
    fig.setAttribute("aria-description", "Toucher pour agrandir");
    const agrandir = () => ouvrirPleinEcran(svg.cloneNode(true));
    fig.addEventListener("click", (ev) => { if (!ev.target.closest("a, figcaption")) agrandir(); });
    fig.addEventListener("keydown", (ev) => {
      if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); agrandir(); }
    });
  });

  // Ancres internes (#t01-ohm) : défilement sans toucher au fragment de
  // l'URL, qui est la route du routeur. Les liens #/… restent des routes.
  const allerA = (id, lisse = true) => {
    const cible = document.getElementById(id);
    if (!cible) return;
    if (cible.tagName === "DETAILS") cible.open = true;
    cible.scrollIntoView({ behavior: lisse ? "smooth" : "auto", block: "start" });
  };
  // Écouteurs posés sur les blocs de la vue, pas sur `racine`, qui survit
  // aux changements d'écran et les accumulerait.
  const surLien = (ev) => {
    const a = ev.target.closest("a[href^='#']");
    if (!a) return;
    const href = a.getAttribute("href");
    if (href.startsWith("#/")) return;
    ev.preventDefault();
    allerA(a.dataset.cible || href.slice(1));
    const sommaire = a.closest("details.sommaire-epreuve");
    if (sommaire) sommaire.open = false;
  };
  article.addEventListener("click", surLien);
  racine.querySelector(".entete-cours").addEventListener("click", surLien);

  if (section) requestAnimationFrame(() => allerA(section, false));
}

// Identifiants d'épreuve (2018-E2) : le navigateur coupe volontiers au trait
// d'union et rejette « E2 » seul à la ligne. On les rend insécables.
const EPREUVE = /\d{4}-E\d/g;

function souderEpreuves(article) {
  const marcheur = document.createTreeWalker(article, NodeFilter.SHOW_TEXT, {
    acceptNode: (n) => n.parentElement.closest("svg, .katex, .insecable")
      ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT,
  });
  const noeuds = [];
  while (marcheur.nextNode()) {
    if (EPREUVE.test(marcheur.currentNode.nodeValue)) noeuds.push(marcheur.currentNode);
    EPREUVE.lastIndex = 0;
  }
  for (const n of noeuds) {
    const morceaux = n.nodeValue.split(/(\d{4}-E\d)/);
    const frag = document.createDocumentFragment();
    morceaux.forEach((m, i) => {
      if (i % 2) {
        const s = document.createElement("span");
        s.className = "insecable";
        s.textContent = m;
        frag.append(s);
      } else if (m) frag.append(m);
    });
    n.replaceWith(frag);
  }
}

// Formules en ligne : KaTeX autorise une coupure après chaque signe = ou +,
// ce qui donne sur un écran étroit « n − » en fin de ligne et « 1 » au début
// de la suivante, ou une virgule rejetée seule à la ligne. Une formule courte
// (moins de 60 % de la colonne) devient insécable, et la ponctuation qui la
// touche (parenthèse, guillemet, virgule, point…) lui reste attachée. Les
// formules longues gardent leurs coupures, sans quoi elles déborderaient.
const AVANT = /[(«[]\u202f?$/;
const APRES = /^\u202f?[,.;:!?)\]»…]+/;

function souderFormules(article) {
  const colonne = article.clientWidth;
  const formules = [...article.querySelectorAll(".maths")];
  // Toutes les mesures d'abord, toutes les écritures ensuite : une seule mise
  // en page au lieu d'une par formule.
  const courtes = formules.filter(m => {
    const largeur = [...m.querySelectorAll(".katex-html > .base")]
      .reduce((somme, b) => somme + b.getBoundingClientRect().width, 0);
    return largeur > 0 && largeur < 0.6 * colonne;
  });
  for (const m of courtes) {
    const bloc = document.createElement("span");
    bloc.className = "insecable";
    m.replaceWith(bloc);
    bloc.append(m);
    const avant = bloc.previousSibling;
    const apres = bloc.nextSibling;
    if (avant && avant.nodeType === Node.TEXT_NODE) {
      const x = avant.nodeValue.match(AVANT);
      if (x) { avant.nodeValue = avant.nodeValue.slice(0, -x[0].length); bloc.prepend(x[0]); }
    }
    if (apres && apres.nodeType === Node.TEXT_NODE) {
      const x = apres.nodeValue.match(APRES);
      if (x) { apres.nodeValue = apres.nodeValue.slice(x[0].length); bloc.append(x[0]); }
    }
  }
}
