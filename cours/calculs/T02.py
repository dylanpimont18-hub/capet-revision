"""Applications numériques du chapitre T02, refaites en Python.

    python3 cours/calculs/T02.py

Chaque bloc reprend une valeur publiée dans cours/textes/T02.html ; un
écart de plus de 0,5 % sur la valeur arrondie fait échouer le script.
"""
import cmath
from math import sqrt, pi, acos, tan, sin, cos, degrees, atan, hypot

ECARTS = []


def verifier(nom, calcule, publie, tol=0.005):
    ok = abs(calcule - publie) <= tol * max(abs(publie), 1e-12)
    print(f"{'ok ' if ok else 'ÉCART'} {nom:62s} calculé {calcule:.6g} · publié {publie:g}")
    if not ok:
        ECARTS.append(nom)


w = 2 * pi * 50
V, U = 230.0, 400.0

# ── Idée physique : courant actif et réactif ───────────────────────────
verifier("Pertes en ligne à cos φ = 0,7 / cos φ = 1", 1 / 0.7**2, 2.04, tol=0.01)

# ── §3 : puissance instantanée constante en triphasé équilibré ─────────
phi = 0.6
for t in (0.0, 0.0013, 0.0071):
    p = sum(2 * V * 10 * cos(w * t - k * 2 * pi / 3) * cos(w * t - k * 2 * pi / 3 - phi) for k in range(3))
    verifier(f"p(t) triphasé constant = 3 V I cos φ (t = {t})", p, 3 * V * 10 * cos(phi))

# ── §4 : pompe triphasée (exercice X-2017-01, non officiel) ─────────────
Ip = 1100 / (0.80 * sqrt(3) * U * 0.82)
verifier("Pompe : I_n avec η (A)", Ip, 2.42)
verifier("Pompe : I_n sans η (A)", 1100 / (sqrt(3) * U * 0.82), 1.94)

# ── §5 : relèvement de 0,75 à 0,93 (X-2017-02, non officiel) ────────────
P5 = 120e3
Qc5 = P5 * (tan(acos(0.75)) - tan(acos(0.93)))
verifier("tan φ (0,75)", tan(acos(0.75)), 0.882)
verifier("tan φ' (0,93)", tan(acos(0.93)), 0.395)
verifier("Q_C (kvar)", Qc5 / 1e3, 58.4)
verifier("C étoile (mF)", Qc5 / (3 * w * V**2) * 1e3, 1.17)
verifier("C triangle (µF)", Qc5 / (3 * w * U**2) * 1e6, 387, tol=0.01)
verifier("Courant avant (A)", P5 / (sqrt(3) * U * 0.75), 231)
verifier("Courant après (A)", P5 / (sqrt(3) * U * 0.93), 186)
verifier("Pertes en ligne : rapport (0,75/0,93)²", (0.75 / 0.93) ** 2, 0.65)

# ── §6 : chute de tension, ordre de grandeur de l'approximation ────────
# Cas de 2024-E2 : R = 17 mΩ, X = 0,320 Ω, I = 258 A en phase avec V
Rl, Ll = 20e-3 * 0.85, 1.2e-3 * 0.85
Xl = Ll * w
Vr = U / sqrt(3)
Vd = abs(Vr + complex(Rl, Xl) * 258)
verifier("Exact : U_D (V)", Vd * sqrt(3), 432, tol=0.005)
verifier("Kapp : ΔU ≈ √3 R I (V)", sqrt(3) * Rl * 258, 7.6)
verifier("Terme du second ordre (X I)²/(2 V) (V)", (Xl * 258) ** 2 / (2 * Vr), 14.8, tol=0.01)

# ── §7 : déséquilibre (spa 2017-E2) ────────────────────────────────────
Ph, Pc = 3000.0, 260.0
Qc = Pc * tan(acos(0.8))
S1 = abs(complex(Ph + Pc, Qc))
verifier("Phase 1 : P (W)", Ph + Pc, 3260)
verifier("Phase 1 : Q (var)", Qc, 195)
verifier("Phase 1 : S (VA)", S1, 3266, tol=0.002)
verifier("Phase 1 : I (A)", S1 / V, 14.2)
verifier("Somme naïve des S (VA)", Ph + Pc / 0.8, 3325)
verifier("Existant par phase (kVA)", 16 / 3, 5.33)
verifier("Phase 1 chargée (kVA)", 16 / 3 + S1 / 1e3, 8.60)
verifier("Abonnement minimal (kVA)", 3 * (16 / 3 + S1 / 1e3), 25.8)
verifier("Hydromassage : S (VA)", 2250 / 0.86, 2616)
verifier("Hydromassage : I (A)", 2250 / 0.86 / V, 11.4)
verifier("Hydromassage : Q (var)", 2250 * tan(acos(0.86)), 1335)
verifier("Réchauffeur : I (A)", 3000 / V, 13.0)
verifier("Pompe de circulation : I (A)", 260 / 0.8 / V, 1.41)

