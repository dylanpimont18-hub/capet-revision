#!/usr/bin/env node
// Vérification d'un chapitre du cours dans un vrai navigateur, au format de
// l'iPhone 17 (393×852, isMobile), en thème clair puis sombre.
//
//   node scripts/verifier_cours.mjs T01 [T07 …]   [--sortie DOSSIER] [--sans-captures]
//   node scripts/verifier_cours.mjs --tous
//
// Lance son propre serveur statique (python3 -m http.server) sur un port
// libre. Contrôle : erreurs console et KaTeX, formules non rendues, largeur
// de défilement = 393, texte SVG ≥ 12 px une fois rendu, formules ≤ 340 px
// et sans débordement, cibles tactiles ≥ 44 px, paragraphes ≤ 6 lignes,
// plein écran d'un schéma ; plus l'écran Catégories, la liste des chapitres
// et l'ouverture d'une carte (#/reviser?carte=…).
// Captures (sauf --sans-captures) : la page découpée en tranches et une
// planche des schémas par thème, dans DOSSIER (défaut : ./captures-cours).
// Playwright : module global (npm root -g) ; Chromium : /opt/pw-browsers.
import { createRequire } from "node:module";
import { execSync, spawn } from "node:child_process";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { createServer } from "node:net";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const RACINE = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const require = createRequire(import.meta.url);
let playwright;
try { playwright = require("playwright"); }
catch { playwright = require(join(execSync("npm root -g").toString().trim(), "playwright")); }
const { chromium } = playwright;

const args = process.argv.slice(2);
const opt = (nom) => { const i = args.indexOf(nom); return i >= 0 ? args[i + 1] : null; };
const SORTIE = resolve(opt("--sortie") || join(RACINE, "captures-cours"));
const CAPTURES = !args.includes("--sans-captures");
const index = JSON.parse(readFileSync(join(RACINE, "cours/index.json"), "utf-8")).chapitres;
let themes = args.filter((a, i) => /^T\d\d$/.test(a) && args[i - 1] !== "--sortie");
if (args.includes("--tous")) themes = index.filter(c => c.disponible).map(c => c.theme);
if (!themes.length) { console.error("Usage : node scripts/verifier_cours.mjs T01 [--tous]"); process.exit(2); }

const LARGEUR = 393, HAUTEUR = 852;
const MODES = [["clair", "clair"], ["sombre", "sombre"]];

function portLibre() {
  return new Promise(ok => { const s = createServer(); s.listen(0, () => { const p = s.address().port; s.close(() => ok(p)); }); });
}

async function attendreServeur(url) {
  for (let i = 0; i < 50; i++) {
    try { const r = await fetch(url); if (r.ok) return; } catch { /* pas encore */ }
    await new Promise(r => setTimeout(r, 100));
  }
  throw new Error("serveur statique injoignable");
}

async function nouvellePage(navigateur, mode, dpr = 1) {
  const contexte = await navigateur.newContext({
    viewport: { width: LARGEUR, height: HAUTEUR }, isMobile: true, hasTouch: true,
    deviceScaleFactor: dpr, serviceWorkers: "block",
  });
  await contexte.addInitScript((t) => { try { localStorage.setItem("capet.theme", t); } catch {} }, mode);
  const page = await contexte.newPage();
  const erreurs = [];
  page.on("console", m => { if (m.type() === "error") erreurs.push(m.text()); });
  page.on("pageerror", e => erreurs.push(String(e)));
  page.on("requestfailed", r => erreurs.push(`requête échouée : ${r.url()}`));
  return { contexte, page, erreurs };
}

