// app/js/card-render.js
// Rendu HTML d'une carte, recto et verso. Aucun contenu pédagogique en dur ici.
// Trois types de cartes (formule, piege, schema) : voir task-10-brief.md pour le
// tableau des règles recto/verso. Règle absolue : le recto ne doit jamais dévoiler
// la réponse (formule, règle, ou schéma selon le niveau).

export function echapper(s) {
  return String(s ?? "")
    .replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;").replaceAll("'", "&#039;");
}

// KaTeX est vendored (app/vendor/katex/) et chargé en <script> classique par la
// page hôte, donc exposé en global. On y accède via globalThis pour rester
// utilisable tel quel en environnement Node (vérification hors navigateur) et en
// navigateur (où globalThis === window). Sans KaTeX chargé (échec réseau au
// vendoring, ou page qui ne l'a pas inclus), on retombe sur un <code> échappé :
// le module reste fonctionnel hors ligne dans tous les cas.
function maths(latex, displayMode = true) {
  const katex = globalThis.katex;
  if (katex) {
    try {
      return katex.renderToString(latex, { displayMode, throwOnError: false });
    } catch { /* retombe sur le brut */ }
  }
  return `<code class="latex-brut">${echapper(latex)}</code>`;
}

// 26 labels du corpus contiennent du LaTeX inline — « Phase $t \in [0;\alpha T[$ »,
// « Rapport cyclique maximisant $\Delta i_L$ ». Affichés via echapper() seul,
// ils apparaîtraient en source brute. On rend donc chaque segment $…$ par
// KaTeX (mode inline) et on échappe le texte autour : jamais de HTML non
// échappé hors des segments math.
// Un énoncé du corpus commence souvent en minuscule (fragment de liste) ;
// affiché seul en position de réponse, il mérite sa majuscule.
function majuscule(s) {
  const t = String(s ?? "").trim();
  return t.charAt(0).toUpperCase() + t.slice(1);
}

export function texteAvecMaths(s) {
  const brut = String(s ?? "");
  if (!brut.includes("$")) return echapper(brut);
  return brut
    .split(/(\$[^$]+\$)/g)
    .map(seg =>
      seg.startsWith("$") && seg.endsWith("$") && seg.length > 2
        ? maths(seg.slice(1, -1), false)
        : echapper(seg)
    )
    .join("");
}

// Le SVG est injecté inline (voir hydraterSchemas) et non via <img> : dans
// une image, la feuille de style interne du SVG suit `prefers-color-scheme`
// du système, pas le thème choisi dans l'app. Système clair + app sombre
// donnait des traits bleu nuit sur fond sombre. Inline, les traits héritent
// de `currentColor` et var(--svg-bg) du document : ils suivent le thème réel.
function svg(chemin, alt) {
  return `<div class="carte-svg" data-svg="${echapper(chemin)}" role="img"
               aria-label="${echapper(alt)}"></div>`;
}

const SVG_CACHE = new Map();

async function chargerSvg(chemin) {
  if (!SVG_CACHE.has(chemin)) {
    SVG_CACHE.set(chemin, fetch(chemin).then(r => {
      if (!r.ok) throw new Error(r.status);
      return r.text();
    }).then(txt => {
      // La <style> interne (couleur selon le système) deviendrait globale une
      // fois dans le document et repeindrait aussi les icônes de navigation.
      // Largeur/hauteur en pt sont retirées : la taille vient du CSS.
      return txt
        .replace(/<\?xml[^>]*>|<!--[\s\S]*?-->|<style>[\s\S]*?<\/style>/g, "")
        .replace(/<svg\b([^>]*)>/, (m, attrs) =>
          `<svg${attrs.replace(/\s(width|height)='[^']*'/g, "")}>`);
    }).catch(e => { SVG_CACHE.delete(chemin); throw e; }));
  }
  return SVG_CACHE.get(chemin);
}

