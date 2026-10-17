"""Applications numériques du chapitre T15, refaites en Python.

    python3 cours/calculs/T15.py

Chaque bloc reprend une valeur publiée dans cours/textes/T15.html ; un
écart supérieur à la demi-unité du dernier chiffre publié fait échouer le
script (tolérance relative explicite pour une valeur annoncée « environ »).
"""
from decimal import Decimal
from math import sqrt, ceil

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


g = 9.81

# ── §1 : grandeurs ───────────────────────────────────────────────────────
verifier("§1 : 1 kW·h en MJ", 1000 * 3600 / 1e6, 3.6)
# figure 2 : durées de décharge aux bords des zones (t = E/P, en h)
for nom, Pmax, Emin in (("plomb", 400, 25), ("NiMH", 1000, 55), ("Li-ion", 3000, 90)):
    vrai(f"Fig. 2 : {nom}, quelques minutes au plus fort ({60 * Emin / Pmax:.1f} min)", 1 < 60 * Emin / Pmax < 5)
vrai("Fig. 2 : Li-ion, plus d'une heure à 200 W/kg", 270 / 200 > 1)
vrai("Fig. 2 : supercondensateurs, d'une seconde à quelques dizaines de secondes",
     0.4 < 2 / 15000 * 3600 < 1 and 30 < 10 / 1000 * 3600 < 40)

# ── §4 : chaîne de rendements (figure 6) ─────────────────────────────────
eta = 0.96 * 0.95 * 0.95 * 0.93
verifier("§4 : énergie aux panneaux pour 1 kW·h livré (kW·h)", 1 / eta, "1.241")
verifier("§4 : entrée de l'onduleur (kW·h)", 1 / 0.93, "1.075")
verifier("§4 : entrée de la batterie (kW·h)", 1 / (0.93 * 0.95 ** 2), "1.191")
verifier("§4 : pertes du chargeur (kW·h)", 1 / eta - 1 / (0.93 * 0.95 ** 2), "0.050")
verifier("§4 : pertes de la batterie (kW·h)", 1 / (0.93 * 0.95 ** 2) - 1 / 0.93, "0.116")
verifier("§4 : pertes de l'onduleur (kW·h)", 1 / 0.93 - 1, "0.075")
verifier("§4 : rendement global, « environ » (%)", 100 * eta, 81, tol=0.01)
verifier("§4 : sous-dimensionnement sans DoD de 70 % (%)", 100 * (1 - 0.7), 30)

# ── §6 : supercondensateurs ──────────────────────────────────────────────
verifier("§6 : énergie utile entre Umax/2 et Umax (%)", 100 * (1 - 0.5 ** 2), 75)
for n in (2, 5, 7):
    vrai(f"§6 : énergie de {n} cellules en série = {n} fois celle d'une cellule",
         abs(0.5 * (3000 / n) * (n * 2.7) ** 2 - n * 0.5 * 3000 * 2.7 ** 2) < 1e-6)

# ── §7 : STEP et hydrogène ───────────────────────────────────────────────
E100 = 1000 * 1 * g * 100
verifier("§7 : 1 m³ tombant de 100 m (MJ)", E100 / 1e6, 0.98)
verifier("§7 : idem (kW·h)", E100 / 3.6e6, 0.27)
EUH = 237e3 * 500 / 3.6e6
verifier("§7 : 500 × 237 (kJ)", 500 * 237, 118500)
verifier("§7 : énergie de 1 kg de H2, « environ » (kW·h)", EUH, 32.9, tol=0.002)
verifier("§7 : PCI de 120 MJ/kg (kW·h/kg)", 120e6 / 3.6e6, 33.3)
verifier("§7 : rendement global de la filière", 0.57 * 0.50, 0.285)
verifier("Fig. 10 : électricité pour 1 kg (kW·h)", EUH / 0.57, 57.7)
verifier("Fig. 10 : électricité restituée (kW·h)", EUH * 0.50, 16.5)
verifier("Fig. 10 : pertes de l'électrolyseur (kW·h)", EUH / 0.57 - EUH, 24.8)
verifier("Fig. 10 : pertes de la pile (kW·h)", EUH * 0.50, 16.5)
V1kg = 500 * 8.314 * (25 + 273.15) / 101300
verifier("§7 : volume de 1 kg de H2 à 1 013 hPa et 25 °C, « environ » (m³)", V1kg, 12, tol=0.03)