# ── §8 : harmoniques ───────────────────────────────────────────────────
I1, c1, thd = 10.0, 0.95, 0.8
Ph8 = V * I1 * c1
Ieff = I1 * sqrt(1 + thd**2)
S8 = V * Ieff
Q18 = V * I1 * sin(acos(c1))
D8 = V * I1 * thd
verifier("AT6 / §8 : I (A)", Ieff, 12.81)
verifier("AT6 / §8 : P (W)", Ph8, 2185)
verifier("AT6 / §8 : S (VA)", S8, 2945)
verifier("AT6 / §8 : FP", Ph8 / S8, 0.742)
verifier("AT6 / §8 : Q1 (var)", Q18, 718)
verifier("AT6 / §8 : D (VA)", D8, 1840)
verifier("S² = P² + Q1² + D²", sqrt(Ph8**2 + Q18**2 + D8**2), S8)

# ── Méthode : 2024-E2 A5 (puissance absorbée par le moteur) ─────────────
verifier("2024-E2 A5 : P_a = √3 U I cos φ (kW)", sqrt(3) * 400 * 229 * 0.85 / 1e3, 134.9)

# ── Méthode : 2020-E2 Q19-Q20 ──────────────────────────────────────────
In20 = 750 / (0.86 * 230 * 0.8)
verifier("2020-E2 Q19 : I_n (A)", In20, 4.74)
verifier("2020-E2 Q19 : I_d = 3 I_n (A)", 3 * In20, 14.2)
verifier("2020-E2 Q19 : seuil magnétique bas 12 × 6 A × 0,8 (A)", 12 * 6 * 0.8, 57.6)
dU20 = 2 * In20 * (22.5 / 1.5 * 0.8) * 6e-3
verifier("2020-E2 Q20 : ΔU AC (V)", dU20, 0.68, tol=0.01)
verifier("2020-E2 Q20 : ΔU AC (%)", dU20 / 230 * 100, 0.30, tol=0.02)
verifier("2020-E2 Q20 : ΔU avec L en m par erreur (V)", 2 * In20 * (22.5 / 1.5 * 0.8) * 6, 683, tol=0.01)

# ── Méthode : 2018-E2 Q13, Q14, Q15, Q27 (DRS 5) ───────────────────────
P1L = 3020 / 15
S1L = P1L / 0.84
verifier("2018-E2 Q13 : P1L (W)", P1L, 201)
verifier("2018-E2 Q13 : S1L = P/FP (VA)", S1L, 240)
verifier("2018-E2 Q13 : Q1L = P tan φ1 (var)", P1L * tan(acos(0.86)), 119)
verifier("2018-E2 Q14 : S_TL (kVA)", 46 * S1L / 1e3, 11.0)
verifier("2018-E2 Q15 : 16 luminaires (kVA)", 16 * S1L / 1e3, 3.8, tol=0.02)
verifier("2018-E2 Q27 : P sous 190 V (W)", 204 * (190 / 230) ** 2, 139)
# ── Méthode : 2018-E2 Q7-Q8 (DRS 3 et DRS 4) ───────────────────────────
verifier("2018-E2 Q8 COMPACTO : D (kVA)", sqrt(1.98**2 - 1.90**2), 0.56, tol=0.01)
verifier("2018-E2 Q8 COMPACTO : P × THD (kVA)", 1.90 * 0.296, 0.56, tol=0.01)
Q1L = 1.93 * tan(acos(0.75))
verifier("2018-E2 Q8 LUBIO : Q1 (kvar)", Q1L, 1.70)
verifier("2018-E2 Q8 LUBIO : D (kVA)", sqrt(2.72**2 - 1.93**2 - Q1L**2), 0.88, tol=0.01)
# ── Méthode : 2015-E1 Q30 ──────────────────────────────────────────────
verifier("2015-E1 Q30 : PERFORM 6500 GAZ, I = S_n/230 (A)", 7250 / 230, 31.5)

