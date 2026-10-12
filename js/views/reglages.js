// app/js/views/reglages.js
import {
  exporter, importer, reinitialiser, charger, chargerActivite, calculerSerie,
  lireDateEcrit, ecrireDateEcrit, joursAvant,
} from "../store.js";
import { pluriel, dateISO } from "../texte.js";

const DELAI_CONFIRMATION = 6000;   // fenêtre pendant laquelle « Confirmer » reste armé

export function vueReglages(racine, data, ctx = {}) {
  const progression = charger();
  const suivies = Object.keys(progression).length;
  const acquises = Object.values(progression)
    .filter(p => p && p.repetitions >= 2 && p.facilite >= 2.3).length;
  const serie = calculerSerie(chargerActivite());
  const dateEcrit = lireDateEcrit();
  const j = joursAvant(dateEcrit);

  racine.innerHTML = `
    <div class="carte">
      <p class="consigne">Réglages</p>
      <p class="vedette">Votre progression</p>
      <ul class="bilan stats" aria-label="Progression">
        <li><strong>${suivies}</strong><span>vues / ${data.cards.length}</span></li>
        <li class="su"><strong>${acquises}</strong><span>acquises</span></li>
        <li><strong>${serie}</strong><span>${serie > 1 ? "jours de suite" : "jour de suite"}</span></li>
      </ul>
    </div>

    <section class="carte" aria-labelledby="t-ecrit">
      <h2 class="consigne" id="t-ecrit">Date de l'écrit</h2>
      <p class="texte-doux" id="ecrit-info">${j === null
        ? "Indiquez la date de l'épreuve : un compte à rebours s'affiche sur l'écran Réviser."
        : j >= 0 ? `Dans ${pluriel(j, "jour")}.` : "Cette date est passée."}</p>
      <input type="date" id="date-ecrit" class="champ" value="${dateEcrit || ""}"
             min="${dateISO()}" aria-label="Date de l'écrit">
    </section>

    <section class="carte" aria-labelledby="t-sauve">
      <h2 class="consigne" id="t-sauve">Sauvegarde</h2>
      <p class="texte-doux">Aucun serveur : la progression vit sur cet iPhone.
        Partagez un fichier de sauvegarde vers Fichiers ou iCloud Drive avant
        tout changement d'appareil.</p>
      <div class="pile-boutons">
        <button class="revelateur" id="partager">Partager la sauvegarde</button>
        <button class="bouton-secondaire" id="copier">Copier le texte</button>
      </div>
      <p class="texte-doux" style="margin-top:var(--e4)">Pour restaurer, choisissez un fichier
        de sauvegarde ou collez son contenu.</p>
      <div class="pile-boutons">
        <label class="bouton-secondaire">
          <input type="file" id="fichier" class="sr-only" accept=".json,application/json">
          Restaurer depuis un fichier
        </label>
        <button class="bouton-secondaire" id="coller">Coller un export</button>
      </div>
      <div id="zone-collage" hidden>
        <textarea id="zone" rows="6" aria-label="Contenu de l'export" spellcheck="false"
                  autocapitalize="off" autocorrect="off"></textarea>
        <button class="bouton-secondaire" id="restaurer" style="margin-top:var(--e2)">Restaurer ce texte</button>
      </div>
      <p id="msg" class="message" role="status" aria-live="polite"></p>
    </section>

    <section class="carte carte-danger" aria-labelledby="t-raz">
      <h2 class="consigne" id="t-raz">Zone sensible</h2>
      <p class="texte-doux">Efface la progression et la série de jours sur cet appareil.
        Irréversible sans sauvegarde.</p>
      <button class="bouton-danger" id="raz">Effacer toute la progression</button>
    </section>`;

  const msg = document.getElementById("msg");
  const zoneCollage = document.getElementById("zone-collage");
  const zone = document.getElementById("zone");
  const dire = (texte, ok = true) => {
    msg.textContent = texte;
    msg.classList.toggle("erreur", !ok);
  };

  /* ─── Date de l'écrit ────────────────────────────────────────────────── */
  document.getElementById("date-ecrit").onchange = (e) => {
    const v = e.target.value || null;
    ecrireDateEcrit(v);
    const jj = joursAvant(v);
    document.getElementById("ecrit-info").textContent = jj === null
      ? "Indiquez la date de l'épreuve : un compte à rebours s'affiche sur l'écran Réviser."
      : jj >= 0 ? `Dans ${pluriel(jj, "jour")}.` : "Cette date est passée.";
  };

  /* ─── Export ─────────────────────────────────────────────────────────── */
  const nomFichier = () => `capet-progression-${dateISO()}.json`;

  document.getElementById("partager").onclick = async () => {
    const texte = exporter();
    const fichier = new File([texte], nomFichier(), { type: "application/json" });
    // Feuille de partage iOS : « Enregistrer dans Fichiers », AirDrop, Mail…
    if (navigator.canShare && navigator.canShare({ files: [fichier] })) {
      try {
        await navigator.share({ files: [fichier], title: "Sauvegarde CAPET" });
        dire("Sauvegarde partagée.");
        return;
      } catch (e) {
        if (e && e.name === "AbortError") return;   // l'utilisateur a fermé la feuille
      }
    }
    // Repli : téléchargement classique.
    const url = URL.createObjectURL(fichier);
    const a = Object.assign(document.createElement("a"), { href: url, download: nomFichier() });
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    dire("Fichier de sauvegarde téléchargé.");
  };

  document.getElementById("copier").onclick = async () => {
    const texte = exporter();
    try {
      await navigator.clipboard.writeText(texte);
      dire("Sauvegarde copiée dans le presse-papiers.");
    } catch {
      // Presse-papiers refusé : on montre le texte, sélectionné, à copier à la main.
      zoneCollage.hidden = false;
      zone.value = texte;
      zone.focus();
      zone.select();
      dire("Copiez ce texte et conservez-le.");
    }
  };

  /* ─── Import ─────────────────────────────────────────────────────────── */
  const restaurer = (texte) => {
    if (importer(texte)) {
      dire("Progression restaurée.");
      // Les autres écrans relisent le stockage à chaque affichage : rien à recharger.
      if (ctx.naviguer) setTimeout(() => ctx.naviguer(), 0);
    } else {
      dire("Import refusé : ce contenu n'est pas une sauvegarde valide.", false);
    }
  };

  document.getElementById("fichier").onchange = async (e) => {
    const f = e.target.files && e.target.files[0];
    if (!f) return;
    try {
      restaurer(await f.text());
    } catch {
      dire("Impossible de lire ce fichier.", false);
    }
    e.target.value = "";
  };

  document.getElementById("coller").onclick = () => {
    zoneCollage.hidden = false;
    zone.value = "";
    zone.focus();
    dire("Collez le contenu d'une sauvegarde, puis touchez « Restaurer ce texte ».");
  };

  document.getElementById("restaurer").onclick = () => {
    if (!zone.value.trim()) { dire("La zone est vide.", false); return; }
    restaurer(zone.value);
  };

  /* ─── Réinitialisation en deux temps, sans dialogue natif ────────────── */
  const raz = document.getElementById("raz");
  let arme = null;
  raz.onclick = () => {
    if (!arme) {
      raz.textContent = "Confirmer l'effacement";
      raz.classList.add("arme");
      dire("Touchez de nouveau pour effacer. Rien n'est fait tant que vous ne confirmez pas.");
      arme = setTimeout(() => {
        arme = null;
        raz.textContent = "Effacer toute la progression";
        raz.classList.remove("arme");
        dire("");
      }, DELAI_CONFIRMATION);
      return;
    }
    clearTimeout(arme);
    arme = null;
    reinitialiser();
    dire("Progression effacée.");
    if (ctx.naviguer) setTimeout(() => ctx.naviguer(), 600);
  };
}