# ── Méthode : bilans ─────────────────────────────────────────────────────
verifier("2020-E2 Q9 : instruments (W·h/j)", 40 * 24 + 30 * 1 + 70 * 10, 1690)
verifier("2020-E2 Q14 : avec GPS, pilote, dessalinisateur (W·h/j)", 1690 + 80 * 18 + 40 * 18 + 432 * 1, 4282)
verifier("2018-E1 Q20 : énergie embarquée (W·h)", 8 * 12 * 115, 11040)
P_ = (-19, -14, -9, -4, 8, 15, 22, 31); pc = (2, 3, 15, 23, 30, 17, 7, 3)
vrai("2018-E1 : parts du temps, somme 100 %", sum(pc) == 100)
Pm = sum(p * q for p, q in zip(P_, pc)) / 100
verifier("2018-E1 Q22 : puissance moyenne (kW)", Pm, 4.35)
verifier("2018-E1 Q22 : parcours de 30 min (kW·h)", Pm * 0.5, 2.175)
verifier("2018-E1 Q22 : 20 km, 2 h (kW·h)", Pm * 2, "8.70")
verifier("2018-E1 Q22 : part de l'énergie embarquée (%)", 100 * Pm * 2 / 11.04, 78.8)
vrai("2018-E1 : Id 1.2, décharge ≤ 80 %", Pm * 2 / 11.04 <= 0.80)
verifier("2023-E2 B1 : 3 000 m à 4 km/h (h)", 3 / 4, 0.75)
verifier("2023-E2 B2 : énergie du parcours (kW·h)", 5.6 * 0.75, 4.2)

# ── Méthode : du besoin à la capacité ────────────────────────────────────
Ep = 55 * g * 5
verifier("2020-E1 Q16 : Ep (J), « environ »", Ep, 2698, tol=0.0005)
verifier("2020-E1 Q16 : Ep (W·h)", Ep / 3600, 0.749)
verifier("2020-E1 Q16 : 80 % de Ep (W·h)", 0.8 * Ep / 3600, "0.600")
t_tr = 2 * 20 / 1.5 + 3 * 5 + 5 / 1 + (2 * 5 / g) ** 0.5 + 40
verifier("2020-E1 : durée du trajet (s)", t_tr, 87.7)
E19 = 2 * 200 * 20 / 1.5 + 2 * 48 * 3 * 5 + 1100 * 5 / 1 + 48 * 10 * 5 + 48 * 1 * t_tr - 0.8 * Ep
verifier("2020-E1 Q19 : énergie d'un trajet (J)", E19, 16724)
verifier("2020-E1 Q19 : idem (W·h)", E19 / 3600, 4.645)
E20 = 160 * 4.645 / 0.80
verifier("2020-E1 Q20 : énergie nécessaire (W·h)", E20, 929)
verifier("2020-E1 Q21 : capacité (A·h)", 929 / 48, 19.35)
C15 = 4282 * 2 / (0.7 * 12)
verifier("2020-E2 Q15 : capacité, « environ » (A·h)", C15, 1020, tol=0.001)
verifier("2020-E2 Q15 : batteries GEL12-130, au moins", ceil(C15 / 130), 8)
for E_, Pe_, t_, t80 in ((80e3, 5715, "14.0", 11.2), (60e3, 5672, 10.6, 8.5), (40e3, 5629, 7.11, 5.7)):
    verifier(f"2023-E2 A8 : {E_ / 1e3:.0f} kW·h, durée (h)", E_ / Pe_, t_)
    verifier(f"2023-E2 A8 : {E_ / 1e3:.0f} kW·h à 80 %, durée (h)", 0.8 * E_ / Pe_, t80)
