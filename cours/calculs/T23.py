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

# ── Méthode : 2025-E1 ────────────────────────────────────────────────────
Vcc = 5.0
F_ = [0, 5e3, 10e3, 15e3]
i_ = [0.0416667, 0.0416647, 0.0416627, 0.0416607]
R_ = [Vcc / i for i in i_]
verifier("2025-E1 Q56 : R0 (Ω)", R_[0], 120, tol=1e-4)
KR = (R_[-1] - R_[0]) / 15e3
verifier("2025-E1 Q56 : K_R (Ω/N)", KR, 1.15e-6, tol=0.01)
verifier("2025-E1 Q56 : ΔR/R0 à 15 kN", KR * 15e3 / 120, "0.00014")
verifier("2025-E1 : puissance dans la jauge sous 5 V (W)", 5 ** 2 / 120, 0.21)
F59 = 1380 * 9.81
verifier("2025-E1 Q59 : effort (N)", F59, 13538)
dR59 = 1.147e-6 * F59
verifier("2025-E1 Q59 : ΔR (Ω)", dR59, 0.0155)
V59 = 1.0 / 4 * dR59 / 120
verifier("2025-E1 Q59 : V_A − V_B (V)", V59, 3.23e-5, tol=0.005)
verifier("2025-E1 Q59 : K_A", 5 / V59, 1.55e5, tol=0.01)
verifier("2025-E1 Q59 : K_A (dB)", 20 * log10(5 / V59), 104)
verifier("2025-E1 Q26 : pas sur 24 bits (µV)", 1e6 * 10 / (2 ** 24 - 1), 0.6)
# ── 2021-E1 ──────────────────────────────────────────────────────────────
verifier("2021-E1 Q21 : F (N)", 90 / 0.3, 300)
verifier("2021-E1 Q22 : masse (kg)", 300 / 9.81, 30.6)
Iq = pi * 0.0275 ** 4 / 64
verifier("2021-E1 Q23 : I (m⁴)", Iq, 2.81e-8, tol=0.005)
verifier("2021-E1 Q23 : flèche (µm)", 1e6 * 300 * 0.082 ** 3 / (3 * 200e9 * Iq), 9.8)
verifier("2021-E1 Q26 : K_cod (m/incrément)", 2 * pi * 0.18 / 500, 2.26e-3, tol=0.003)
# ── 2024-E2, 2023-E1, 2021-E2 ────────────────────────────────────────────
verifier("2024-E2 D4 : pente (mA/°C)", 16 / 220, 0.0727)
verifier("2024-E2 D4 : ordonnée (mA)", 4 + 16 * 20 / 220, 5.45)
verifier("2023-E1 Q47 : sensibilité (mA/°)", 8 / 23, 0.348)
vrai("2023-E1 Q47 : 4 mA à −23°, 20 mA à +23°", abs(12 + 8 / 23 * -23 - 4) < 1e-9 and abs(12 + 8 / 23 * 23 - 20) < 1e-9)
vrai("2023-E1 Q50 : sensibilité doublée", abs((16 / 23) / (8 / 23) - 2) < 1e-12)
verifier("2021-E2 : courant, mA par cm", 16 / 200, 0.08)
verifier("2021-E2 : N par cm", 625 * 0.08, 50)
verifier("2021-E2 : V par point (m³)", 6.25 / 50, 0.125)
verifier("2021-E2 : N plein", 0.95 * 1000 / 0.125, 7600)
verifier("2021-E2 : N vide", 0.05 * 1000 / 0.125, 400)
verifier("2021-E2 : N à 1,6 m", 50 * 160, 8000)
# ── Codeurs ──────────────────────────────────────────────────────────────
verifier("2024-E1 Q22 : résolution (mm)", 1000 * 2 * pi * 0.20 / 400, 3.14)
v = 60 / 3.6
verifier("2024-E1 Q23 : vitesse (m/s)", v, 16.67)
verifier("2024-E1 Q23 : tr/s", v / (2 * pi * 0.20), 13.26)
verifier("2024-E1 Q23 : fréquence par voie (kHz)", 100 * v / (2 * pi * 0.20) / 1000, 1.33)
verifier("2023-E2 D2 : impulsions", int(680 / 0.15), 4533)
vrai("2023-E2 D2 : 13 bits pour 4 534 positions", 2 ** 12 < 4534 <= 2 ** 13)
vrai("2023-E2 D2 : 4 533 = 0x11B5", 4533 == 0x11B5)
verifier("2023-E2 D3 : pas sur 8 bits (mm)", 2 ** 5 * 0.15, 4.8)
vrai("2023-E2 D3 : 4 533 >> 5 = 0x8D", 4533 >> 5 == 0x8D)
verifier("2023-E2 D5 : 1 000 tr/min (rad/s)", 1000 * 2 * pi / 60, 104.7)
verifier("2023-E2 D5 : K_GT (V·s/rad)", 5 / (1000 * 2 * pi / 60), 0.0477)
verifier("2020-E1 Q12 : pas (mm)", pi * 3.18, 9.99)
verifier("2020-E1 Q12 : dents", round(9390 / (pi * 3.18)), 940)
verifier("2020-E1 Q15 : fréquence (Hz)", 24 * 240 / 60, 96)
# ── Choix et chaînes ─────────────────────────────────────────────────────
verifier("2020-E2 Q6 : erreur sans compensation à 23 °C (%)", -1.90 * 2, -3.8)
verifier("2020-E2 : 659 mol/m³ de NaCl (g/l)", 659 * 58.44 / 1000, 38.5)
verifier("2022-E1 Q24 : quantum (mV)", 1000 * 3.5 / 4096, 0.854)
verifier("2022-E1 Q24 : N pour 1 V", round(1 / (3.5 / 4096)), 1170)
vrai("2022-E1 Q24 : 1 170 = 0x492", 1170 == 0x492)
verifier("2022-E1 Q24 : tension pour 0xAF (V)", 0xAF * 3.5 / 4096, "0.150")
verifier("2022-E1 Q24 : tension Peltier (V)", 2 * 0xAF * 3.5 / 4096, "0.30")
verifier("2022-E1 Q26 : 3 mA dans 23,7 Ω (mV)", 23.7 * 3, 71.1)
verifier("2022-E1 Q17 : 0x0336", 0x0336, 822)
verifier("2022-E1 Q17 : température (°C)", 0x0336 / 16, 51.375)
verifier("2023-E2 F2 : 22,4 V / 10", 22.4 / 10, 2.24)
verifier("2023-E2 F2 : 21,8 V / 10", 21.8 / 10, 2.18)
verifier("2023-E2 F4 : quantum (mV)", 1000 * 4 / 1024, 3.9)
verifier("2023-E2 F4 : mV par point", 1000 * (2.24 - 2.18) / 10, 6)
verifier("2023-E2 F4 : résolution (%)", (4 / 1024) / 0.006, 0.65)

print()
print("Aucun écart." if not ECARTS else f"{len(ECARTS)} écart(s) : " + " ; ".join(ECARTS))
