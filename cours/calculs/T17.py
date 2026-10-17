"""Applications numériques du chapitre T17, refaites en Python.

    python3 cours/calculs/T17.py

Chaque bloc reprend une valeur publiée dans cours/textes/T17.html ; un
écart supérieur à la demi-unité du dernier chiffre publié fait échouer le
script (tolérance relative explicite pour une valeur annoncée « environ »).
"""
from decimal import Decimal
from math import sqrt, acos, sin, ceil

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



RHO = 22.5e-3  # Ω·mm²/m, cuivre, NF C 15-100
verifier("§2 : R_u en 50 mm² (mΩ/m)", 22.5 / 50, 0.45)
D_HAUT, D_CATALOGUE = 20, 12 * 1.2  # courbe D : haut de bande normalisé (NF EN 60898-1), iC60 (2020-E2)

# ── §6 : schéma TT ───────────────────────────────────────────────────────
verifier("§6 : I_d en TT (A)", 230 / (30 + 10), 5.75)
verifier("§6 : U_c en TT (V)", 30 * 230 / (30 + 10), 172.5)
verifier("§6 : sensibilité maximale, « environ » (A)", 50 / 30, 1.67)
verifier("§6 : U_c en TN à sections égales (V)", 0.8 * 230 * 1 / (1 + 1), 92)
verifier("§8 : limite de sélectivité, bas de bande de l'amont C63 (A)", 5 * 63, 315)

# ── Exemple chiffré ──────────────────────────────────────────────────────
Pa = 11e3 / 0.89
c = 0.85
s = sqrt(1 - c ** 2)
IB = Pa / (sqrt(3) * 400 * c)
verifier("Ex. 1 : puissance absorbée (W)", Pa, 12360, tol=0.001)
verifier("Ex. 1 : I_B (A)", IB, "21.0")
verifier("Ex. 2 : R_u en 6 mm² (mΩ/m)", 22.5 / 6, 3.75)
verifier("Ex. 2 : sin φ", s, 0.527)
dU6 = sqrt(3) * IB * 120 * (RHO / 6 * c + 0.08e-3 * s)
verifier("Ex. 2 : terme entre parenthèses (mΩ/m)", 3.75 * c + 0.08 * s, 3.23)
verifier("Ex. 2 : ΔU en 6 mm² (V)", dU6, 14.1)
verifier("Ex. 2 : ΔU avec 3,23 mΩ/m (V)", sqrt(3) * 21.0 * 120 * 3.23e-3, 14.1)
verifier("Ex. 2 : ΔU en 6 mm² (%)", 100 * dU6 / 400, 3.52)
verifier("Ex. 2 : total avec l'amont (%)", 100 * dU6 / 400 + 2, 5.52)
verifier("Ex. 2 : R_u en 10 mm² (mΩ/m)", 22.5 / 10, 2.25)
dU10 = sqrt(3) * IB * 120 * (RHO / 10 * c + 0.08e-3 * s)
verifier("Ex. 2 : ΔU en 10 mm² (V)", dU10, 8.53)
verifier("Ex. 2 : ΔU en 10 mm² (%)", 100 * dU10 / 400, 2.13)
verifier("Ex. 2 : total avec l'amont (%)", 100 * dU10 / 400 + 2, 4.13)
verifier("Ex. 2 : terme réactif (V)", sqrt(3) * IB * 120 * 0.08e-3 * s, 0.18)
vrai("Ex. 3 : I_B ≤ 25 A ≤ I_z = 50 A", IB <= 25 <= 50)
verifier("Ex. 3 : appel au démarrage (A)", 7 * IB, 147)
vrai("Ex. 3 : courbe C, appel dans la bande 125–250 A", 5 * 25 <= 7 * IB <= 10 * 25)
vrai("Ex. 3 : courbe D, appel sous 250 A", 7 * IB < 10 * 25)
verifier("Ex. 3 : haut de la bande D (A)", D_HAUT * 25, 500)
verifier("Ex. 3 : appel rapporté au calibre", 7 * IB / 25, 5.9)
verifier("Ex. 4 : I_d (A)", 230 / 50, 4.6)
verifier("Ex. 4 : U_c (V)", 40 * 230 / 50, 184)
verifier("Ex. 4 : sensibilité maximale (A)", 50 / 40, 1.25)
verifier("Ex. 4 : U_c au seuil de 300 mA (V)", 40 * 0.3, 12)
IdTN = 0.8 * 230 / (RHO * 120 * (1 / 10 + 1 / 10))
verifier("Ex. 5 : I_d en TN-S (A)", IdTN, 341)
verifier("Ex. 5 : seuil haut de la courbe D (A)", D_HAUT * 25, 500)
vrai("Ex. 5 : I_d < 500 A, coupure non garantie", IdTN < D_HAUT * 25)
verifier("Ex. 5 : longueur maximale en courbe D, « environ » (m)", 0.8 * 230 / (RHO * D_HAUT * 25 * 0.2), 82, tol=0.005)
verifier("Ex. 5 : haut de la bande catalogue (A)", D_CATALOGUE * 25, 360)
vrai("Ex. 5 : I_d < 360 A aussi", IdTN < D_CATALOGUE * 25)
vrai("Ex. 5 : courbe C sûre à 250 A < I_d", 10 * 25 < IdTN)
Id16 = 0.8 * 230 / (RHO * 120 * (1 / 16 + 1 / 16))
verifier("Ex. 5 : I_d en 16 mm², phases et PE, « environ » (A)", Id16, 545, tol=0.002)
vrai("Ex. 5 : 545 A > 500 A", Id16 > D_HAUT * 25)

