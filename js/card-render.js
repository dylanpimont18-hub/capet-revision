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

export function rendreRecto(c) {
  if (c.type === "formule") {
    return `<p class="consigne">Énoncez la relation :</p>
            <p class="vedette">${texteAvecMaths(c.label)}</p>`;
  }
  if (c.type === "piege") {
    return `<p class="titre-piege">${texteAvecMaths(c.titre)}</p>
            <p class="enonce">${texteAvecMaths(c.piege)}</p>
            <p class="consigne">Légitime, ou non ?</p>`;
  }
  // schema : reconnaissance et calcul montrent le SVG au recto ; trace montre
  // le label au recto et garde le SVG (la réponse) pour le verso.
  if (c.niveau === "trace") {
    return `<p class="consigne">Tracez de mémoire :</p>
            <p class="vedette">${texteAvecMaths(c.label)}</p>`;
  }
  const question = c.niveau === "calcul"
    ? "Calculez la grandeur demandée."
    : "Quel montage ? Quelle relation entrée/sortie ?";
  return `${svg(c.svg, "schéma à identifier")}
          <p class="consigne">${question}</p>`;
}

export function rendreVerso(c) {
  if (c.type === "formule") {
    const u = c.unites
      ? `<p class="unites">Unités : ${texteAvecMaths(c.unites)}</p>` : "";
    const cond = c.conditions
      ? `<p class="conditions"><strong>Conditions :</strong> ${texteAvecMaths(c.conditions)}</p>` : "";
    return `${maths(c.latex)}${u}${cond}`;
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