vrai("2023-E2 A9 : 40 kW·h, 7,11 h ≥ 7 h ; à 80 %, il faut 60 kW·h", 40e3 / 5629 >= 7 and 0.8 * 40e3 / 5629 < 7 <= 0.8 * 60e3 / 5672)

# ── Méthode : packs ──────────────────────────────────────────────────────
verifier("2020-E1 Q22 : 48/3,7", 48 / 3.7, 12.97)
verifier("2020-E1 Q22 : 19,35/5,2", 19.35 / 5.2, 3.72)
verifier("2020-E1 Q22 : masse (kg), « environ »", 13 * 4 * 0.092, 4.78)
vrai("2020-E1 Q22 : 52 cellules, 20,8 A·h ≥ 19,35 A·h", 13 * 4 == 52 and 4 * 5.2 >= 19.35)
verifier("2023-E2 C1 : 25/3,6", 25 / 3.6, 6.94)
verifier("2023-E2 C1 : tension de branche (V)", 7 * 3.6, 25.2)
verifier("2023-E2 C1 : résistance de branche (mΩ)", 7 * 15, 105)
verifier("2023-E2 C2 : 400/3,3", 400 / 3.3, 121.2)
vrai("2023-E2 C2 : 121 branches ne suffisent pas", 121 * 3.3 < 400 <= 122 * 3.3)
verifier("2023-E2 C2 : résistance de la batterie (mΩ)", 105 / 122, 0.861)
verifier("2023-E2 C2 : cellules par batterie", 7 * 122, 854)
verifier("2023-E2 C2 : quatre batteries, tension (V)", 4 * 25.2, 100.8)
verifier("2023-E2 C2 : quatre batteries, résistance (mΩ)", 4 * 105 / 122, 3.44)
verifier("2023-E2 F1 : plage de 7 cellules (V)", 7 * 2.5, 17.5)
verifier("2023-E2 F1 : idem, pleine charge (V)", 7 * 4.2, 29.4)
verifier("2025-E2 Q33 : 48/3,69", 48 / 3.69, 13.01)

# ── Méthode : courbe de décharge (2025-E2) ───────────────────────────────
verifier("2025-E2 Q34 : ΔEb (V), notre lecture 4,05 V", 13 * (4.05 - 3.3), 9.8)
verifier("2025-E2 Q34 : bornes de lecture 4,0 V (V)", 13 * (4.0 - 3.3), 9.1)
verifier("2025-E2 Q34 : bornes de lecture 4,1 V (V)", 13 * (4.1 - 3.3), 10.4)
verifier("2025-E2 Q35 : batterie pleine (V)", 52.65, 52.65)
verifier("2025-E2 Q35 : V_DC pleine (V)", 13 * 4.05 / 0.21, 250.7)
verifier("2025-E2 Q35 : écart (%)", 100 * (13 * 4.05 / 0.21 / 230 - 1), "9.0")
verifier("2025-E2 Q35 : à 85 % (V)", 13 * 3.3, 42.9)
verifier("2025-E2 Q35 : V_DC à 85 % (V)", 42.9 / 0.21, 204.3)
verifier("2025-E2 Q35 : écart (%)", 100 * (42.9 / 0.21 / 230 - 1), -11.2)
verifier("2025-E2 Q35 : alpha pour 230 V, pleine, « environ »", 1 - 52.65 / 230, 0.77, tol=0.01)
verifier("2025-E2 Q35 : alpha pour 230 V, à 85 %, « environ »", 1 - 42.9 / 230, 0.81, tol=0.01)

