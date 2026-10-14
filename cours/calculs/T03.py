"""Applications numériques du chapitre T03, refaites en Python.

    python3 cours/calculs/T03.py

Chaque bloc reprend une valeur publiée dans cours/textes/T03.html ; un
écart de plus de 0,5 % sur la valeur arrondie fait échouer le script.
"""
import cmath
from math import sqrt, pi, atan, degrees, radians, cos, sin, log10, tan

ECARTS = []


def verifier(nom, calcule, publie, tol=0.005):
    ok = abs(calcule - publie) <= tol * max(abs(publie), 1e-12)
    print(f"{'ok ' if ok else 'ÉCART'} {nom:58s} calculé {calcule:.6g} · publié {publie:g}")
    if not ok:
        ECARTS.append(nom)


w50 = 2 * pi * 50

# ── Méthode : 2018-E2 Q10–Q11 (tension injectée en opposition) ─────────
U = 230.0
Xmax = (230 - 190) * sqrt(2)
verifier("2018-E2 Q11 : X_max (V)", Xmax, 56.6)
u = cmath.rect(230, 0); x = cmath.rect(40, pi)
verifier("2018-E2 Q11 : |U + X| (V)", abs(u + x), 190)

# ── Méthode : 2025-E2 Q22 (charge R-L, S = 3 kVA) ──────────────────────
R0, L0 = 17.7, 10e-3
Z = complex(R0, L0 * w50)
phi = cmath.phase(Z)
verifier("2025-E2 Q22 : L ω (Ω)", L0 * w50, 3.14)
verifier("2025-E2 Q22 : φ (°)", degrees(phi), 10.1, tol=0.01)
verifier("2025-E2 Q22 : cos φ", cos(phi), 0.985)
verifier("2025-E2 Q22 : P = S cos φ (W)", 3000 * cos(phi), 2954)
verifier("2025-E2 Q22 : Q = S sin φ (var)", 3000 * sin(phi), 524)
verifier("Facteur 0,9 : fondamental d'un créneau (V)", 4 * 230 / (pi * sqrt(2)), 207)
verifier("THD d'un créneau", sqrt(pi**2 / 8 - 1), 0.48, tol=0.01)

# ── Méthode : 2024-E2 A3–A4 (modèle de la MAS) ─────────────────────────
Ns = 60 * 50 / 2
g = (Ns - 1400) / Ns
verifier("2024-E2 A3 : N_s (tr/min)", Ns, 1500)
verifier("2024-E2 A3 : g", g, 0.0667)
Zr = complex(0.1 / g, 3.6e-3 * w50)
verifier("2024-E2 A4 : R'_R/g (Ω)", Zr.real, 1.5)
verifier("2024-E2 A4 : L_f ω_s (Ω)", Zr.imag, 1.13)
verifier("2024-E2 A4 : |Z_r| (Ω)", abs(Zr), 1.88)
verifier("2024-E2 A4 : I'_r (A)", 230 / abs(Zr), 122)

# ── Cours : RLC, ordres de grandeur, Bode ──────────────────────────────
verifier("−3 dB : 20 log(1/√2)", 20 * log10(1 / sqrt(2)), -3.01)
verifier("20 log 10 = 20 dB", 20 * log10(10), 20)
# Marge de phase de l'exemple du cours : H_BO = 10 / (jω (1 + jω/10))
def Hbo(w):
    return 10 / (1j * w * (1 + 1j * w / 10))
wc = sqrt(50 * (sqrt(5) - 1))
verifier("FTBO : |H(j ω_c0)| = 1", abs(Hbo(wc)), 1)
verifier("FTBO : ω_c0 (rad/s)", wc, 7.86)
verifier("FTBO : arg H(j ω_c0) (°)", degrees(cmath.phase(Hbo(wc))), -128.2)
verifier("FTBO : marge de phase (°)", 180 + degrees(cmath.phase(Hbo(wc))), 51.8)