# ── Auto-test ────────────────────────────────────────────────────────────
S2 = sqrt(3) * 400 * 15
verifier("Q2 : S (VA)", S2, 10392)
verifier("Q2 : P (W)", 0.8 * S2, 8314)
verifier("Q2 : Q (var)", 0.6 * S2, 6235)
verifier("Q3 : R_u (mΩ/m)", 22.5 / 2.5, 9)
verifier("Q3 : ΔU (V)", 2 * 16 * 30 * 9e-3, 8.64)
verifier("Q3 : ΔU (%)", 100 * 2 * 16 * 30 * 9e-3 / 230, 3.76)
verifier("Q4 : local sec (A)", 50 / 100, 0.5)
verifier("Q4 : local mouillé (mA)", 1000 * 25 / 100, 250)
In5 = 1000 / 230
verifier("Q5 : courant nominal (A)", In5, 4.35)
verifier("Q5 : appel (A)", 12 * In5, 52)
vrai("Q5 : C de 30 à 60 A contient l'appel ; D, de 60 à 120 A, au-dessus", 30 <= 12 * In5 <= 60 and 12 * In5 < 10 * 6)
verifier("Q5 : haut de la bande D (A)", D_HAUT * 6, 120)
verifier("Q6 : longueur maximale (m)", 0.8 * 230 / (RHO * 160 * 0.8), 63.9)

# ── Méthode : 2020-E2, Q20 et Q21 ────────────────────────────────────────
In_ac0 = 750 / 0.86 / (230 * 0.8)
verifier("2020-E2 : câble alternatif (%)", 100 * 2 * In_ac0 * (RHO / 1.5 * 0.8) * 6 / 230, "0.30")
Pdc = 370 / 0.86
Idc = Pdc / 12
verifier("2020-E2 : puissance absorbée du moteur continu (W)", Pdc, 430)
verifier("2020-E2 : courant sous 12 V (A)", Idc, 35.9)
dUdc = RHO * 15 / 16 * Idc
verifier("2020-E2 : ΔU, formule du sujet (V)", dUdc, 0.76)
verifier("2020-E2 : ΔU, formule du sujet (%)", 100 * dUdc / 12, 6.3)
verifier("2020-E2 : ΔU, aller et retour (%)", 200 * dUdc / 12, 12.6)
vrai("2020-E2 : section minimale 20,2 mm² → 25 ; 40,3 mm² → 50",
     16 < RHO * 15 * Idc / (0.05 * 12) <= 25 and 35 < 2 * RHO * 15 * Idc / (0.05 * 12) <= 50)