# ── Méthode : supercondensateurs ─────────────────────────────────────────
verifier("2019-E1 Q15 : recharges par jour", 20 * 60 / 6, 200)
verifier("2019-E1 Q15 : cycles en 10 ans", 200 * 365 * 10, 730000)
verifier("2019-E1 Q16 : énergie de climatisation (W·h)", (3000 / 2 * 1 + 1200 / 2 * 6) / 60, 85)
verifier("2019-E1 Q16 : à stocker (W·h)", 85 / 0.94, 90.4)
verifier("2019-E1 Q17 : capacité en fin de vie (F)", 89 * 0.8, 71.2)
E17 = 0.5 * 71.2 * (102 ** 2 - 34 ** 2)
verifier("2019-E1 Q17 : énergie utile (J), « environ »", E17, 329229, tol=1e-5)
verifier("2019-E1 Q17 : idem (W·h)", E17 / 3600, 91.45)
verifier("2019-E1 Q17 : marge sur 91 W·h (%)", 100 * (E17 / 3600 / 91 - 1), 0.5)
verifier("2019-E1 Q18 : puissance de recharge (kW)", 250 * 102 / 1e3, 25.5)
verifier("2019-E1 Q20 : énergie de la batterie (W·h)", 12.8 * 55, 704)
verifier("2019-E1 Q20 : besoin (W·h)", 190 * 3, 570)
verifier("2019-E1 Q20 : décharge (%)", 100 * 570 / 704, 81)
Ec = 0.5 * 1000 * (60 / 3.6) ** 2
verifier("2024-E1 Q50 : énergie cinétique (kJ)", Ec / 1e3, 138.9)
verifier("2024-E1 Q51 : 72/16,2", 72 / 16.2, 4.44)
verifier("2024-E1 Q51 : C_eq (F)", 65 / 5, 13)
verifier("2024-E1 Q51 : U_max (V)", 5 * 16.2, 81)
Ef = 0.5 * 13 * 72 ** 2 + 0.8 * 138.9e3
verifier("2024-E1 Q52 : énergie finale (kJ)", Ef / 1e3, 144.8)
verifier("2024-E1 Q52 : tension finale (V)", sqrt(2 * Ef / 13), 149)
E7281 = 0.5 * 13 * (81 ** 2 - 72 ** 2)
verifier("2024-E1 Q53 : énergie absorbable entre 72 et 81 V (kJ)", E7281 / 1e3, 8.95)
verifier("2024-E1 Q53 : part de l'énergie récupérée (%)", 100 * E7281 / (0.8 * Ec), 8)

# ── Méthode : STEP (2021-E2) ─────────────────────────────────────────────
Ep5 = 1000 * 900 * g * 130
verifier("2021-E2 Q5 : énergie potentielle (GJ)", Ep5 / 1e9, 1.148)
verifier("2021-E2 Q5 : idem (kW·h)", Ep5 / 3.6e6, 318.8)
Et = 0.78 * Ep5 / 3.6e6
verifier("2021-E2 Q6 : énergie turbinée (kW·h)", Et, 248.7)
verifier("2021-E2 Q6 : part de 580 kW·h (%)", 100 * Et / 580, 42.9)
verifier("2021-E2 BP2 : 6 h à 50 kW (kW·h)", 6 * 50, 300)
verifier("2021-E2 Q8 : 1 000 m³ à 160 m³/h (h)", 1000 / 160, 6.25)
verifier("2021-E2 Q9 : contrôle ρgQH, pompe à 76 % (kW)", 1000 * g * 160 / 3600 * 135 / 1e3 / 0.76, 77.4)
verifier("2021-E2 Q9 : pompage de 900 m³ (kW·h)", 76 * 900 / 160, 427.5)
verifier("2021-E2 Q9 : rendement, même volume (%)", 100 * Et / 427.5, 58, tol=0.01)
verifier("2021-E2 Q9 : rendement, 1 000 m³ pompés (%)", 100 * Et / (76 * 1000 / 160), 52, tol=0.01)
verifier("2021-E2 Q27 : énergie restituée (MW·h/an)", 0.25 * 390 * 0.5, 48.75)
verifier("2021-E2 Q28 : 40 % de 390 (MW·h)", 0.40 * 390, 156)
verifier("2021-E2 Q28 : énergie reçue par le village (MW·h)", 156 + 48.75, 204.75)
verifier("2021-E2 Q28 : énergie achetée (MW·h)", 320 - 204.75, 115.25)
verifier("2021-E2 Q28 : coût (€)", 115.25 * 170, 19592.5)
vrai("2021-E2 : 580 kW·h/j ≠ 320 MW·h/an", abs(320e3 / 365 - 580) > 100)