# ── Exemple chiffré : charge R-L sous 230 V, 50 Hz ─────────────────────
V = 230.0
verifier("Ex. 1 : |Z| (Ω)", abs(Z), 17.98)
verifier("Ex. 1 : arg Z (°)", degrees(phi), 10.06)
I = V / Z
verifier("Ex. 2 : I (A)", abs(I), 12.79)
verifier("Ex. 2 : arg I (°)", degrees(cmath.phase(I)), -10.06)
verifier("Ex. 2 : U_R (V)", abs(R0 * I), 226.5)
verifier("Ex. 2 : U_L (V)", abs(1j * L0 * w50 * I), 40.2)
Ssc = V * I.conjugate()
verifier("Ex. 3 : P (W)", Ssc.real, 2897)
verifier("Ex. 3 : Q (var)", Ssc.imag, 514)
verifier("Ex. 3 : S (VA)", abs(Ssc), 2943)
verifier("Ex. 3 : cos φ", Ssc.real / abs(Ssc), 0.985)
Y = 1 / Z
verifier("Ex. 4 : G (mS)", Y.real * 1e3, 54.8)
verifier("Ex. 4 : B (mS)", Y.imag * 1e3, -9.72)
verifier("Ex. 4 : R_p (Ω)", 1 / Y.real, 18.26)
verifier("Ex. 4 : L_p (H)", 1 / (-Y.imag * w50), 0.327)
C = -Y.imag / w50
verifier("Ex. 5 : C (µF)", C * 1e6, 30.9)
verifier("Ex. 5 : Q_C = C ω V² (var)", C * w50 * V**2, 514)
verifier("Ex. 5 : I' = V G (A)", V * Y.real, 12.60)
verifier("Ex. 5 : baisse du courant (%)", (1 - Y.real / abs(Y)) * 100, 1.5, tol=0.05)
# Harmoniques d'un créneau ±E dans le condensateur : amplitude indépendante de n
E = 230.0
for n in (1, 3, 5, 7):
    Vn = 4 * E / (n * pi)
    verifier(f"Ex. 6 : amplitude du courant harmonique {n} (A)", Vn * n * w50 * C, 4 * E * w50 * C / pi)
verifier("Ex. 6 : 4 E ω C / π (A)", 4 * E * w50 * C / pi, 2.85)

# ── Auto-test ──────────────────────────────────────────────────────────
X = cmath.rect(5, -pi / 3)
verifier("AT1 : f = 100π/2π (Hz)", 100 * pi / (2 * pi), 50)
U1 = complex(10, 10)
verifier("AT1 : |10 + 10 j| (V)", abs(U1), 14.14)
verifier("AT1 : amplitude (V)", abs(U1) * sqrt(2), 20)
Zb = complex(8, 19.1e-3 * w50)
verifier("AT2 : L ω (Ω)", Zb.imag, 6.0)
verifier("AT2 : |Z| (Ω)", abs(Zb), 10.0)
verifier("AT2 : φ (°)", degrees(cmath.phase(Zb)), 36.9)
verifier("AT2 : I (A)", 230 / abs(Zb), 23.0)
verifier("AT2 : P (W)", 8 * (230 / abs(Zb)) ** 2, 4232)
verifier("AT2 : Q (var)", Zb.imag * (230 / abs(Zb)) ** 2, 3174)
R, Cc, w = 1e3, 100e-9, 2 * pi * 1e3
verifier("AT3 : 1/(Cω) (Ω)", 1 / (Cc * w), 1592)
verifier("AT3 : |Z| RC (Ω)", abs(complex(R, -1 / (Cc * w))), 1880)
verifier("AT3 : φ RC (°)", degrees(-atan(1 / (R * Cc * w))), -57.9)
fc = 1 / (2 * pi * R * Cc)
H = 1 / (1 + 1j * 1e3 / fc)
verifier("AT3 : f_c (Hz)", fc, 1592)
verifier("AT3 : |H| (dB)", 20 * log10(abs(H)), -1.44)
verifier("AT3 : arg H (°)", degrees(cmath.phase(H)), -32.1)
Rr, Lr, Cr = 10.0, 10e-3, 1e-6
w0 = 1 / sqrt(Lr * Cr)
verifier("AT4 : ω0 (rad/s)", w0, 1e4)
verifier("AT4 : f0 (Hz)", w0 / (2 * pi), 1592)
Qf = Lr * w0 / Rr
verifier("AT4 : Q", Qf, 10)
verifier("AT4 : Δf (Hz)", w0 / (2 * pi) / Qf, 159)
verifier("AT4 : U_C à la résonance sous 1 V (V)", 1 / (Rr * Cr * w0), 10)
verifier("AT5 : m = (R/2)√(C/L)", Rr / 2 * sqrt(Cr / Lr), 0.05)
verifier("AT5 : m = 1/(2Q)", 1 / (2 * Qf), 0.05)
# Bande passante exacte du RLC série : ω2 − ω1 = R/L
w1 = -Rr / (2 * Lr) + sqrt((Rr / (2 * Lr)) ** 2 + w0**2)
w2 = Rr / (2 * Lr) + sqrt((Rr / (2 * Lr)) ** 2 + w0**2)
verifier("Cours : ω2 − ω1 = R/L (rad/s)", w2 - w1, Rr / Lr)
verifier("AT6 : marge pour φ = −140° (°)", 180 - 140, 40)