# ── Méthode : 2021-E1 Q18 ──────────────────────────────────────────────
verifier("2021-E1 Q18 : L_P si Q0 total (mH)", 3 * 133**2 / (2137 * w) * 1e3, 79.0)
verifier("2021-E1 Q18 : L_P si Q0 par phase (mH)", 133**2 / (2137 * w) * 1e3, 26.3)

# ── Méthode : 2015-E1 Q28 ──────────────────────────────────────────────
verifier("2015-E1 Q28 : puissance maximale (W)", 800 + 500 + 1.5 * 2000 + 75, 4375)

# ── Exemple : 2024-E2 B1 à B9 ──────────────────────────────────────────
Sm = 3 * 230 * 229
Pm, Qm = Sm * 0.85, Sm * sin(acos(0.85))
verifier("B1 : S moteur (kVA)", Sm / 1e3, 158.0)
verifier("B1 : P moteur (kW)", Pm / 1e3, 134.3)
verifier("B1 : Q moteur (kvar)", Qm / 1e3, 83.2)
verifier("B1 : P moteur avec √3 × 400 (kW)", sqrt(3) * 400 * 229 * 0.85 / 1e3, 134.9)
Pch, Qch = Pm + 1e3 + 43e3, Qm + 25.5e3
verifier("B1 : P_charge (kW)", Pch / 1e3, 178.3)
verifier("B1 : Q_charge (kvar)", Qch / 1e3, 108.7)
Sch = abs(complex(178.3e3, 108.7e3))
verifier("B1 : S_charge (kVA)", Sch / 1e3, 208.8)
verifier("B1 : somme naïve des S (kVA)", (Sm + 1e3 + abs(complex(43e3, 25.5e3))) / 1e3, 209.0)
verifier("B2 : I_abs (A)", Sch / (sqrt(3) * 400), 301)
verifier("B2 : F_p", 178.3 / (Sch / 1e3), 0.854)
C = 108.7e3 / (3 * w * 230**2)
verifier("B4 : C (mF)", C * 1e3, 2.18)
verifier("B4 : réactif par condensateur (kvar)", C * w * 230**2 / 1e3, 36.2)
verifier("B4 : C en triangle (µF)", 108.7e3 / (3 * w * 400**2) * 1e6, 721, tol=0.01)
verifier("B5 : R_L (mΩ)", Rl * 1e3, 17)
verifier("B5 : L_L (mH)", Ll * 1e3, 1.02)
verifier("B5 : X_L (Ω)", Xl, 0.320)
verifier("B6 : I_tot (A)", 178.3e3 / (sqrt(3) * 400), 257.4)
It = 258.0
PT = 178.3e3 + 3 * Rl * It**2
QT = 3 * Xl * It**2
ST = abs(complex(PT, QT))
verifier("B7 : pertes en ligne 3 R I² (kW)", 3 * Rl * It**2 / 1e3, 3.39)
verifier("B7 : P_T (kW)", PT / 1e3, 181.7)
verifier("B7 : Q_T (kvar)", QT / 1e3, 64.0)
verifier("B7 : S_T (kVA)", ST / 1e3, 192.6)
UD = ST / (sqrt(3) * It)
verifier("B8 : U_D (V)", UD, 431)
verifier("B8 : ΔU (V)", UD - 400, 31, tol=0.02)
verifier("B8 : ΔU / U_D (%)", (UD - 400) / UD * 100, 7.2)
verifier("B8 : X_L I (V)", Xl * It, 82.7)
verifier("B8 : R_L I (V)", Rl * It, 4.39)
verifier("Gain de pertes en ligne : 0,854²", 0.854**2, 0.73)
verifier("Avant compensation : pertes 3 R I² (kW)", 3 * Rl * 301**2 / 1e3, 4.62)

# ── §6 et exemple : critère de l'approximation, R_L nulle ──────────────
verifier("Critère : X I / V_r", Xl * 258 / Vr, 0.36, tol=0.01)
verifier("Critère : √(2 R I / V_r)", sqrt(2 * Rl * 258 / Vr), 0.20, tol=0.03)
verifier("Critère : √(2 × 4,4 / 231)", sqrt(2 * 4.4 / 231), 0.20, tol=0.03)
U0 = abs(Vr + complex(0, Xl) * 258) * sqrt(3)
verifier("R_L = 0 : ΔU (V)", U0 - 400, 25, tol=0.02)
verifier("R_L = 0 : ΔU / U_D (%)", (U0 - 400) / U0 * 100, 5.9, tol=0.01)
verifier("√3 × 400 × 258 (kW)", sqrt(3) * 400 * 258 / 1e3, 178.7)
verifier("Exact : ΔU avec I = 258 A (V)", Vd * sqrt(3) - 400, 32, tol=0.02)