verifier("2020-E2 : en 24 V, formule du sujet (%)", 100 * RHO * 15 / 16 * (Pdc / 24) / 24, 1.6)
verifier("2020-E2 : en 24 V, aller et retour (%)", 200 * RHO * 15 / 16 * (Pdc / 24) / 24, 3.2)

# ── Méthode : 2024-E2, B5 à B9 ───────────────────────────────────────────
from math import pi
RL, XL, It = 20e-3 * 0.85, 1.2e-3 * 0.85 * 2 * pi * 50, 258
verifier("2024-E2 : R_L (mΩ)", 1000 * RL, "17.0")
verifier("2024-E2 : X_L (Ω)", XL, "0.320")
def UD(R, X):
    PT, QT = 178.3e3 + 3 * R * It ** 2, 3 * X * It ** 2
    return sqrt(PT ** 2 + QT ** 2) / (sqrt(3) * It)
verifier("2024-E2 : U_D (V)", UD(RL, XL), 431)
verifier("2024-E2 : ΔU/U_D (%)", 100 * (UD(RL, XL) - 400) / UD(RL, XL), 7.2)
verifier("2024-E2 : formule approchée (V)", sqrt(3) * It * RL, 7.6)
verifier("2024-E2 : formule approchée (%)", 100 * sqrt(3) * It * RL / 400, 1.9)
verifier("2024-E2 : à résistance nulle (%)", 100 * (UD(0, XL) - 400) / UD(0, XL), 5.6)
Vr = 400 / sqrt(3)
UD0 = sqrt(3) * abs(complex(Vr, XL * It))
verifier("2024-E2 : à résistance nulle, chapitre 3 (%)", 100 * (UD0 - 400) / UD0, 5.9)
vrai("2024-E2 : X_L près de vingt fois R_L", 17 < XL / RL < 20)
vrai("2024-E2 : 20 mΩ/km ↔ de l'ordre de 1 000 mm² de cuivre", 800 < 22.5 / 0.020 < 1200)

# ── Méthode : 2024-E1, Q38 à Q43 ─────────────────────────────────────────
S_rail = 150 * 11 + 79 * 11
Rl = 0.13 / S_rail
verifier("2024-E1 : section du rail (mm²)", S_rail, 2519)
verifier("2024-E1 : R_ℓ (Ω/m)", Rl, 5.16e-5)
for x in (100.0, 300.0, 500.0, 800.0):
    R1, R2 = 2 * Rl * x, 2 * Rl * (1000 - x)
    vrai(f"2024-E1 : R1 // R2 = 2 Rℓ L (1 − x/L) x/L pour x = {x:.0f} m",
         abs(R1 * R2 / (R1 + R2) - 2 * Rl * 1000 * (1 - x / 1000) * x / 1000) < 1e-12)
verifier("2024-E1 : chute admise (V)", 0.05 * 72, 3.6)
verifier("2024-E1 : L_max (m)", 2 * 3.6 / (Rl * 100), 1395)
verifier("2024-E1 : chute pour L = 1,1 km (V)", Rl * 1100 * 100 / 2, 2.84)
verifier("2024-E1 : idem (%)", 100 * Rl * 1100 * 100 / 2 / 72, 3.9)
verifier("2024-E1 : courant moyen (A)", 7200 / 72, 100)

# ── Méthode : disjoncteurs (2020-E2, 2021-E2) ────────────────────────────
In_ac = 750 / 0.86 / (230 * 0.8)
verifier("2020-E2 : I_n du moteur alternatif (A)", In_ac, 4.74)
verifier("2020-E2 : démarrage 3 I_n (A)", 3 * In_ac, 14.2)
verifier("2020-E2 : bas de la bande D du D6A (A)", 0.8 * 12 * 6, 57.6)
vrai("2020-E2 : iC60 40 A ≥ 35,9 A", 40 >= Idc)
verifier("2021-E2 : I_n du moteur de 90 kW (A)", 90e3 / (0.942 * sqrt(3) * 400 * 0.86), 160)