# ── Méthode : 2023-E2 D4, D7, D8 (lecture de DR4) ─────────────────────
KM = 10 ** (26.4 / 20)
verifier("2023-E2 D4 : K_M = 10^(26,4/20)", KM, 20.9)
wa, wb = 10.0, 7e3
KGT = 5 / (1000 * 2 * pi / 60)
verifier("2023-E2 D7 : K_GT (V·s/rad)", KGT, 0.0477)
def ftbo(w, k=1.0):
    return k * KM * KGT / ((1 + 1j * w / wa) * (1 + 1j * w / wb))
verifier("2023-E2 D8 : phase de la FTBO à ω_b (°)", degrees(cmath.phase(ftbo(wb))), -135, tol=0.01)
verifier("2023-E2 D8 : 1/(700 √2)", 1 / (700 * sqrt(2)), 1 / 990, tol=0.01)
verifier("2023-E2 D8 : |FTBO(j ω_b)| pour K_PV = 1", abs(ftbo(wb)), 1 / 990, tol=0.02)
verifier("2023-E2 D8 : gain en dB", 20 * log10(abs(ftbo(wb))), -60, tol=0.01)
Kpv = 1 / abs(ftbo(wb))
verifier("2023-E2 D8 : K_PV", Kpv, 1e3, tol=0.03)
verifier("2023-E2 D8 : marge obtenue (°)", 180 + degrees(cmath.phase(ftbo(wb, Kpv))), 45, tol=0.01)

# ── Méthode : forme canonique, exemple 5/(2 + 0,01 jω + 2e-5 (jω)²) ───
K, a1, a2 = 5 / 2, 0.01 / 2, 2e-5 / 2
w0c = 1 / sqrt(a2)
verifier("Canonique : K", K, 2.5)
verifier("Canonique : ω0 (rad/s)", w0c, 316)
verifier("Canonique : m", a1 * w0c / 2, 0.79)

# ── Exemple : compléments ─────────────────────────────────────────────
verifier("Ex. 1 : L ω / R (%)", L0 * w50 / R0 * 100, 18, tol=0.02)
verifier("Ex. 2 : √(U_R² + U_L²) (V)", sqrt(abs(R0 * I) ** 2 + abs(L0 * w50 * I) ** 2), 230)
verifier("Ex. 2 : U_R + U_L (arrondis affichés)", 226.5 + 40.2, 266.7)
verifier("Ex. 4 : courant actif V G (A)", V * Y.real, 12.60)
verifier("Ex. 4 : courant réactif V |B| (A)", V * abs(Y.imag), 2.24)
verifier("Pièges : 1/0,03 ≈ 33", 1 / 0.03, 33.3)

# ── Méthode 2025-E2 : puissance réelle sous créneau ±230 V ────────────
P_cr, I2_cr = 0.0, 0.0
for n in range(1, 20001, 2):
    Vn = 4 * 230 / (n * pi * sqrt(2))
    In = Vn / abs(complex(R0, n * L0 * w50))
    P_cr += R0 * In**2
    I2_cr += In**2