# ── §6 : contre-exemple avant compensation (FP = 0,854, I = 301 A) ─────
cp, sp = 0.854, sin(acos(0.854))
verifier("Avant compensation : projection I(R cos φ + X sin φ) (V)", 301 * (Rl * cp + Xl * sp), 55, tol=0.01)
verifier("Avant compensation : terme négligé (V)", (Xl * 301 * cp - Rl * 301 * sp) ** 2 / (2 * Vr), 14, tol=0.02)
Vd301 = abs(Vr + complex(Rl, Xl) * 301 * complex(cp, -sp))
verifier("Avant compensation : chute exacte par phase (V)", Vd301 - Vr, 65.5, tol=0.01)
verifier("Avant compensation : sous-estimation de la projection (%)", (1 - 301 * (Rl * cp + Xl * sp) / (Vd301 - Vr)) * 100, 17, tol=0.03)
verifier("2017-E2 B2.3 Boucherot : P phase 1 (W)", 16000 / 3 + 3000 + 260, 8593)
verifier("2017-E2 B2.3 Boucherot : Q phase 1 (var)", 260 * tan(acos(0.8)), 195)
verifier("2017-E2 B2.3 Boucherot : S phase 1 (VA)", hypot(16000 / 3 + 3260, 260 * tan(acos(0.8))), 8596)
verifier("Compensé : terme négligé par phase (V)", (Xl * 258) ** 2 / (2 * Vr), 14.8, tol=0.01)
verifier("Compensé : projection R I par phase (V)", Rl * 258, 4.4, tol=0.01)
verifier("2018-E2 DRS 3 : S1 × THD (kVA)", 1.93 / 0.75 * 0.288, 0.74, tol=0.01)
verifier("2018-E2 DRS 5 : V I / 15 (VA)", 230.1 * 16.23 / 15, 249)

# ── Auto-test ──────────────────────────────────────────────────────────
verifier("AT1 : P (W)", 230 * 8 * 0.8, 1472)
verifier("AT1 : Q (var)", 230 * 8 * 0.6, 1104)
verifier("AT1 : S (VA)", 230 * 8, 1840)
verifier("AT1 : C (µF)", 1104 / (w * 230**2) * 1e6, 66.4)
Pa = 1500 + 4000 + 3000
Qa = 1500 * tan(acos(0.9)) + 4000 * tan(acos(0.75))
verifier("AT2 : P (kW)", Pa / 1e3, 8.5)
verifier("AT2 : Q (kvar)", Qa / 1e3, 4.25)
verifier("AT2 : S (kVA)", abs(complex(Pa, Qa)) / 1e3, 9.50)
verifier("AT2 : FP", Pa / abs(complex(Pa, Qa)), 0.894)
verifier("AT2 : I (A)", abs(complex(Pa, Qa)) / 230, 41.3)
verifier("AT2 : somme naïve des S (kVA)", (1500 / 0.9 + 4000 / 0.75 + 3000) / 1e3, 10.0)
# Cours §2 : moteur 3 kW (0,8), chauffage 2 kW, condensateur 1 kvar
Pb, Qb = 5000, 3000 * tan(acos(0.8)) - 1000
verifier("§2 : Q moteur (kvar)", 3000 * tan(acos(0.8)) / 1e3, 2.25)
verifier("§2 : S_tot (kVA)", abs(complex(Pb, Qb)) / 1e3, 5.15)
verifier("§2 : FP", Pb / abs(complex(Pb, Qb)), 0.970)
verifier("§2 : somme naïve (kVA)", (3000 / 0.8 + 2000 + 1000) / 1e3, 6.75)
verifier("AT3 : étoile, P (W)", 3 * (400 / sqrt(3)) ** 2 / 50, 3200)
verifier("AT3 : étoile, I (A)", 400 / sqrt(3) / 50, 4.62)
verifier("AT3 : triangle, P (W)", 3 * 400**2 / 50, 9600)
verifier("AT3 : triangle, J (A)", 400 / 50, 8)
verifier("AT3 : triangle, I (A)", sqrt(3) * 8, 13.9)
verifier("AT4 : I_n (A)", 7500 / (0.88 * sqrt(3) * 400 * 0.83), 14.8)
verifier("AT4 : I sans η (A)", 7500 / (sqrt(3) * 400 * 0.83), 13.0)
verifier("AT4 : P_a (kW)", 7500 / 0.88 / 1e3, 8.52)
P5a = 50e3
Qc5a = P5a * (tan(acos(0.7)) - tan(acos(0.95)))
verifier("AT5 : Q_C (kvar)", Qc5a / 1e3, 34.6)
verifier("AT5 : C étoile (µF)", Qc5a / (3 * w * 230**2) * 1e6, 693, tol=0.01)
verifier("AT5 : I avant (A)", P5a / (sqrt(3) * 400 * 0.7), 103)
verifier("AT5 : I après (A)", P5a / (sqrt(3) * 400 * 0.95), 76.0)
verifier("AT5 : pertes, rapport (0,7/0,95)²", (0.7 / 0.95) ** 2, 0.543)

