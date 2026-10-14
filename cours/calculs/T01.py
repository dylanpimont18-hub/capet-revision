"""Applications numériques du chapitre T01, refaites en Python.

    python3 cours/calculs/T01.py

Chaque bloc reprend une valeur publiée dans cours/textes/T01.html ; un
écart de plus de 0,5 % sur la valeur arrondie fait échouer le script.
"""
from math import sqrt, pi, exp, cos, sin, acos, tan, atan

ECARTS = []


def verifier(nom, calcule, publie, tol=0.005):
    ok = abs(calcule - publie) <= tol * max(abs(publie), 1e-12)
    print(f"{'ok ' if ok else 'ÉCART'} {nom:55s} calculé {calcule:.6g} · publié {publie:g}")
    if not ok:
        ECARTS.append(nom)


# ── Méthode : bilan d'énergie (2020-E2, Q9 et Q14) ──────────────────────
E9 = 40 * 24 + 30 * 1 + 70 * 10
verifier("2020-E2 Q9 : énergie journalière (Wh)", E9, 1690)
E14 = E9 + 80 * 18 + 40 * 18 + 432 * 1
verifier("2020-E2 Q14 : nouvelle énergie journalière (Wh)", E14, 4282)
C15 = E14 * 2 / (0.7 * 12)                # 2020-E2 Q15 : C = Ec·N/(L·U)
verifier("2020-E2 Q15 : capacité nécessaire (Ah)", C15, 1020)
verifier("2020-E2 Q15 : avec 8 % de pertes (Ah)", C15 * 1.08, 1100, tol=0.01)
verifier("2020-E2 Q15 : nombre de batteries de 130 Ah", C15 * 1.08 / 130, 8.5, tol=0.02)
verifier("2020-E2 : parc existant 2 × 130 Ah", 2 * 130, 260)

# ── Méthode : modéliser une charge (2017-E2 C1.2, 2025-E2 Q36) ──────────
verifier("R = U²/P, 230 V, 3 kW (Ω)", 230**2 / 3000, 17.6)
verifier("courant du réchauffeur (A)", 3000 / 230, 13.0)

# ── Méthode : frein (2022-E2 Q25, Q34) ──────────────────────────────────
verifier("R_f · I_f = 10,1 Ω × 19 A (V)", 10.1 * 19, 192)

# ── Méthode : diviseur (2023-E2 F2, V_s1 prise aux bornes de R_A) ──────
RA = 1.0
RB = 9 * RA
verifier("R_A/(R_A+R_B) avec R_B = 9 R_A", RA / (RA + RB), 0.1)

# ── Cours : valeurs efficaces de référence (intégration numérique) ──────
N = 200000
def efficace(f):
    return sqrt(sum(f((k + 0.5) / N) ** 2 for k in range(N)) / N)
def moyenne(f):
    return sum(f((k + 0.5) / N) for k in range(N)) / N
verifier("sinus : V_eff / V_max", efficace(lambda t: sin(2 * pi * t)), 1 / sqrt(2))
verifier("triangle : V_eff / V_max", efficace(lambda t: 4 * t - 1 if t < 0.5 else 3 - 4 * t), 1 / sqrt(3))
verifier("sinus redressé : V_eff / V_max", efficace(lambda t: abs(sin(2 * pi * t))), 1 / sqrt(2))
verifier("sinus redressé : <v> / V_max", moyenne(lambda t: abs(sin(2 * pi * t))), 2 / pi)
alpha = 0.25
verifier("créneau 0/E α=0,25 : <v>/E", moyenne(lambda t: 1.0 if t < alpha else 0.0), alpha)
verifier("créneau 0/E α=0,25 : V_eff/E", efficace(lambda t: 1.0 if t < alpha else 0.0), sqrt(alpha))
verifier("2/π (arrondi publié 0,637)", 2 / pi, 0.637)

# ── Cours : premier ordre ──────────────────────────────────────────────
verifier("1 − e^-1 (63 %)", 1 - exp(-1), 0.632)
verifier("1 − e^-3 (95 %)", 1 - exp(-3), 0.950)
verifier("1 − e^-5 (99,3 %)", 1 - exp(-5), 0.993)

# ── Cours : vitesses de synchronisme à 50 Hz ───────────────────────────
for p, ns in [(1, 3000), (2, 1500), (3, 1000), (4, 750)]:
    verifier(f"N_s à 50 Hz, p = {p} (tr/min)", 60 * 50 / p, ns)