// Mesures faites dans la page du chapitre.
function mesurer() {
  const article = document.getElementById("corps-cours");
  const res = { defauts: [], remarques: [], infos: {} };
  const d = (m) => res.defauts.push(m);
  // Largeur de l'appareil, et non window.innerWidth : en mode mobile, le
  // viewport de mise en page s'élargit à la largeur du contenu qui déborde.
  const ecran = screen.width;
  res.infos.innerWidth = window.innerWidth;
  const largeur = Math.max(document.documentElement.scrollWidth, document.body.scrollWidth);
  if (largeur > ecran) d(`défilement horizontal : scrollWidth ${largeur} > ${ecran}`);
  if (window.innerWidth > ecran) d(`viewport élargi par le contenu : ${window.innerWidth} > ${ecran}`);
  res.infos.largeurTexte = Math.round(article.getBoundingClientRect().width);
  // body masque le débordement horizontal : un bloc trop large serait coupé
  // sans faire défiler la page. On compare donc chaque élément à l'écran,
  // sauf ceux qui défilent dans leur propre cadre (formules, tableaux).
  const coupes = new Set();
  document.querySelectorAll("#app *, #corps-cours *, .entete-cours *, .pagination-epreuve *").forEach(e => {
    if (e.closest(".maths-bloc, .table-scroll, svg, .katex")) return;
    const r = e.getBoundingClientRect();
    if (r.width && r.right > ecran + 0.5) {
      const bloc = e.closest("li, p, figure, details, nav, div") || e;
      if (!coupes.has(bloc)) {
        coupes.add(bloc);
        d(`élément coupé à droite (${Math.round(r.right)} > ${ecran}) : ${(bloc.textContent || "").trim().slice(0, 50)}`);
      }
    }
  });

  // KaTeX : erreurs de rendu et formules restées en source.
  article.querySelectorAll(".katex-error").forEach(e => d(`erreur KaTeX : ${e.getAttribute("title") || e.textContent}`));
  const marche = document.createTreeWalker(article, NodeFilter.SHOW_TEXT);
  while (marche.nextNode()) {
    const n = marche.currentNode;
    if (n.parentElement.closest("svg, .katex, script")) continue;
    if (/\$[^$]+\$/.test(n.nodeValue)) d(`formule non rendue : ${n.nodeValue.trim().slice(0, 60)}`);
  }

  // Formules : 340 px au plus, aucune ne déborde de son cadre.
  let maxFormule = 0;
  // Largeur réelle d'une formule : l'union des boîtes .base de KaTeX (le
  // conteneur .katex-html, lui, occupe toute la ligne en mode display).
  const largeurFormule = (racine) => {
    const bases = [...racine.querySelectorAll(".katex-html .base")].map(e => e.getBoundingClientRect());
    if (!bases.length) return racine.getBoundingClientRect().width;
    return Math.max(...bases.map(r => r.right)) - Math.min(...bases.map(r => r.left));
  };
  article.querySelectorAll(".maths-bloc").forEach(b => {
    const w = largeurFormule(b);
    maxFormule = Math.max(maxFormule, w);
    if (w > 340.5) d(`formule de ${Math.round(w)} px > 340 : ${b.textContent.slice(0, 50)}`);
    if (b.scrollWidth > b.clientWidth + 1) d(`formule qui déborde (${b.scrollWidth} > ${b.clientWidth}) : ${b.textContent.slice(0, 50)}`);
  });
  // En ligne : KaTeX coupe après = et + ; aucun bloc insécable (.base) ne
  // doit dépasser la colonne, et une formule de plus de deux tiers de ligne
  // mérite d'être affichée à part (simple remarque).
  const colonne = article.getBoundingClientRect().width;
  article.querySelectorAll(".maths").forEach(m => {
    const plusLarge = Math.max(0, ...[...m.querySelectorAll(".katex-html > .base")].map(b => b.getBoundingClientRect().width));
    if (plusLarge > colonne) d(`formule en ligne insécable de ${Math.round(plusLarge)} px : ${m.textContent.slice(0, 50)}`);
    const hauts = new Set([...m.querySelectorAll(".katex-html > .base")].map(b => Math.round(b.getBoundingClientRect().top)));
    if (hauts.size === 1 && largeurFormule(m) > colonne * 2 / 3) res.remarques.push(`formule en ligne longue (${Math.round(largeurFormule(m))} px) : ${m.textContent.slice(0, 40)}`);
  });
  res.infos.formuleLaPlusLarge = Math.round(maxFormule);

  // Texte des schémas : taille rendue ≥ 12 px.
  let minTexte = Infinity, nFig = 0;
  article.querySelectorAll("figure.schema > svg").forEach(svg => {
    nFig++;
    const vb = svg.viewBox.baseVal;
    const echelle = svg.getBoundingClientRect().width / vb.width;
    svg.querySelectorAll("text, tspan").forEach(t => {
      if (!t.textContent.trim()) return;
      const px = parseFloat(getComputedStyle(t).fontSize) * echelle;
      minTexte = Math.min(minTexte, px);
      if (px < 11.95) d(`texte SVG de ${px.toFixed(1)} px dans ${svg.closest("figure").id} : « ${t.textContent.trim().slice(0, 20)} »`);
    });
    const fig = svg.closest("figure");
    if (!fig.querySelector("figcaption")) d(`${fig.id} sans figcaption`);
    if (!svg.getAttribute("aria-label")) d(`${fig.id} sans aria-label`);
  });
  res.infos.schemas = nFig;
  res.infos.texteSvgMin = +minTexte.toFixed(2);

  // Cibles tactiles : tout ce qui n'est pas un lien dans le fil du texte.
  const cibles = document.querySelectorAll("main a, main button, main summary");
  cibles.forEach(c => {
    const st = getComputedStyle(c);
    if (st.display === "inline" || c.closest("p, li:not(.formules > li):not(.pieges > li), figcaption, td") && st.display === "inline") return;
    const r = c.getBoundingClientRect();
    if (r.width === 0) return;           // replié dans un <details> fermé
    if (r.height < 43.5) d(`cible tactile de ${Math.round(r.height)} px : ${c.className || c.tagName} « ${c.textContent.trim().slice(0, 30)} »`);
  });

  // Paragraphes : 6 lignes d'écran au plus.
  let maxLignes = 0;
  article.querySelectorAll("p").forEach(p => {
    if (p.closest("details:not([open])")) return;
    const lh = parseFloat(getComputedStyle(p).lineHeight);
    const lignes = Math.round(p.getBoundingClientRect().height / lh);
    maxLignes = Math.max(maxLignes, lignes);
    if (lignes > 6) d(`paragraphe de ${lignes} lignes : « ${p.textContent.trim().slice(0, 50)}… »`);
  });
  res.infos.paragrapheLePlusLong = maxLignes;

  // Tableaux : 3 colonnes au plus, sinon dans un cadre défilant.
  article.querySelectorAll("table").forEach(t => {
    const cols = Math.max(...[...t.rows].map(r => r.cells.length));
    if (cols > 3 && !t.closest(".table-scroll")) d(`tableau de ${cols} colonnes hors .table-scroll`);
  });
  res.infos.hauteur = document.documentElement.scrollHeight;
  return res;
}

