// app/js/views/reglages.js
import { exporter, importer, reinitialiser, charger } from "../store.js";

export function vueReglages(racine, data) {
  const n = Object.keys(charger()).length;
  racine.innerHTML = `
    <div class="carte">
      <p class="vedette">Réglages</p>
      <p class="consigne">${n} carte(s) suivie(s) sur ${data.cards.length}.
        Aucun serveur : l'export est votre seule sauvegarde.</p>
      <div class="actions" style="margin-bottom:.6rem">
        <button id="exp">Exporter</button>
        <button id="imp">Importer</button>
      </div>
      <button class="revelateur" id="raz" style="background:var(--rate)">
        Tout réinitialiser</button>
      <p id="msg" class="consigne"></p>
      <textarea id="zone" rows="6" style="width:100%;display:none;
        background:var(--bg);color:var(--ink);border:1px solid var(--rule);
        border-radius:8px;padding:.5rem"></textarea>
    </div>`;

  const zone = document.getElementById("zone");
  const msg = document.getElementById("msg");

  document.getElementById("exp").onclick = () => {
    zone.style.display = "block";
    zone.value = exporter();
    zone.select();
    msg.textContent = "Copiez ce texte et conservez-le.";
  };

  document.getElementById("imp").onclick = () => {
    if (zone.style.display === "none" || !zone.value.trim()) {
      zone.style.display = "block";
      zone.value = "";
      msg.textContent = "Collez un export puis cliquez de nouveau sur Importer.";
      return;
    }
    msg.textContent = importer(zone.value)
      ? "Progression restaurée. Rechargez la page."
      : "Import refusé : le contenu n'est pas un export valide.";
  };

  document.getElementById("raz").onclick = () => {
    if (confirm("Effacer toute la progression ? Action irréversible.")) {
      reinitialiser();
      msg.textContent = "Progression effacée.";
    }
  };
}
