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

function svg(chemin, alt) {
  return `<div class="carte-svg"><img src="${echapper(chemin)}" alt="${echapper(alt)}" loading="lazy"></div>`;
}

// Le thème situe la question : « Rendement » seul est ambigu, « Rendement
// — Transformateur » ne l'est plus. 45 labels du corpus sont partagés par
// plusieurs cartes ; sans ce repère, elles posent la même question.
function situer(c, data) {
  const t = data && data.themes && data.themes.find(x => x.code === c.theme);
  return t ? `${c.theme} · ${t.titre}` : c.theme;
}

export function rendreRecto(c, data) {
  const contexte = `<p class="contexte">${echapper(situer(c, data))}</p>`;

  if (c.type === "formule") {
    // Les unités attendues cadrent la réponse sans la donner : savoir qu'on
    // cherche des volts ou des watts fait partie de la question, pas de la
    // réponse. C'est aussi ce que le jury attend d'un candidat.
    const indice = c.unites
      ? `<p class="indice">Résultat attendu en ${texteAvecMaths(c.unites)}</p>` : "";
    return `${contexte}
            <p class="consigne">Énoncez la relation</p>
            <p class="vedette">${texteAvecMaths(c.label)}</p>
            ${indice}`;
  }
  if (c.type === "piege") {
    // Les énoncés du corpus DÉCRIVENT l'erreur (« oublier de changer le
    // signe… »), ils ne proposent pas un cas à juger. Demander « est-ce
    // légitime ? » serait donc incohérent : la réponse est dans la question.
    // La bonne question est celle que le jury pose vraiment — pourquoi
    // c'est faux, et que faut-il écrire à la place.
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
  const question = c.niveau === "calcul"
    ? "Calculez la grandeur demandée."
    : "Quel montage ? Quelle relation entrée/sortie ?";
  return `${contexte}
          ${svg(c.svg, "schéma à identifier")}
          <p class="consigne">${question}</p>`;
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

export function rendreVerso(c) {
  if (c.type === "formule") {
    const u = c.unites
      ? `<p class="unites">Unités : ${texteAvecMaths(c.unites)}</p>` : "";
    const cond = c.conditions
      ? `<p class="conditions"><strong>Conditions :</strong> ${texteAvecMaths(c.conditions)}</p>` : "";
    return `${rendreFormule(c.latex)}${u}${cond}`;
  }
  if (c.type === "piege") {
    // 99 cartes/574 (source réelle) n'ont ni regle ni erreur_type : le corps
    // de section 5 tenait en une seule phrase et _couper() a tout versé dans
    // `piege`, laissant `regle` vide. Ce n'est pas un trou : l'énoncé du
    // piège est déjà la règle, formulée en négatif. On l'affiche donc en
    // position de réponse plutôt que de rendre un verso muet.
    if (!c.regle && !c.erreur_type) {
      return `<p class="consigne">L'erreur à éviter :</p>
              <p class="regle">${texteAvecMaths(c.piege)}</p>`;
    }
    const err = c.erreur_type
      ? `<p class="erreur-type">${texteAvecMaths(c.erreur_type)}</p>` : "";
    return `<p class="regle">${texteAvecMaths(c.regle)}</p>${err}`;
  }
  // schema : trace ne montre le SVG (la réponse) qu'au verso ; reconnaissance
  // et calcul rappellent le label à côté du SVG déjà visible au recto.
  if (c.niveau === "trace") {
    return svg(c.svg, echapper(c.label));
  }
  return `<p class="vedette">${texteAvecMaths(c.label)}</p>${svg(c.svg, c.label)}`;
}