# ── Méthode : hydrogène (2025-E2) ────────────────────────────────────────
verifier("2025-E2 Q8 : énergies de liaison (kJ/mol)", (4 * 461 - 2 * 436 - 498) / 2, 237)
verifier("2025-E2 Q9 : électricité à l'électrolyseur (kW·h)", EUH / 0.57, 57.7)
verifier("2025-E2 Q10 : électricité rendue (kW·h)", 0.50 * EUH, 16.5)
verifier("2025-E2 Q11 : rendement global (%)", 100 * 0.57 * 0.50, 28.5)
verifier("2025-E2 Q12 : volume de 1 kg (m³)", 500 * 8.314 * 298 / 101300, 12.2)
Ej = 1.3e9 / 365 / 1e3
verifier("2025-E2 Q13 : énergie journalière (kW·h)", Ej, 3562)
mj = Ej / 16.46
verifier("2025-E2 Q13 : dihydrogène par jour (kg)", mj, 216)
verifier("2025-E2 Q13 : volume à 1 013 hPa (m³)", mj * 500 * 8.314 * 298 / 101300, 2646)
verifier("2025-E2 Q13 : volume à 500 bar, gaz parfait (m³)", mj * 500 * 8.314 * 298 / 500e5, 5.4)

# ── Méthode : synoptique et rendements ───────────────────────────────────
verifier("2023-E2 B4 : 1/(0,98 × 0,88) (kW·h)", 1 / (0.98 * 0.88), 1.16)
verifier("2023-E2 B5 : 4,2 × 1,16 (kW·h)", 4.2 / (0.98 * 0.88), 4.87)
verifier("2022-E1 Q20 : 150 mA·h / 3 mA, régime C/50", 150 / 3, 50)
verifier("2022-E1 Q26 : 23,7 Ω × 3 mA (mV)", 23.7 * 3, 71)

# ── Exemple chiffré : refuge ─────────────────────────────────────────────
Eac = 60 * 24 + 200 * 5 + 750 * 1 + 40 * 24
verifier("Ex. 1 : consommation journalière (W·h)", Eac, 4150)
Ebj = Eac / 0.93
verifier("Ex. 1 : côté batterie (W·h)", Ebj, 4462)
Enom = 2 * Ebj / (0.80 * 0.95)
verifier("Ex. 2 : énergie nominale (W·h)", Enom, 11743)
verifier("Ex. 2 : capacité sous 48 V (A·h)", Enom / 48, 244.6)
verifier("Ex. 2 : sans DoD, part installée (%)", 100 * (2 * Ebj / 0.95) / Enom, 80)
verifier("Ex. 3 : N_s", 48 / 3.2, 15)
verifier("Ex. 3 : N_p brut", Enom / 48 / 100, 2.45)
Np = ceil(Enom / 48 / 100)
verifier("Ex. 3 : N_p", Np, 3)
vrai("Ex. 3 : deux branches insuffisantes", 2 * 100 < Enom / 48)
verifier("Ex. 3 : nombre de cellules", 15 * Np, 45)
verifier("Ex. 3 : énergie installée (W·h)", 15 * Np * 3.2 * 100, 14400)
verifier("Ex. 3 : masse (kg)", 15 * Np * 2.0, 90)
verifier("Ex. 3 : énergie massique (W·h/kg)", 14400 / 90, 160)
verifier("Ex. 4 : tension mini (V)", 15 * 2.5, 37.5)
verifier("Ex. 4 : tension maxi (V)", 15 * 3.65, 54.75)
verifier("Ex. 4 : à 80 % de décharge (V)", 15 * 3.2, 48)
vrai("Ex. 4 : 48 à 54,75 V dans la plage 40–60 V", 40 <= 48 and 54.75 <= 60)
Ppk = 200 + 750 + 150 + 40
verifier("Ex. 5 : pointe, compresseur à 150 W (W)", Ppk, 1140)
Pb = 1140 / 0.93
verifier("Ex. 5 : puissance batterie (W)", Pb, 1226)
I = Pb / 48
verifier("Ex. 5 : courant (A)", I, 25.5)
verifier("Ex. 5 : régime (C)", I / 300, 0.085)
R = 15 / Np * 0.5e-3
verifier("Ex. 5 : R_pack (mΩ)", R * 1e3, 2.5)
verifier("Ex. 5 : chute de tension (V)", R * I, 0.064)
verifier("Ex. 5 : pertes (W)", R * I ** 2, 1.6)
Eu = 14400 * 0.80 * 0.95
verifier("Ex. 6 : énergie utile (W·h)", Eu, 10944)
verifier("Ex. 6 : autonomie (jours)", Eu / Ebj, 2.45)
verifier("Ex. 6 : marge (%)", 100 * (Eu / Ebj / 2 - 1), 23)
Epb = 2 * Ebj / (0.50 * 0.95)
verifier("Ex. 6 : plomb, énergie nominale (W·h)", Epb, 18789)
verifier("Ex. 6 : plomb à 35 W·h/kg, « environ » (kg)", Epb / 35, 540, tol=0.01)
verifier("Ex. 6 : rapport des masses, « six fois »", Epb / 35 / 90, 6, tol=0.01)
verifier("Ex. 6 : STEP, volume d'eau à 50 m (m³)", 2 * Ebj * 3600 / (1000 * g * 50 * 0.80), 82)