async function verifierChapitre(navigateur, base, theme) {
  const rapport = { theme, defauts: [], infos: {} };
  for (const [mode] of MODES) {
    const { contexte, page, erreurs } = await nouvellePage(navigateur, mode);
    await page.goto(`${base}/#/cours?theme=${theme}`);
    await page.waitForSelector("#corps-cours figure.schema", { timeout: 15000 });
    await page.waitForFunction(() => document.querySelectorAll("#corps-cours .katex").length > 0);
    // Ouvre les réponses de l'auto-test : elles doivent aussi tenir à l'écran.
    await page.$$eval("#corps-cours details", ds => ds.forEach(x => { x.open = true; }));
    await page.waitForTimeout(300);
    const m = await page.evaluate(mesurer);
    rapport.defauts.push(...m.defauts.map(x => `[${mode}] ${x}`));
    if (mode === "clair") rapport.remarques = m.remarques;
    rapport.infos[mode] = m.infos;

    // Plein écran : toucher le premier schéma l'ouvre, le bouton le ferme.
    await page.$$eval("#corps-cours details", ds => ds.forEach(x => { x.open = false; }));
    await page.locator("#corps-cours figure.schema > svg").first().click();
    if (!(await page.locator(".plein-ecran svg").count())) rapport.defauts.push(`[${mode}] le schéma ne s'ouvre pas en plein écran`);
    else await page.locator(".plein-ecran .fermer").click();

    // Sommaire : un lien mène à sa section sans changer de route.
    await page.locator(".sommaire-epreuve summary").click();
    await page.locator(".sommaire-epreuve a").nth(4).click();
    await page.waitForTimeout(600);
    if (!(await page.evaluate(() => location.hash.startsWith("#/cours")))) rapport.defauts.push(`[${mode}] le sommaire a changé la route`);

    // Couleurs : une flèche d'accent rendue avec la couleur d'accent.
    const couleurs = await page.evaluate(() => {
      const el = document.querySelector('#corps-cours figure.schema [stroke="var(--accent)"]');
      const accent = getComputedStyle(document.documentElement).getPropertyValue("--accent").trim();
      return { trait: el ? getComputedStyle(el).stroke : null, accent };
    });
    rapport.infos[mode].accent = couleurs;

    if (CAPTURES) {
      mkdirSync(SORTIE, { recursive: true });
      await page.evaluate(() => window.scrollTo(0, 0));
      await page.$$eval("#corps-cours details", ds => ds.forEach(x => { x.open = true; }));
      const hauteur = await page.evaluate(() => document.documentElement.scrollHeight);
      const tranche = 1700;
      let n = 0;
      for (let y = 0; y < hauteur; y += tranche, n++) {
        await page.screenshot({
          path: join(SORTIE, `${theme}-${mode}-page-${String(n).padStart(2, "0")}.png`),
          fullPage: true, clip: { x: 0, y, width: LARGEUR, height: Math.min(tranche, hauteur - y) },
        });
      }
      rapport.infos[mode].tranches = n;
    }
    if (erreurs.length) rapport.defauts.push(...erreurs.map(e => `[${mode}] console : ${e}`));
    await contexte.close();
  }

  // Planches des schémas, en haute définition : clair à gauche, sombre à droite.
  if (CAPTURES) {
    const images = {};
    for (const [mode] of MODES) {
      const { contexte, page } = await nouvellePage(navigateur, mode, 2);
      await page.goto(`${base}/#/cours?theme=${theme}`);
      await page.waitForSelector("#corps-cours figure.schema");
      await page.waitForFunction(() => document.querySelectorAll("#corps-cours .katex").length > 0);
      await page.$$eval("#corps-cours details", ds => ds.forEach(x => { x.open = true; }));
      // Les barres fixes masqueraient le bas des figures capturées.
      await page.addStyleTag({ content: ".barre-haut, .barre-bas { display: none !important; }" });
      const figures = await page.locator("#corps-cours figure.schema").all();
      images[mode] = [];
      for (const f of figures) images[mode].push((await f.screenshot()).toString("base64"));
      await contexte.close();
    }
    const parPlanche = 4;
    const { contexte, page } = await nouvellePage(navigateur, "clair", 1);
    for (let i = 0, p = 0; i < images.clair.length; i += parPlanche, p++) {
      const lignes = images.clair.slice(i, i + parPlanche).map((c, k) => `
        <div class="ligne"><span>Figure ${i + k + 1}</span>
          <img src="data:image/png;base64,${c}"><img src="data:image/png;base64,${images.sombre[i + k]}"></div>`).join("");
      await page.setViewportSize({ width: 820, height: 600 });
      await page.setContent(`<style>body{margin:0;background:#888;font:14px sans-serif}
        .ligne{display:grid;grid-template-columns:393px 393px;gap:6px;padding:6px 6px 10px;position:relative}
        .ligne span{position:absolute;left:10px;top:8px;background:#ff0;padding:0 4px;z-index:2}
        img{width:393px;display:block}</style>${lignes}`);
      await page.screenshot({ path: join(SORTIE, `${theme}-schemas-${p + 1}.png`), fullPage: true });
    }
    await contexte.close();
  }
  return rapport;
}