# ── Méthode : départs-moteurs (2022-E1, 2017-E2) ─────────────────────────
vrai("2022-E1 : 4,8 A dans 3–12 A et dans 1,25–5 A", 3 <= 4.8 <= 12 and 1.25 <= 4.8 <= 5)
verifier("2017-E2 : réchauffeur (A)", 3000 / 230, "13.0")
verifier("2017-E2 : hydromassage (A)", 2250 / 0.86 / 230, 11.4)
verifier("2017-E2 : circulation (A)", 260 / 0.8 / 230, 1.41)
vrai("2017-E2 : 1,41 A hors de 0,35–1,4 A, dans 1,25–5 A", 260 / 0.8 / 230 > 1.4 and 1.25 <= 260 / 0.8 / 230 <= 5)
vrai("2017-E2 : 13,0 A dans 4,5–18 A ; 11,4 A dans 3–12 A", 4.5 <= 3000 / 230 <= 18 and 3 <= 2250 / 0.86 / 230 <= 12)
verifier("2017-E2 : 2 HP (kW), « environ »", 2 * 0.7457, 1.5, tol=0.01)

# ── Méthode : 2018-E2, différentiel ──────────────────────────────────────
verifier("2018-E2 : courant de défaut au plus (A)", 230 / 150, 1.5)
verifier("2018-E2 : sensibilité maximale (mA)", 1000 * 50 / 150, 333)
verifier("2018-E2 : U_c au seuil de 300 mA (V)", 150 * 0.3, 45)
verifier("2018-E2 : U_c au seuil de 500 mA (V)", 150 * 0.5, 75)

# ── Méthode : bilans (2017-E2, 2015-E1, 2018-E2) ─────────────────────────
P1, Q1 = 3000 + 260, 260 * 0.6 / 0.8
S1 = sqrt(P1 ** 2 + Q1 ** 2)
verifier("2017-E2 : S de la phase 1 (kVA)", S1 / 1000, 3.27)
verifier("2017-E2 : phase 1 chargée (kVA)", 16 / 3 + S1 / 1000, 8.60)
verifier("2017-E2 : équivalent triphasé (kVA)", 3 * (16 / 3 + S1 / 1000), 25.8)
verifier("2015-E1 : puissance maximale (W)", 800 + 500 + 1.5 * 2000 + 75, 4375)
verifier("2015-E1 : courant du groupe (A)", 7250 / 230, 31.5)
verifier("2015-E1 : courant du shelter (A)", 4375 / 230, 19)
vrai("2015-E1 : 31,5 A ≤ 32 A et > 16 A", 16 < 7250 / 230 <= 32)
vrai("2017-E2 : 24 kVA < 25,8 kVA ≤ 30 kVA", 24 < 3 * (16 / 3 + S1 / 1000) <= 30)
E15 = (800 * 0.7 + 500 * 0.3 + 2000 * 0.6 + 75 * 0.5) * 24 / 0.27 / 1000  # kW·h de combustible par jour
vrai("2015-E1 : seul le GPL sous 42 kg de CO₂ (GPL, essence, gazole)", E15 * 0.231 < 42 < min(E15 * 0.264, E15 * 0.271))
verifier("2018-E2 : puissance apparente, « environ » (kVA)", 46 * 200 / 0.84 / 1000, 11, tol=0.01)
vrai("2018-E2 : 16 luminaires par phase sous 4 kVA, 3 × 4 kVA ≥ 11 kVA", 16 * 200 / 0.84 <= 4000 and 3 * 4 >= 46 * 200 / 0.84 / 1000)
verifier("2018-E2 : courant d'un module de 4 kVA (A)", 4000 / 230, 17)

print()
print("Aucun écart." if not ECARTS else f"{len(ECARTS)} écart(s) : " + " ; ".join(ECARTS))
