"""Applications numériques du chapitre T23, refaites en Python.

    python3 cours/calculs/T23.py

Chaque bloc reprend une valeur publiée dans cours/textes/T23.html ; un
écart supérieur à la demi-unité du dernier chiffre publié fait échouer le
script (tolérance relative explicite pour une valeur annoncée « environ »).
"""
from decimal import Decimal
from math import sqrt, log10, pi

ECARTS = []


def verifier(nom, calcule, publie, tol=None):
    """Écart admis : la demi-unité du dernier chiffre publié, sauf tolérance relative explicite."""
    # Une valeur publiée avec un zéro final (« 0,580 ») se passe en chaîne.
    texte = publie if isinstance(publie, str) else repr(publie)
    publie = float(texte)
    if tol is None:
        ecart_admis = 0.5 * 10 ** Decimal(texte).as_tuple().exponent * 1.000001
    else:
        ecart_admis = tol * max(abs(publie), 1e-12)
    ok = abs(calcule - publie) <= ecart_admis
    print(f"{'ok ' if ok else 'ÉCART'} {nom:62s} calculé {calcule:.6g} · publié {publie:g}")
    if not ok:
        ECARTS.append(nom)


def vrai(nom, ok):
    print(f"{'ok ' if ok else 'ÉCART'} {nom}")
    if not ok:
        ECARTS.append(nom)




R0, ALPHA = 100.0, 3.85e-3

# ── §2 : température ─────────────────────────────────────────────────────
verifier("§2 : PT100 à 100 °C (Ω)", R0 * (1 + ALPHA * 100), 138.5)
verifier("§2 : sensibilité R0·α (Ω/°C)", R0 * ALPHA, 0.385)
verifier("§2 : erreur 2 fils pour 1 Ω (°C)", 1 / (R0 * ALPHA), 2.6)
verifier("§2 : résolution DS18B20 12 bits (°C)", 1 / 16, 0.0625)

# ── §3 : jauges et pont ──────────────────────────────────────────────────
verifier("§3 : 1 + 2ν pour ν = 0,3", 1 + 2 * 0.3, 1.6)
verifier("§3 : ΔR/R pour ε = 500 µm/m, K = 2", 2 * 500e-6, 1e-3)
verifier("§3 : ΔR sur 350 Ω (Ω)", 2 * 500e-6 * 350, 0.35)
def exact(x):  # (VA − VB)/Vcc, x = ΔR/R0
    return x / (2 * (2 + x))
for x in (1e-3, 0.385):
    vrai(f"§3 : erreur relative de la linéarisation ≈ x/2 pour x = {x}", abs((x / 4 - exact(x)) / exact(x) - x / 2) < 1e-9)
verifier("§3 : erreur pour une jauge (%)", 100 * 1e-3 / 2, 0.05)
vrai("§3 : près de 20 % pour une PT100 à 100 °C", 18 < 100 * 0.385 / 2 < 20)
# demi-pont et pont complet
d_ = 0.01
VA = (1 + d_) / 2; VB = 0.5
vrai("§3 : demi-pont, Vcc ΔR/(2R0) exact", abs((VA - VB) - d_ / 2) < 1e-12)
VB2 = (1 - d_) / 2
vrai("§3 : pont complet, Vcc ΔR/R0 exact", abs((VA - VB2) - d_) < 1e-12)
# compensation : toutes les branches multipliées par le même facteur
k_ = 1.02
R1, R2, R3, R4 = 100, 100, 100, 100.3
vrai("§3 : rapports inchangés si toutes les branches varient ensemble",
     abs((R4 / (R1 + R4) - R3 / (R2 + R3)) - (k_ * R4 / (k_ * R1 + k_ * R4) - k_ * R3 / (k_ * R2 + k_ * R3))) < 1e-12)

# ── §4 : boucle 4–20 mA ──────────────────────────────────────────────────
verifier("§4 : résistance de boucle maximale (Ω)", (24 - 12) / 0.020, 600)
verifier("§4 : 4 mA sur 250 Ω (V)", 250 * 0.004, 1)
verifier("§4 : 20 mA sur 250 Ω (V)", 250 * 0.020, 5)