# ── Cours : tension composée, diviseur chargé ──────────────────────────
verifier("U = 2 V cos 30° = √3 V (V = 230 V)", 2 * 230 * cos(pi / 6), 398.4)
verifier("√3 × 230 V ≈ 400 V", sqrt(3) * 230, 400, tol=0.01)
Ra = Rb = 10e3
Rc = 100 * (Ra * Rb / (Ra + Rb))
verifier("erreur relative du diviseur pour R_c = 100 R_th (%)", (1 - Rc / (Rc + Ra * Rb / (Ra + Rb))) * 100, 1, tol=0.02)

# ── Exemple chiffré : alimentation par rails (d'après 2024-E1) ─────────
P, U0 = 7.2e3, 72.0
I = P / U0
verifier("Ex. Q1 : I = P/U0 (A)", I, 100)
S = 150 * 11 + (90 - 11) * 11          # mm², cornière 150 × 90 × 11
verifier("Ex. Q2 : section de la cornière (mm²)", S, 2519)
rho = 0.13                              # Ω·mm²/m
Rl = rho / S
verifier("Ex. Q2 : R_l (µΩ/m)", Rl * 1e6, 51.6)
L = 1000.0
x = 300.0
R1, R2 = 2 * Rl * x, 2 * Rl * (L - x)
Req = R1 * R2 / (R1 + R2)
verifier("Ex. Q3 : R1 ∥ R2 = 2 R_l L (1−x/L)(x/L)", Req, 2 * Rl * L * (1 - x / L) * (x / L))
dU = 0.05 * U0
verifier("Ex. Q5 : chute admissible (V)", dU, 3.6)
Lmax = 2 * dU / (Rl * I)
verifier("Ex. Q5 : L_max (m)", Lmax, 1395)
Reqmax = Rl * Lmax / 2
verifier("Ex. Q5 : R_eq max (mΩ)", Reqmax * 1e3, 36.0)
verifier("Ex. Q5 (Q43) : boucle de 2,2 km, deux boîtiers (m)", 2200 / 2, 1100)
PJ = Reqmax * I**2
verifier("Ex. Q6 : pertes Joule au pire (W)", PJ, 360)
verifier("Ex. Q6 : pertes / P", PJ / P, 0.05)
# Courants des deux boîtiers, capsule à x = L/4 de la ligne L_max
x = Lmax / 4
R1, R2 = 2 * Rl * x, 2 * Rl * (Lmax - x)
i1 = I * R2 / (R1 + R2)
verifier("Ex. Q4 : i1 à x = L/4 (A)", i1, 75)
verifier("Ex. Q4 : i2 à x = L/4 (A)", I - i1, 25)

# ── Auto-test ──────────────────────────────────────────────────────────
verifier("AT1 : R radiateur 2 kW 230 V (Ω)", 230**2 / 2000, 26.5)
verifier("AT1 : I (A)", 2000 / 230, 8.70)
verifier("AT1 : W en 3 h (kWh)", 2 * 3, 6)
verifier("AT1 : W (MJ)", 6 * 3.6, 21.6)
verifier("AT2 : <v> créneau 48 V α = 0,25 (V)", 0.25 * 48, 12)
verifier("AT2 : V_eff (V)", 48 * sqrt(0.25), 24)
verifier("AT2 : P dans 10 Ω (W)", 24**2 / 10, 57.6)
Rp = 10e3 * 10e3 / 20e3
verifier("AT3 : V_s chargé (V)", 12 * Rp / (10e3 + Rp), 4)
verifier("AT3 : E_th (V)", 6, 6)
verifier("AT3 : V_s via Thévenin (V)", 6 * 10e3 / (5e3 + 10e3), 4)
U, Pm, fp = 400.0, 15e3, 0.8
Im = Pm / (sqrt(3) * U * fp)
verifier("AT4 : I ligne (A)", Im, 27.1)
Q = Pm * tan(acos(fp))
verifier("AT4 : Q (kvar)", Q / 1e3, 11.25)
w = 2 * pi * 50
V = U / sqrt(3)
verifier("AT4 : C étoile (µF)", Q / (3 * w * V**2) * 1e6, 224)
verifier("AT4 : C triangle (µF)", Q / (3 * w * U**2) * 1e6, 74.6)
verifier("AT4 : I après compensation (A)", Pm / (sqrt(3) * U), 21.7)
Lb, Rb, Eb = 0.5, 10.0, 24.0
tau = Lb / Rb
verifier("AT5 : τ (ms)", tau * 1e3, 50)
verifier("AT5 : I∞ (A)", Eb / Rb, 2.4)
verifier("AT5 : i(τ) (A)", Eb / Rb * (1 - exp(-1)), 1.52)
verifier("AT5 : énergie finale (J)", 0.5 * Lb * (Eb / Rb) ** 2, 1.44)
verifier("AT5 : 3τ (ms)", 3 * tau * 1e3, 150)
Vcc, R0, dR = 5.0, 350.0, 0.7
exact = Vcc / 2 * dR / (2 * R0 + dR)
approx = Vcc * dR / (4 * R0)
verifier("AT6 : V_A − V_B exact (mV)", exact * 1e3, 2.4975)
verifier("AT6 : V_A − V_B approché (mV)", approx * 1e3, 2.5)
verifier("AT6 : écart relatif approx (%)", (approx - exact) / exact * 100, 0.1)

