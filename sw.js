// app/sw.js
// Cache-first : l'app doit fonctionner sans réseau (usage en transports).

// Liste générée par build_cards.py : tous les SVG de schémas + les polices
// KaTeX réellement utilisées. Sans elle, un schéma jamais affiché avant la
// coupure réseau donne une image cassée, et les formules tombent sur une
// police de substitution.
importScripts("./sw-assets.js");   // définit self.ASSETS = [...] et self.CACHE_VERSION

// Le nom du cache doit changer quand le contenu précaché change : c'est ce
// changement de littéral qui fait détecter par le navigateur un nouveau
// sw.js, réinstaller le service worker, et laisser `activate` purger
// l'ancien cache. self.CACHE_VERSION vient de sw-assets.js (hash du
// contenu) ; le repli "v1" ne sert qu'à l'absence accidentelle du fichier.
const CACHE = "capet-" + (self.CACHE_VERSION || "v1");

const SOCLE = [
  "./", "./index.html", "./cards.json",
  "./css/style.css",
  "./js/app.js", "./js/store.js", "./js/scheduler.js", "./js/card-render.js",
  "./js/views/reviser.js", "./js/views/priorites.js", "./js/views/reglages.js",
  "./vendor/katex/katex.min.js", "./vendor/katex/katex.min.css",
  "./manifest.webmanifest",
  "./icons/icone-192.png", "./icons/icone-512.png",
  ...(self.ASSETS || []),
];

self.addEventListener("install", e => {
  e.waitUntil(
    caches.open(CACHE)
      // addAll échoue en bloc si un seul fichier manque : on tolère l'absence.
      .then(c => Promise.allSettled(SOCLE.map(u => c.add(u))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys()
      .then(noms => Promise.all(noms.filter(n => n !== CACHE).map(n => caches.delete(n))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  e.respondWith(
    caches.match(e.request).then(hit => hit || fetch(e.request).then(rep => {
      // Les SVG et polices sont mis en cache à la volée.
      if (rep.ok && new URL(e.request.url).origin === location.origin) {
        const copie = rep.clone();
        caches.open(CACHE).then(c => c.put(e.request, copie));
      }
      return rep;
    }).catch(() => {
      // Le fallback ne vaut que pour une NAVIGATION. Renvoyer index.html
      // pour un cards.json ou un .svg absent produirait une erreur de parse
      // JSON opaque au lieu d'un échec lisible.
      if (e.request.mode === "navigate") return caches.match("./index.html");
      return Response.error();
    }))
  );
});