verifier("2025-E2 : P sous créneau (kW)", P_cr / 1e3, 2.65)
verifier("2025-E2 : facteur de puissance sous créneau", P_cr / (230 * sqrt(I2_cr)), 0.94)
verifier("2025-E2 : I sous créneau (A)", sqrt(I2_cr), 12.2)
verifier("2025-E2 : S sous créneau (kVA)", 230 * sqrt(I2_cr) / 1e3, 2.81)
V1 = 4 * 230 / (pi * sqrt(2))
P1 = R0 * (V1 / abs(Z)) ** 2
verifier("2025-E2 : puissance des harmoniques (kW)", (P_cr - P1) / 1e3, 0.30, tol=0.02)
verifier("2025-E2 : S sous 230 V sinusoïdaux (kVA)", 230**2 / abs(Z) / 1e3, 2.94)
verifier("2023-E2 D7 : 20 log K_GT (dB)", 20 * log10(KGT), -26.4)
verifier("2023-E2 D7 : K_M K_GT", KM * KGT, 1.00)
verifier("2023-E2 D8 : ω_b/ω_a", wb / wa, 700)
verifier("MAS à l'arrêt (2024-E2) : I'_r ≈ V_s/(L_f ω_s) (A)", 230 / abs(complex(0.1, 3.6e-3 * w50)), 230 / (3.6e-3 * w50))
verifier("Cours : Q = Q_L/P à la résonance", (Lr * w0 * 1**2) / (Rr * 1**2), Qf)
verifier("2024-E2 : I'_r à l'arrêt (A)", 230 / abs(complex(0.1, 3.6e-3 * w50)), 203)
verifier("2024-E2 : rapport au courant nominal 122 A (arrondi à 0,1)", round(230 / abs(complex(0.1, 3.6e-3 * w50)) / 122, 1), 1.7)

# ── Homogénéité des formules du chapitre ──────────────────────────────
# Dimensions en exposants de (kg, m, s, A) ; j, φ, g, m et Q sont sans dimension.
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
VOLT = mul(WATT, inv(AMP))
OHM = mul(VOLT, inv(AMP))
SIEMENS = inv(OHM)
FARAD = mul(AMP, SEC, inv(VOLT))
HENRY = mul(VOLT, SEC, inv(AMP))
RADS = inv(SEC)
RELATIONS = [
    ("T03-f-002 Z_C = 1/(j C ω)", OHM, inv(mul(FARAD, RADS))),
    ("T03-f-003 Z_L = j L ω", OHM, mul(HENRY, RADS)),
    ("T03-f-004 U = Z I", VOLT, mul(OHM, AMP)),
    ("T03-f-005 Y = 1/Z", SIEMENS, inv(OHM)),
    ("T03-f-006 |Z|² = R² + (1/Cω)²", puis(OHM, 2), puis(inv(mul(FARAD, RADS)), 2)),
    ("T03-f-007 |Z|² = R² + (Lω)²", puis(OHM, 2), puis(mul(HENRY, RADS), 2)),
    ("T03-f-008 argument de arctan : 1/(R C ω)", SANS, inv(mul(OHM, FARAD, RADS))),
    ("T03-f-009 argument de arctan : L ω / R", SANS, mul(HENRY, RADS, inv(OHM))),
    ("T03-f-011 ω0 = 1/√(LC)", RADS, puis(mul(HENRY, FARAD), -0.5)),
    ("T03-f-012 Q = L ω0 / R", SANS, mul(HENRY, RADS, inv(OHM))),
    ("T03-f-012 Q = 1/(R C ω0)", SANS, inv(mul(OHM, FARAD, RADS))),
    ("T03-f-013 ω_c = 1/(R C)", RADS, inv(mul(OHM, FARAD))),
    ("T03-f-014 m = (R/2) √(C/L)", SANS, mul(OHM, puis(mul(FARAD, inv(HENRY)), 0.5))),
    ("T03-f-014 2m/ω0 = R C", SEC, mul(OHM, FARAD)),
    ("T03-f-018 I'_r = V/(L ω)", AMP, mul(VOLT, inv(mul(HENRY, RADS)))),
    ("T03-f-019 Z_Cp = 1/(j C_p ω)", OHM, inv(mul(FARAD, RADS))),
    ("Δω = R/L", RADS, mul(OHM, inv(HENRY))),
    ("S = V I*", WATT, mul(VOLT, AMP)),
    ("P = R I², Q = X I²", WATT, mul(OHM, puis(AMP, 2))),
    ("C = |B|/ω", FARAD, mul(SIEMENS, inv(RADS))),
    ("Q_C = C ω V²", WATT, mul(FARAD, RADS, puis(VOLT, 2))),
    ("Ex. 6 : I = 4 E C ω / π", AMP, mul(VOLT, FARAD, RADS)),
    ("L_p = 1/(|B| ω)", HENRY, inv(mul(SIEMENS, RADS))),
]
for nom, gauche, droite in RELATIONS:
    ok = gauche == droite
    print(f"{'ok ' if ok else 'ÉCART'} homogénéité · {nom}")
    if not ok:
        ECARTS.append(nom)

print()
print("Aucun écart." if not ECARTS else f"{len(ECARTS)} écart(s) : {ECARTS}")
raise SystemExit(1 if ECARTS else 0)