// À appeler après insertion du HTML d'une carte. Remplit chaque conteneur
// [data-svg] ; en cas d'échec (hors ligne sans cache), retombe sur <img>.
// Plein écran : une figure (schéma ou image) occupe tout l'écran, le fond ne
// défile pas, Échap ou un toucher la ferme. Le pincement natif zoome.
export function ouvrirPleinEcran(noeud, legende = "Pincez pour zoomer · touchez pour fermer") {
  const voile = document.createElement("div");
  voile.className = "plein-ecran";
  voile.setAttribute("role", "dialog");
  voile.setAttribute("aria-label", "Figure agrandie");
  voile.innerHTML = `<button type="button" class="fermer" aria-label="Fermer">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
           stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>
    </button><div class="cadre"></div><p class="aide">${legende}</p>`;
  voile.querySelector(".cadre").appendChild(noeud);
  // Le fond ne doit pas défiler pendant l'affichage : sans verrou, la roue
  // ou le glissement font remonter la page derrière la figure.
  const html = document.documentElement;
  const etatDefilement = html.style.overflow;
  html.style.overflow = "hidden";
  const surEchap = (e) => { if (e.key === "Escape") fermer(); };
  const fermer = () => {
    voile.remove();
    html.style.overflow = etatDefilement;
    document.removeEventListener("keydown", surEchap);
  };
  document.addEventListener("keydown", surEchap);
  voile.querySelector(".fermer").onclick = fermer;
  voile.onclick = (e) => { if (e.target === voile || e.target.classList.contains("aide")) fermer(); };
  document.body.appendChild(voile);
}

// Un schéma se lit mal sur 36 mm de large : un toucher l'ouvre en plein écran.
function activerAgrandissement(zone) {
  if (zone.dataset.agrandissable) return;
  zone.dataset.agrandissable = "1";
  zone.style.cursor = "zoom-in";
  zone.addEventListener("click", (e) => {
    // Toucher le schéma l'agrandit ; il ne doit pas aussi révéler la carte.
    e.stopPropagation();
    const svgEl = zone.querySelector("svg");
    if (svgEl) ouvrirPleinEcran(svgEl.cloneNode(true));
  });
}

// Formules dans un texte déjà inséré : $…$ et $$…$$ deviennent des rendus
// KaTeX. Parcourt les nœuds texte, donc ne touche ni aux balises ni aux
// attributs. Sans KaTeX chargé, le texte reste tel quel.
export function rendreMathsDans(racine) {
  if (!globalThis.katex) return;
  const marche = document.createTreeWalker(racine, NodeFilter.SHOW_TEXT, {
    acceptNode: (n) => n.nodeValue.includes("$") && !n.parentElement.closest("script,style,.katex")
      ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT,
  });
  const noeuds = [];
  while (marche.nextNode()) noeuds.push(marche.currentNode);
  for (const n of noeuds) {
    const morceaux = n.nodeValue.split(/(\$\$[\s\S]+?\$\$|\$[^$\n]+?\$)/g);
    if (morceaux.length < 2) continue;
    const frag = document.createDocumentFragment();
    for (const m of morceaux) {
      if (!m) continue;
      if (m.startsWith("$$") && m.endsWith("$$") && m.length > 4) frag.append(tex(m.slice(2, -2), true));
      else if (m.startsWith("$") && m.endsWith("$") && m.length > 2) frag.append(tex(m.slice(1, -1), false));
      else frag.append(document.createTextNode(m));
    }
    n.parentNode.replaceChild(frag, n);
  }
}

function tex(latex, display) {
  const span = document.createElement(display ? "div" : "span");
  span.className = display ? "maths-bloc" : "maths";
  try {
    span.innerHTML = globalThis.katex.renderToString(latex, { displayMode: display, throwOnError: false });
  } catch {
    span.textContent = latex;
  }
  return span;
}