# ── Homogénéité des formules du chapitre ──────────────────────────────
# Dimensions en exposants de (kg, m, s, A) ; chaque relation doit avoir la
# même dimension des deux côtés.
def dim(kg=0, m=0, s=0, a=0):
    return (kg, m, s, a)
def mul(*ds):
    return tuple(sum(x) for x in zip(*ds))
def inv(d):
    return tuple(-x for x in d)
def puis(d, n):
    return tuple(n * x for x in d)
SANS = dim()
SEC, AMP = dim(s=1), dim(a=1)
WATT = dim(kg=1, m=2, s=-3)
JOULE = mul(WATT, SEC)
VOLT = mul(WATT, inv(AMP))
OHM = mul(VOLT, inv(AMP))
FARAD = mul(AMP, SEC, inv(VOLT))
HENRY = mul(VOLT, SEC, inv(AMP))
HZ = inv(SEC)
COULOMB = mul(AMP, SEC)
RELATIONS = [
    ("T01-f-001 u = R i", VOLT, mul(OHM, AMP)),
    ("T01-f-002 u = e + R i", VOLT, mul(OHM, AMP)),
    ("T01-f-005 diviseur : V_e R_B/(R_A+R_B)", VOLT, mul(VOLT, OHM, inv(OHM))),
    ("T01-f-006 diviseur : I R_2/(R_1+R_2)", AMP, mul(AMP, OHM, inv(OHM))),
    ("T01-f-008 V² = (1/T)∫v² dt", puis(VOLT, 2), mul(inv(SEC), puis(VOLT, 2), SEC)),
    ("T01-f-009 P = V I cos φ", WATT, mul(VOLT, AMP)),
    ("T01-f-011 Q = V I sin φ (var ≡ W)", WATT, mul(VOLT, AMP)),
    ("T01-f-012 S² = P² + Q²", puis(WATT, 2), puis(WATT, 2)),
    ("T01-f-014 τ = R C", SEC, mul(OHM, FARAD)),
    ("T01-f-015 τ = L/R", SEC, mul(HENRY, inv(OHM))),
    ("T01-f-016 W = ½ C U²", JOULE, mul(FARAD, puis(VOLT, 2))),
    ("T01-f-017 W = ½ L I²", JOULE, mul(HENRY, puis(AMP, 2))),
    ("T01-f-018 C = Q/(3 ω V²)", FARAD, mul(WATT, inv(HZ), inv(puis(VOLT, 2)))),
    ("T01-f-020 N_s = 60 f/p (tours par unité de temps)", HZ, HZ),
    ("i = dq/dt", AMP, mul(COULOMB, inv(SEC))),
    ("i = C du/dt", AMP, mul(FARAD, VOLT, inv(SEC))),
    ("u = L di/dt", VOLT, mul(HENRY, AMP, inv(SEC))),
    ("R = ρ L/S (ρ en Ω·m)", OHM, mul(OHM, dim(m=1), dim(m=1), inv(dim(m=2)))),
    ("R = U²/P", OHM, mul(puis(VOLT, 2), inv(WATT))),
    ("W = U Q (énergie d'une batterie)", JOULE, mul(VOLT, COULOMB)),
    ("Millman : V = Σ(E/R)/Σ(1/R)", VOLT, mul(VOLT, inv(OHM), OHM)),
    ("RC du/dt + u = E", VOLT, mul(OHM, FARAD, VOLT, inv(SEC))),
    ("I_C = C ω V", AMP, mul(FARAD, HZ, VOLT)),
    ("ΔU_max = R_ℓ L I/2 (R_ℓ en Ω/m)", VOLT, mul(OHM, inv(dim(m=1)), dim(m=1), AMP)),
    ("V_A − V_B = V_cc ΔR/(4 R0)", VOLT, mul(VOLT, OHM, inv(OHM))),
]
for nom, gauche, droite in RELATIONS:
    ok = gauche == droite
    print(f"{'ok ' if ok else 'ÉCART'} homogénéité · {nom}")
    if not ok:
        ECARTS.append(nom)

print()
print("Aucun écart." if not ECARTS else f"{len(ECARTS)} écart(s) : {ECARTS}")
raise SystemExit(1 if ECARTS else 0)