# ── §5 : codeur, denture ─────────────────────────────────────────────────
verifier("§5 : incréments par tour, 500 points", 4 * 500, 2000)

# ── §6 et §7 ─────────────────────────────────────────────────────────────
verifier("§7 : gain d'un premier ordre à fe/2 pour fc = fe/10", 1 / sqrt(26), 0.2, tol=0.03)

# ── Exemple chiffré ──────────────────────────────────────────────────────
verifier("Ex. 1 : R à 85 °C (Ω)", R0 * (1 + ALPHA * 85), 132.7)
rf = 0.0175 * 12 / 0.5
verifier("Ex. 2 : un fil (Ω)", rf, 0.42)
verifier("Ex. 2 : deux fils (Ω)", 2 * rf, 0.84)
verifier("Ex. 2 : erreur (°C)", 2 * rf / (R0 * ALPHA), 2.2)
verifier("Ex. 2 : tolérance classe A à 85 °C, « de l'ordre de » (°C)", 0.15 + 0.002 * 85, 0.3, tol=0.1)
I85 = 4 + 16 * 85 / 150
verifier("Ex. 3 : courant (mA)", I85, 13.07)
verifier("Ex. 3 : tension (V)", 250 * I85 / 1000, 3.27)
verifier("Ex. 3 : tension disponible à 20 mA (V)", 24 - 250 * 0.020, 19)
verifier("Ex. 4 : N à 85 °C", 27648 * 250 * I85 / 1000 / 10, 9032, tol=0.0001)
verifier("Ex. 4 : N à 4 mA", 27648 * 0.1, 2765)
verifier("Ex. 4 : N à 20 mA", 27648 * 0.5, 13824)
verifier("Ex. 4 : pas utilisés", 27648 * 0.4, 11059)
verifier("Ex. 4 : résolution (°C)", 150 / (27648 * 0.4), 0.014)
U12 = 12000 * 10 / 27648
verifier("Ex. 5 : tension pour 12 000 (V)", U12, "4.340")
verifier("Ex. 5 : courant (mA)", U12 / 250 * 1000, 17.36)
verifier("Ex. 5 : température (°C)", (U12 / 250 * 1000 - 4) / 16 * 150, 125.3)
verifier("Ex. 5 : fausse lecture pour 0 mA (°C)", (0 - 4) / 16 * 150, -37.5)

# ── Auto-test ────────────────────────────────────────────────────────────
verifier("Q2 : 50 °C (Ω)", R0 * (1 + ALPHA * 50), 119.25)
verifier("Q2 : −20 °C (Ω)", R0 * (1 - ALPHA * 20), 92.3)
verifier("Q3 : pression (bar)", (11.2 - 4) / 16 * 10, 4.5)
dR = 2 * 500e-6 * 350
verifier("Q4 : ΔR (Ω)", dR, 0.35)
verifier("Q4 : tension linéarisée (mV)", 1000 * 10 / 4 * dR / 350, 2.5)
verifier("Q4 : tension exacte (mV)", 1000 * 10 / 2 * dR / (700 + dR), 2.499)
verifier("Q4 : écart (%)", 100 * ((10 / 4 * dR / 350) / (10 / 2 * dR / (700 + dR)) - 1), 0.05)
verifier("Q4 : gain", 5 / (10 / 4 * dR / 350), 2000)
verifier("Q5 : fréquence (kHz)", 1024 * 3000 / 60 / 1000, 51.2)
verifier("Q5 : résolution (°)", 360 / 4096, 0.088)
verifier("Q6 : gain à 900 Hz", 1 / sqrt(1 + 81), 0.11)
verifier("Q6 : en dB", 20 * log10(1 / sqrt(82)), -19)

print()
print("Aucun écart." if not ECARTS else f"{len(ECARTS)} écart(s) : " + " ; ".join(ECARTS))