export function hydraterSchemas(racine) {
  racine.querySelectorAll(".carte-svg[data-agrandir]").forEach(activerAgrandissement);
  racine.querySelectorAll(".carte-svg[data-svg]").forEach(zone => {
    const chemin = zone.dataset.svg;
    delete zone.dataset.svg;
    chargerSvg(chemin).then(markup => {
      zone.innerHTML = markup;
      const largeur = markup.match(/viewBox='[-\d.]+ [-\d.]+ ([\d.]+)/);
      // Taille naturelle (1 pt ≈ 1,33 px) comme plafond : un petit schéma
      // ne doit pas être étiré à toute la largeur de la carte.
      if (largeur) zone.firstElementChild.style.maxWidth = `${Math.round(largeur[1] * 4 / 3)}px`;
      activerAgrandissement(zone);
    }).catch(() => {
      zone.innerHTML = `<img src="${echapper(chemin)}" alt="">`;
    });
  });
}

// Le thème situe la question : « Rendement » seul est ambigu, « Rendement
// — Transformateur » ne l'est plus. 45 labels du corpus sont partagés par
// plusieurs cartes ; sans ce repère, elles posent la même question.
function situer(c, data) {
  const t = data && data.themes && data.themes.find(x => x.code === c.theme);
  return t ? `${c.theme} · ${t.titre}` : c.theme;
}

// « Puissance apparente » -> « la puissance apparente ». Sans article, la
// phrase de repli sonne comme une note télégraphique, pas comme une question.
// Les sigles et noms propres (THD, Laplace) gardent leur casse et leur forme.
const FEMININ = /^(puissance|tension|valeur|impédance|admittance|fréquence|vitesse|capacité|résistance|énergie|marge|constante|loi|relation|chute|section|charge|pente|durée|période|force|masse|surface|densité|intensité|inductance|réactance|conductance|erreur|bande|phase|pulsation)/i;

function avecArticle(label) {
  const s = String(label ?? "").trim();
  if (!s) return s;

  const premier = s.split(/[\s(]/)[0];
  // Sigle ou symbole : on l'introduit sans article pour éviter « le THD ? »
  // mal accordé sur des cas imprévus.
  if (premier === premier.toUpperCase() && premier.length > 1) return s;

  const bas = s.charAt(0).toLowerCase() + s.slice(1);
  if (/^[aeiouéèêâîôûh]/i.test(bas)) return "l'" + bas;
  return (FEMININ.test(bas) ? "la " : "le ") + bas;
}

// Les conditions peuvent être longues ; au recto, une phrase suffit à
// cadrer sans encombrer.
function premierePhrase(s) {
  const t = String(s ?? "").trim();
  const m = t.match(/^(.{0,120}?[.;])\s/);
  // Un « ; » qui clôt la phrase retenue devient un point.
  return m ? m[1].replace(/[\s\u00a0\u202f]*;$/, ".") : (t.length > 130 ? t.slice(0, 127) + "…" : t);
}

// Les grandeurs en jeu cadrent la réponse sans la livrer : c'est la forme
// même d'une question de concours (« quelle relation lie P, U, I et cos φ ? »).
// On liste les symboles du membre de DROITE — le membre de gauche est la
// grandeur cherchée, l'afficher reviendrait à donner le début de la réponse.
const SYMBOLES_IGNORES = new Set([
  "frac", "dfrac", "sqrt", "cdot", "times", "sum", "int", "left", "right",
  "quad", "qquad", "text", "approx", "leq", "geq", "neq", "pm", "ldots",
  "underline", "overline", "bar", "log", "ln", "exp", "arg", "max", "min", "pi",
  "langle", "rangle", "lfloor", "rfloor", "cos", "sin", "tan",
  "mathrm", "mathbf", "mathit", "operatorname", "displaystyle", "infty",
  "cdots", "implies", "Rightarrow", "Longrightarrow", "Leftrightarrow", "iff", "to", "xrightarrow",
  "bigl", "bigr", "Bigl", "Bigr", "underbrace", "lim", "arctan", "arcsin", "arccos", "partial",
  "mathcal", "oplus", "ll", "gg", "simeq", "propto", "equiv", "le", "ge",
]);

function grandeursEnJeu(latex) {
  const s = String(latex ?? "");
  // Plusieurs relations séparées par « ; », \qquad ou « \quad\text{avec}\quad » :
  // le membre de gauche de chacune est une grandeur cherchée, on garde les droites.
  // Les bornes d'une somme ou d'une intégrale (indice muet, ∞) ne sont pas des grandeurs.
  const droite = s.split(/;|\\qquad|\\quad\s*\\text\{\s*(?:avec|et|soit|où)\s*\}\s*\\quad/)
    .map(r => {
      // Membre de droite de l'égalité, à défaut de l'inégalité (≤, ≥, <, >),
      // à défaut encore de l'approximation (≈).
      const rel = r.includes("=") ? /=/.exec(r)
        : /\\[lg](?:eq?|t)(?![a-zA-Z])|[<>]/.exec(r) ?? /\\approx(?![a-zA-Z])/.exec(r);
      return rel ? r.slice(rel.index + rel[0].length) : r;
    })
    .join(" ")
    .replace(/\\text\{[^{}]*\}/g, " ")          // texte courant : pas de grandeurs
    .replace(/\\mathcal\{[^{}]*\}/g, " ")       // opérateur (transformée de Laplace…)
    // Constantes et opérateurs écrits en romain : e de l'exponentielle, d du
    // différentiel, j imaginaire, matrice identité. Hors indice seulement.
    .replace(/(?<!_)\\mathrm\{d\}\s*t(?![A-Za-z])/g, " ")
    .replace(/(?<!_)\\mathrm\{(?:e|d|j|Id)\}/g, " ")
    .replace(/(?<![A-Za-z\\])d(?=\\[a-zA-Z])/g, " ")   // différentielle dτ, dθ
    // Variable d'une fonction, f(t) ou H(p) : ce n'est pas une grandeur de plus.
    .replace(/\(\s*[tp]\s*\)/g, " ")
    .replace(/\\(sum|prod|int)\s*(_\{[^{}]*\}|_\w)?\s*(\^\{[^{}]*\}|\^\w)?/g, " ");
  const vus = new Set();
  const sortie = [];

  // Symboles simples (V, I, R…) éventuellement suivis d'un indice court,
  // et commandes grecques (\varphi, \omega, \eta…). Un symbole surmonté
  // ou souligné (\bar U, \hat V, \underline{Z}) reste un seul symbole, décor compris :
  // sans sa barre, la valeur moyenne Ū se lirait comme une tension U.
  const motif = /\\(bar|overline|underline|hat|widehat|tilde|vec|dot|ddot|mathbf)\s*(?:\{([A-Za-z]|\\[a-zA-Z]+)\}|([A-Za-z]))(?:_\{([^{}]{1,10})\}|_([A-Za-z0-9]))?|\\([a-zA-Z]+)(?:_\{([^{}]{1,10})\}|_\\mathrm\{([^{}]{1,10})\}|_(\\[a-zA-Z]+|[A-Za-z0-9]))?|([A-Za-z])(?:_\{([^{}]{1,10})\}|_\\mathrm\{([^{}]{1,10})\}|_([A-Za-z0-9]))|(?<![A-Za-z\\])([A-Za-z])(?![A-Za-z])/g;
  let m;
  while ((m = motif.exec(droite)) !== null) {
    let sym;
    if (m[1]) {
      const indice = m[4] ?? m[5];
      sym = `\\${m[1]}{${m[2] ?? m[3]}}` + (indice ? `_{${indice}}` : "");
    } else if (m[6]) {
      // Commande grecque, indice compris : ω₀ et ω_c ne sont pas ω.
      if (SYMBOLES_IGNORES.has(m[6])) continue;
      const indice = m[7] ?? (m[8] ? `\\mathrm{${m[8]}}` : m[9]);
      sym = "\\" + m[6] + (indice ? `_{${indice}}` : "");
    } else if (m[10]) {
      // Lettre indicée, accolades ou non : K_c n'est ni K ni c.
      const indice = m[11] ?? (m[12] ? `\\mathrm{${m[12]}}` : m[13]);
      sym = `${m[10]}_{${indice}}`;
    } else {
      if (m[14] === "j") continue;      // unité imaginaire, pas une grandeur
      sym = m[14];
    }
    if (!vus.has(sym)) { vus.add(sym); sortie.push(sym); }
    if (sortie.length >= 6) break;      // au-delà, ce n'est plus un indice
  }
  // Ordre alphabétique : l'ordre d'apparition épellerait la relation.
  const cle = t => t.replace(/\\(?:bar|overline|underline|hat|widehat|tilde|vec|dot|ddot|mathbf|mathrm)(?![a-zA-Z])/g, "")
    .replace(/[\\{}]/g, "");
  return sortie.sort((a, b) => cle(a).localeCompare(cle(b), "fr", { sensitivity: "base" }));
}

// Extrait d'épreuve : étiquette de session, système support, données,
// schéma inline (dessiné pour l'écran, suit le thème), question isolée.
function rendreExerciceRecto(c, data) {
  const donnees = (c.donnees || []).map(d => `<li>${texteAvecMaths(d)}</li>`).join("");
  return `<p class="contexte">${echapper(situer(c, data))}</p>
          <p class="etiquette-sujet">Dans l'esprit du sujet ${echapper(c.annee)} · ${echapper(c.epreuve)}</p>
          <p class="vedette">${texteAvecMaths(c.titre)}</p>
          <p class="systeme">${echapper(c.systeme)}</p>
          ${donnees ? `<ul class="donnees">${donnees}</ul>` : ""}
          <div class="carte-svg schema-exo" role="img" aria-label="Schéma de l'exercice"
               data-agrandir="1">${c.schema || ""}</div>
          <p class="consigne">Question</p>
          <p class="enonce-schema">${texteAvecMaths(c.question)}</p>`;
}

function rendreExerciceVerso(c) {
  const paragraphes = String(c.reponse || "").split(/\n+/)
    .map(t => `<p>${texteAvecMaths(t)}</p>`).join("");
  const attendus = (c.attendus || []).map(a => `<li>${texteAvecMaths(a)}</li>`).join("");
  return `<p class="consigne">Corrigé</p>
          <div class="reponse-exo">${paragraphes}</div>
          ${attendus ? `<p class="consigne">Ce que le jury attend</p><ul class="attendus">${attendus}</ul>` : ""}`;
}

export function rendreRecto(c, data) {
  if (c.type === "exercice") return rendreExerciceRecto(c, data);
  const contexte = `<p class="contexte">${echapper(situer(c, data))}</p>`;

  if (c.type === "formule") {
    // Question rédigée si elle existe, sinon repli sur la formulation
    // générique : aucune carte ne doit se retrouver sans énoncé.
    const question = (c.question && c.question.trim())
      ? texteAvecMaths(c.question.trim())
      : `Quelle est la relation donnant ${texteAvecMaths(avecArticle(c.label))} ?`;

    const symboles = grandeursEnJeu(c.latex);
    const enJeu = symboles.length >= 2
      ? `<p class="en-jeu">Grandeurs en jeu : ${symboles.map(s => maths(s, false)).join(" ")}</p>`
      : "";

    // Le contexte d'application vient des fiches (régime, hypothèses).
    const cadre = c.conditions
      ? `<p class="cadre">${texteAvecMaths(premierePhrase(c.conditions))}</p>` : "";

    // « sans dimension » ne se lit pas après « en » : « Résultat sans dimension ».
    const sansDim = /^sans dimension\s*(.*)$/i.exec(c.unites || "");
    const indice = !c.unites ? ""
      : sansDim
        ? `<p class="indice">Résultat sans dimension${texteAvecMaths(
            /^[,;]/.test(sansDim[1]) ? ", ou en " + sansDim[1].replace(/^[,;]\s*/, "")
              : sansDim[1] ? " " + sansDim[1] : "")}</p>`
        : `<p class="indice">Résultat attendu en ${texteAvecMaths(c.unites)}</p>`;

    const freq = c.presence
      ? `<p class="freq">${echapper(c.presence)}</p>` : "";

    return `${contexte}
            <p class="vedette">${question}</p>
            ${cadre}${enJeu}${indice}${freq}`;
  }
  if (c.type === "piege") {
    // Deux formes de piège. « erreur » : l'énoncé décrit une erreur réelle
    // (« oublier de changer le signe… ») et la question du jury est pourquoi
    // c'est faux et que faut-il écrire. « vigilance » : l'énoncé du corpus
    // est une règle juste ; demander « pourquoi est-ce faux ? » serait
    // absurde, on demande donc de retrouver le piège et la règle à partir
    // du seul titre, et l'énoncé devient la réponse.
    if (c.forme === "vigilance") {
      return `${contexte}
              <p class="consigne">Point de vigilance</p>
              <p class="vedette">${texteAvecMaths(c.titre)}</p>
              <p class="consigne">Quel est le piège ? Énoncez la règle.</p>`;
    }
    return `${contexte}
            <p class="titre-piege">${texteAvecMaths(c.titre)}</p>
            <p class="consigne">Erreur fréquente</p>
            <p class="enonce">${texteAvecMaths(c.piege)}</p>
            <p class="consigne">Pourquoi est-ce faux ? Que faut-il écrire ?</p>`;
  }
  // schema : reconnaissance et calcul montrent le SVG au recto ; trace montre
  // le label au recto et garde le SVG (la réponse) pour le verso.
  if (c.niveau === "trace") {
    return `${contexte}
            <p class="consigne">Tracez de mémoire</p>
            <p class="vedette">${texteAvecMaths(c.label)}</p>`;
  }
  // Question propre à la carte si elle existe : la question générique
  // « quel montage ? » ne convient pas à un chronogramme ou à un spectre.
  const question = (c.question && c.question.trim())
    ? texteAvecMaths(c.question.trim())
    : (c.niveau === "calcul"
        ? "Calculez la grandeur demandée."
        : "Quel montage ? Quelle relation entrée/sortie ?");
  return `${contexte}
          ${svg(c.svg, "schéma à identifier")}
          <p class="enonce-schema">${question}</p>`;
}

// 28 des 344 formules du corpus ne sont pas des formules pures mais des
// phrases mixtes : « $h = 6k \pm 1$ : rangs $5, 7, 11$ », « $f_{MLI}$ :
// typiquement 1 à 20 kHz ». Les passer en bloc à KaTeX le fait échouer et
// afficher la source en rouge. On distingue donc les deux cas.
function rendreFormule(latex) {
  const s = String(latex ?? "").trim();
  if (!s) return "";

  // Contenu mixte reconnaissable : des délimiteurs $ subsistent, signe que
  // le parseur n'a pas pu les retirer (ils encadraient plusieurs segments).
  if (s.includes("$")) {
    return `<p class="formule-mixte">${texteAvecMaths(s)}</p>`;
  }
  // Formule pure : centrée, en display, comme une équation de manuel.
  return maths(s, true);
}

// Ce que l'auto-évaluation doit vérifier : une formule « sue » dont on a
// oublié les unités ou le domaine de validité n'est pas sue. La liste ne
// cite que ce que la carte contient réellement.
function criteres(c) {
  const items = ["la relation"];
  if (c.unites) items.push("les unités");
  if (c.conditions) items.push("les conditions d'application");
  if (items.length < 2) return "";
  return `<p class="criteres">Pour « su », il fallait : ${items.join(" · ")}</p>`;
}

export function rendreVerso(c) {
  if (c.type === "exercice") return rendreExerciceVerso(c);
  if (c.type === "formule") {
    const u = c.unites
      ? `<p class="unites">Unités : ${texteAvecMaths(c.unites)}</p>` : "";
    const cond = c.conditions
      ? `<p class="conditions"><strong>Conditions :</strong> ${texteAvecMaths(c.conditions)}</p>` : "";
    return `${rendreFormule(c.latex)}${u}${cond}${criteres(c)}`;
  }
  if (c.type === "piege") {
    const err = c.erreur_type
      ? `<p class="erreur-type">${texteAvecMaths(c.erreur_type)}</p>` : "";
    // Vigilance : l'énoncé est la règle, le champ regle la développe.
    if (c.forme === "vigilance") {
      const complement = c.regle && c.regle.trim() !== c.piege.trim()
        ? `<p class="complement">${texteAvecMaths(c.regle)}</p>` : "";
      return `<p class="regle">${texteAvecMaths(majuscule(c.piege))}</p>${complement}${err}`;
    }
    // Erreur : la règle corrige l'énoncé. Sans règle rédigée, l'énoncé
    // formulé en négatif reste la seule réponse disponible.
    if (!c.regle) {
      return `<p class="consigne">L'erreur à éviter :</p>
              <p class="regle">${texteAvecMaths(majuscule(c.piege))}</p>${err}`;
    }
    return `<p class="regle">${texteAvecMaths(c.regle)}</p>${err}`;
  }
  // schema : le verso porte le nom du montage ET la réponse rédigée (relation,
  // rôle, relations clés) — sans elle, l'utilisateur ne peut pas se noter.
  // trace : le SVG est la réponse, il n'apparaît qu'ici. reconnaissance et
  // calcul : le SVG est déjà visible au recto juste au-dessus, on ne le
  // répète pas.
  const reponse = c.reponse
    ? `<p class="regle">${texteAvecMaths(c.reponse)}</p>` : "";
  if (c.niveau === "trace") {
    return `${svg(c.svg, c.label)}<p class="vedette">${texteAvecMaths(c.label)}</p>${reponse}`;
  }
  return `<p class="vedette">${texteAvecMaths(c.label)}</p>${reponse}`;
}