# ── Auto-test ────────────────────────────────────────────────────────────
verifier("Q1 : 12 × 100 (W·h)", 12 * 100, 1200)
verifier("Q1 : utile à 50 % (W·h)", 0.5 * 1200, 600)
verifier("Q2 : N_s", 36 / 3.6, 10)
verifier("Q2 : N_p", 15 / 3, 5)
verifier("Q2 : énergie (W·h)", 36 * 15, 540)
verifier("Q2 : 50 × 3,6 × 3 (W·h)", 50 * 3.6 * 3, 540)
verifier("Q3 : énergie utile (W·h)", 24 * 100 * 0.8, 1920)
verifier("Q3 : puissance prélevée (W)", 60 / 0.9, 66.7)
verifier("Q3 : autonomie (h)", 1920 / (60 / 0.9), 28.8)
verifier("Q4 : C_eq (F)", 3000 / 6, 500)
verifier("Q4 : U_max (V)", 6 * 2.7, 16.2)
verifier("Q4 : E_max (J)", 0.5 * 500 * 16.2 ** 2, 65610)
verifier("Q4 : E_max (W·h)", 0.5 * 500 * 16.2 ** 2 / 3600, 18.2)
verifier("Q4 : utile (J)", 0.75 * 0.5 * 500 * 16.2 ** 2, 49208)
verifier("Q4 : utile (W·h)", 0.75 * 0.5 * 500 * 16.2 ** 2 / 3600, 13.7)
Ep5 = 1000 * 2000 * g * 120
verifier("Q5 : énergie potentielle (GJ)", Ep5 / 1e9, 2.354)
verifier("Q5 : idem (kW·h)", Ep5 / 3.6e6, 654)
verifier("Q5 : pompage (kW·h)", Ep5 / 3.6e6 / 0.8, 817.5)
verifier("Q5 : restitution (kW·h)", 0.85 * Ep5 / 3.6e6, 556)
verifier("Q5 : rendement", 0.80 * 0.85, 0.68)
verifier("Q6 : U_0 (V)", 14 * 3.6, 50.4)
verifier("Q6 : C (A·h)", 10 * 3, 30)
verifier("Q6 : R_pack (mΩ)", 14 / 10 * 20, 28)
verifier("Q6 : régime (C)", 60 / 30, 2)
verifier("Q6 : chute (V)", 0.028 * 60, 1.68)
verifier("Q6 : pertes (W)", 0.028 * 60 ** 2, 101)

print()
print("Aucun écart." if not ECARTS else f"{len(ECARTS)} écart(s) : " + " ; ".join(ECARTS))