async function verifierEcrans(navigateur, base) {
  const defauts = [];
  for (const [mode] of MODES) {
    const { contexte, page, erreurs } = await nouvellePage(navigateur, mode);
    const largeur = () => page.evaluate(() => Math.max(document.documentElement.scrollWidth, document.body.scrollWidth));
    const petitesCibles = (sel) => page.$$eval(sel, els => els
      .map(e => ({ h: e.getBoundingClientRect().height, t: e.textContent.trim().slice(0, 30), c: e.className }))
      .filter(x => x.h > 0 && x.h < 43.5));

    await page.goto(`${base}/#/categories`);
    await page.waitForSelector(".categorie");
    if ((await largeur()) > LARGEUR) defauts.push(`[${mode}] Catégories : défilement horizontal`);
    if (!(await page.locator(".bouton-cours").count())) defauts.push(`[${mode}] Catégories : pas d'accès à la liste des chapitres`);
    if (!(await page.locator(".lien-cours").count())) defauts.push(`[${mode}] Catégories : pas de bouton « Lire le cours » par catégorie`);
    if (!(await page.locator(".chip-cours").count())) defauts.push(`[${mode}] Catégories : pas de bouton de cours par thème`);
    for (const x of await petitesCibles(".bouton-cours, .lien-cours, .chip-cours")) defauts.push(`[${mode}] Catégories : cible de ${Math.round(x.h)} px (${x.c})`);
    if (CAPTURES) await page.screenshot({ path: join(SORTIE, `categories-${mode}.png`), fullPage: true });

    await page.goto(`${base}/#/cours`);
    await page.waitForSelector(".ligne-chapitre");
    if ((await largeur()) > LARGEUR) defauts.push(`[${mode}] Liste du cours : défilement horizontal`);
    const actif = await page.locator('.barre-bas a[aria-current="page"]').getAttribute("href");
    if (actif !== "#/categories") defauts.push(`[${mode}] Liste du cours : onglet actif ${actif}`);
    for (const x of await petitesCibles("a.ligne-chapitre, .revelateur")) defauts.push(`[${mode}] Liste du cours : cible de ${Math.round(x.h)} px`);
    if (CAPTURES) await page.screenshot({ path: join(SORTIE, `liste-cours-${mode}.png`), fullPage: true });

    const carte = index.find(c => c.disponible).theme + "-f-001";
    await page.goto(`${base}/#/reviser?carte=${carte}`);
    await page.waitForSelector("#zone-carte");
    const retour = await page.locator(".filtre-theme a").getAttribute("href");
    if (!retour.startsWith("#/cours?theme=")) defauts.push(`[${mode}] Carte ${carte} : « Retour » mène à ${retour}`);

    await page.goto(`${base}/#/cours?theme=T99`);
    await page.waitForSelector(".carte .vedette");
    if (erreurs.length) defauts.push(...erreurs.map(e => `[${mode}] console : ${e}`));
    await contexte.close();
  }
  return defauts;
}