# ── Auto-test 6 : harmoniques ──────────────────────────────────────────
P6, S6, c6 = 180.0, 240.0, 0.96
Q16 = P6 * tan(acos(c6))
verifier("AT6 : FP", P6 / S6, 0.75)
verifier("AT6 : Q1 (var)", Q16, 52.5)
verifier("AT6 : D (VA)", sqrt(S6**2 - P6**2 - Q16**2), 150)
verifier("2020-E2 Q19 : démarrage crête rapporté au calibre 6 A", 3 * In20 * sqrt(2) / 6, 3.4, tol=0.02)
verifier("2020-E2 Q19 : seuil bas de la courbe D (× I_n)", 12 * 0.8, 9.6)

# ── Homogénéité ────────────────────────────────────────────────────────
def dim(kg=0, m=0, s=0, a=0):
    return (kg, m, s, a)
def mul(*ds):
    return tuple(sum(x) for x in zip(*ds))
def inv(d):
    return tuple(-x for x in d)
def puis(d, n):
    return tuple(n * x for x in d)
SANS, SEC, AMP = dim(), dim(s=1), dim(a=1)
WATT = dim(kg=1, m=2, s=-3)
VOLT = mul(WATT, inv(AMP))
OHM = mul(VOLT, inv(AMP))
FARAD = mul(AMP, SEC, inv(VOLT))
HENRY = mul(VOLT, SEC, inv(AMP))
RADS = inv(SEC)
METRE = dim(m=1)
RELATIONS = [
    ("T02-f-001 P = U I cos φ", WATT, mul(VOLT, AMP)),
    ("T02-f-005 S² = P² + Q²", puis(WATT, 2), puis(WATT, 2)),
    ("T02-f-006 I = P/(U cos φ)", AMP, mul(WATT, inv(VOLT))),
    ("T02-f-007 R = U²/P", OHM, mul(puis(VOLT, 2), inv(WATT))),
    ("T02-f-011 I = P/(√3 U cos φ)", AMP, mul(WATT, inv(VOLT))),
    ("T02-f-016 D = √(S² − P² − Q1²)", WATT, WATT),
    ("T02-f-022 I = S/(√3 U)", AMP, mul(WATT, inv(VOLT))),
    ("T02-f-024 Q_C = 3 C ω V²", WATT, mul(FARAD, RADS, puis(VOLT, 2))),
    ("T02-f-025 C = Q/(3 ω V²)", FARAD, mul(WATT, inv(RADS), puis(VOLT, -2))),
    ("T02-f-027 R_L = R_u ℓ", OHM, mul(OHM, inv(METRE), METRE)),
    ("T02-f-029 ΔU ≈ √3 I (R cos φ + X sin φ)", VOLT, mul(AMP, OHM)),
    ("T02-f-033 P0 = V²/R_f", WATT, mul(puis(VOLT, 2), inv(OHM))),
    ("T02-f-033 Q0 = V²/(L ω)", WATT, mul(puis(VOLT, 2), inv(mul(HENRY, RADS)))),
    ("Pertes en ligne 3 R I²", WATT, mul(OHM, puis(AMP, 2))),
    ("U_D = S_T/(√3 I)", VOLT, mul(WATT, inv(AMP))),
    ("ΔU = ρ L I / s (ρ en Ω·m)", VOLT, mul(OHM, METRE, METRE, AMP, puis(METRE, -2))),
]
for nom, g, d in RELATIONS:
    ok = g == d
    print(f"{'ok ' if ok else 'ÉCART'} homogénéité · {nom}")
    if not ok:
        ECARTS.append(nom)

print()
print("Aucun écart." if not ECARTS else f"{len(ECARTS)} écart(s) : {ECARTS}")
raise SystemExit(1 if ECARTS else 0)