const port = await portLibre();
const serveur = spawn("python3", ["-m", "http.server", String(port), "--bind", "127.0.0.1", "--directory", RACINE], { stdio: "ignore" });
const base = `http://127.0.0.1:${port}`;
let code = 0;
try {
  await attendreServeur(`${base}/index.html`);
  const navigateur = await chromium.launch();
  const rapports = [];
  for (const t of themes) rapports.push(await verifierChapitre(navigateur, base, t));
  const ecrans = await verifierEcrans(navigateur, base);
  await navigateur.close();
  for (const r of rapports) {
    console.log(`── ${r.theme} : ${r.defauts.length} défaut(s)`);
    for (const [mode, i] of Object.entries(r.infos)) console.log(`  ${mode} :`, JSON.stringify(i));
    for (const d of r.defauts) console.log(`  ✗ ${d}`);
    for (const x of r.remarques || []) console.log(`  · ${x}`);
    code ||= r.defauts.length ? 1 : 0;
  }
  console.log(`── Écrans (catégories, liste, carte) : ${ecrans.length} défaut(s)`);
  for (const d of ecrans) console.log(`  ✗ ${d}`);
  if (ecrans.length) code = 1;
  if (CAPTURES) {
    writeFileSync(join(SORTIE, "rapport.json"), JSON.stringify({ rapports, ecrans }, null, 1));
    console.log(`Captures : ${SORTIE}`);
  }
} catch (e) {
  console.error(e);
  code = 2;
} finally {
  serveur.kill();
}
process.exit(code);
