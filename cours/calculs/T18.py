"""Applications numériques du chapitre T18, refaites en Python.

    python3 cours/calculs/T18.py

Chaque bloc reprend une valeur publiée dans cours/textes/T18.html ; un
écart de plus de 0,5 % sur la valeur arrondie fait échouer le script.
Le point de fonctionnement de la figure 3 est recalculé par dichotomie sur
la loi de Shockley, et la valeur moyenne du redresseur commandé par
intégration numérique.
"""
from math import sqrt, pi, sin, cos, exp, log, radians

ECARTS = []


def verifier(nom, calcule, publie, tol=0.005):
    ok = abs(calcule - publie) <= tol * max(abs(publie), 1e-12)
    print(f"{'ok ' if ok else 'ÉCART'} {nom:62s} calculé {calcule:.6g} · publié {publie:g}")
    if not ok:
        ECARTS.append(nom)


def homogene(nom, ok):
    print(f"{'ok ' if ok else 'ÉCART'} homogénéité : {nom}")
    if not ok:
        ECARTS.append(nom)


# ── §1 : loi de Shockley (I_s = 1 pA, n = 1) ───────────────────────────
k_B, q, Tk = 1.380649e-23, 1.602176634e-19, 300.0
UT = k_B * Tk / q
verifier("U_T = kT/q à 300 K (mV)", UT * 1e3, 26, tol=0.01)
verifier("U_T ln 10 (mV)", UT * log(10) * 1e3, 60, tol=0.01)
verifier("1 mA → 100 mA : gain de tension (mV)", UT * log(100) * 1e3, 120, tol=0.01)
Is, UTf = 1e-12, 0.02585     # valeurs de la figure 2


def v_de_i(i):
    return UTf * log(i / Is + 1)


verifier("Fig 2 : v à 50 mA (V)", v_de_i(0.05), 0.64)
verifier("Fig 2 : v à 100 mA (V)", v_de_i(0.1), 0.65, tol=0.01)
verifier("Fig 2 : r_d du modèle seuil + résistance (Ω)", (v_de_i(0.1) - 0.6) / 0.1, 0.55)

verifier("§1 : résistance dynamique locale nU_T/I à 100 mA (Ω)", UTf / 0.1, 0.26, tol=0.01)

# ── §2 : droite de charge, E = 2 V, R = 50 Ω ───────────────────────────
E3, R3 = 2.0, 50.0
a, b = 0.0, E3
for _ in range(100):
    m = (a + b) / 2
    if R3 * Is * (exp(m / UTf) - 1) + m > E3:
        b = m
    else:
        a = m
VQ, IQ = a, Is * (exp(a / UTf) - 1)
verifier("Fig 3 : V_Q (V)", VQ, 0.62)
verifier("Fig 3 : I_Q (mA)", IQ * 1e3, 27.6)
verifier("§2 : modèle à seuil, (2 − 0,6)/50 (mA)", (2 - 0.6) / 50 * 1e3, 28)
verifier("§2 : E = 0,4 V, courant supposé passant (négatif)", min(0.0, (0.4 - 0.6) / 50) * 1e3, -4)

# ── §3 : écrêtage ──────────────────────────────────────────────────────
verifier("§3 : V_ref + V_s (V)", 3.5 + 0.6, 4.1)
verifier("§3 : courant dans D_H sous 12 V, R = 10 kΩ (mA)", (12 - 4.1) / 10e3 * 1e3, 0.79)

# ── §5 : bipolaire, figure 6 ───────────────────────────────────────────
Isat = (12 - 0.2) / 470
verifier("§5 : I_C,sat = 11,8/470 (mA)", Isat * 1e3, 25, tol=0.01)
verifier("§5 : I_B minimal pour β = 100 (mA)", Isat / 100 * 1e3, 0.25, tol=0.01)

# ── §6 : MOSFET et IGBT ────────────────────────────────────────────────
Ron, V0, rce = 0.05, 0.9, 0.02
Ix = V0 / (Ron - rce)
verifier("Fig 7 : courant d'égalité des chutes (A)", Ix, 30)
verifier("Fig 7 : tension d'égalité (V)", Ron * Ix, 1.5)
Pm = lambda I: Ron * I ** 2
Pi = lambda I: V0 * I + rce * I ** 2
verifier("§6 : pertes à 30 A, MOSFET (W)", Pm(30), 45)
verifier("§6 : pertes à 30 A, IGBT (W)", Pi(30), 45)
verifier("§6 : MOSFET à 10 A (W)", Pm(10), 5)
verifier("§6 : IGBT à 10 A (W)", Pi(10), 11)
verifier("§6 : MOSFET à 50 A (W)", Pm(50), 125)
verifier("§6 : IGBT à 50 A (W)", Pi(50), 95)
# Pertes de commutation : aire des triangles de la figure 8
V, I, ton_off, fc = 540.0, 30.0, 0.5e-6, 10e3
N = 10000
W = sum(V * I * (1 - abs(2 * (k + 0.5) / N - 1)) for k in range(N)) * (ton_off / N)  # triangle de base t, hauteur VI
verifier("§6 : ½ V I t vérifié par l'aire du triangle (mJ)", W * 1e3, 0.5 * V * I * ton_off * 1e3)
verifier("§6 : P_com à 10 kHz (W)", 0.5 * V * I * ton_off * fc, 40.5)

# ── §7 : hacheur série ─────────────────────────────────────────────────
E7, al, T7, L7 = 48.0, 0.3, 50e-6, 1e-3
u_moy = sum(E7 if (k + 0.5) / 1000 < al else 0.0 for k in range(1000)) / 1000
verifier("§7 : ⟨u⟩ = αE par moyenne numérique (V)", u_moy, al * E7)
verifier("§7 : Δi = (1 − α)E αT/L = α(1 − α)E/(Lf)", (1 - al) * E7 * al * T7 / L7, al * (1 - al) * E7 * T7 / L7)
alphas = [k / 1000 for k in range(1001)]
verifier("§7 : α de l'ondulation maximale", max(alphas, key=lambda x: x * (1 - x)), 0.5)

# ── §8 : redresseurs ───────────────────────────────────────────────────
Vm, alpha = 1.0, radians(60)
N = 20000
moy = sum(Vm * sin(t) for t in [alpha + (pi - alpha) * (k + 0.5) / N for k in range(N)]) * (pi - alpha) / N / (2 * pi)
verifier("§8 : ⟨u_R⟩ P1 par intégration (× V_m)", moy, Vm * (1 + cos(alpha)) / (2 * pi))
verifier("§8 : P1, α = 0 : V_m/π", Vm * (1 + cos(0)) / (2 * pi), 1 / pi)
verifier("§8 : PD3, 3√2/π", 3 * sqrt(2) / pi, 1.35)
verifier("§8 : PD3, 3√6/π", 3 * sqrt(6) / pi, 2.34)
verifier("§8 : PD3, 3√3/π × √2 = 3√6/π", 3 * sqrt(3) / pi * sqrt(2), 3 * sqrt(6) / pi)
verifier("§8 : P3, 3√6/(2π)", 3 * sqrt(6) / (2 * pi), 1.17)
N = 20000
pd3 = 3 / pi * sum(sqrt(2) * cos(-pi / 6 + (pi / 3) * (k + 0.5) / N) for k in range(N)) * (pi / 3) / N
verifier("§8 : PD3 par intégration sur π/3 (× U)", pd3, 3 * sqrt(2) / pi)
p3 = 3 / (2 * pi) * sum(sqrt(2) * cos(-pi / 3 + (2 * pi / 3) * (k + 0.5) / N) for k in range(N)) * (2 * pi / 3) / N
verifier("§8 : P3 par intégration sur 2π/3 (× V)", p3, 1.17)

# ── Méthode : 2022-E1, Q27 ─────────────────────────────────────────────
verifier("2022-E1 : v_M en charge, 23,7 Ω × 3 mA (mV)", 23.7 * 3e-3 * 1e3, 71, tol=0.01)
verifier("2022-E1 : courant de décharge où D1 conduit (mA)", 0.6 / 23.7 * 1e3, 25, tol=0.02)

# ── Exemple chiffré : électrovanne ─────────────────────────────────────
E, Rb, L = 24.0, 48.0, 0.10
Ic = (E - 0.2) / Rb
verifier("Ex 1 : I_C,sat (A)", Ic, 0.496)
verifier("Ex 2 : I_B minimal (mA)", Ic / 50 * 1e3, 9.9, tol=0.01)
verifier("Ex 2 : I_B visé, k = 2 (mA)", 2 * 9.9, 19.8)
verifier("Ex 2 : R_B calculée (Ω)", (5 - 0.7) / 0.0198, 217)
IB = 4.3 / 220
verifier("Ex 2 : I_B avec 200 Ω (mA)", 4.3 / 200 * 1e3, 21.5)
verifier("Ex 2 : I_B avec 220 Ω (mA)", IB * 1e3, 19.5, tol=0.01)
verifier("Ex 2 : k obtenu", IB / (Ic / 50), 1.97)
P = 0.2 * Ic + 0.7 * IB
verifier("Ex 3 : V_CE,sat I_C (W)", 0.2 * Ic, 0.099)
verifier("Ex 3 : V_BE I_B (W)", 0.7 * 0.0195, 0.014, tol=0.03)
verifier("Ex 3 : pertes du transistor (W)", P, 0.11, tol=0.03)
verifier("Ex 3 : pertes de la bobine (W)", Rb * Ic ** 2, 11.8)
tau = L / Rb
verifier("Ex 4 : τ (ms)", tau * 1e3, 2.1, tol=0.01)
verifier("Ex 4 : 3τ (ms)", 3 * tau * 1e3, 6.3, tol=0.01)
verifier("Ex 4 : 1 − e^{−3} (95 %)", 1 - exp(-3), 0.95)
verifier("Ex 5 : L Δi/Δt sur 1 µs (kV)", L * Ic / 1e-6 / 1e3, 50, tol=0.01)
verifier("Ex 5 : v_CE max (V)", E + 0.7, 24.7)
verifier("Ex 5 : 1 + R_b I/V_s", 1 + Rb * Ic / 0.7, 35, tol=0.01)
verifier("Ex 5 : durée de roue libre τ ln 35 (ms)", tau * log(1 + Rb * Ic / 0.7) * 1e3, 7.4)
verifier("Ex 5 : ½ L I² (mJ)", 0.5 * L * Ic ** 2 * 1e3, 12.3)
verifier("Ex 6 : MOSFET, R I² (mW)", 0.10 * Ic ** 2 * 1e3, 24.6)
verifier("Ex 6 : rapport des pertes bipolaire/MOSFET", P / (0.10 * Ic ** 2), 4.6, tol=0.02)

# ── Auto-test ──────────────────────────────────────────────────────────
verifier("Q1 : (5 − 0,6)/220 (mA)", (5 - 0.6) / 220 * 1e3, 20)
verifier("Q2 : 3,3 + 0,6 (V)", 3.3 + 0.6, 3.9)
verifier("Q2 : (12 − 3,9)/10 kΩ (mA)", (12 - 3.9) / 10e3 * 1e3, 0.81)
verifier("Q3 : I_C,sat (mA)", 11.8, (12 - 0.2) / 1e3 * 1e3)
verifier("Q3 : β I_B à 50 µA (mA)", 100 * 50e-6 * 1e3, 5)
verifier("Q3 : V_CE linéaire (V)", 12 - 1e3 * 5e-3, 7)
verifier("Q3 : β I_B à 200 µA (mA)", 100 * 200e-6 * 1e3, 20)
verifier("Q4 : ⟨u⟩ (V)", 0.25 * 48, 12)
verifier("Q4 : Δi (A)", 0.25 * 0.75 * 48 / (1e-3 * 20e3), 0.45)
verifier("Q4 : Δi max (A)", 48 / (4 * 1e-3 * 20e3), 0.6)
Vm5 = 230 * sqrt(2)
verifier("Q5 : V_m (V)", Vm5, 325.3)
verifier("Q5 : P1 à 60° (V)", Vm5 * 1.5 / (2 * pi), 77.7)
verifier("Q5 : diode (V)", Vm5 / pi, 103.5)
verifier("Q5 : PD2 mixte (V)", Vm5 * 1.5 / pi, 155, tol=0.01)
verifier("Q6 : PD3 sous 400 V (V)", 3 * sqrt(2) / pi * 400, 540)
verifier("Q6 : tension inverse des diodes (V)", sqrt(2) * 400, 566)
verifier("Q6 : marge 1 200/566", 1200 / 566, 2, tol=0.07)

# ── Homogénéité ────────────────────────────────────────────────────────
# Dimensions [M, L, T, I] ; tension = M L² T⁻³ I⁻¹
V_, A_, S_ = (1, 2, -3, -1), (0, 0, 0, 1), (0, 0, 1, 0)
W_ = (1, 2, -3, 0)
OHM = tuple(a - b for a, b in zip(V_, A_))
HENRY = tuple(a + b for a, b in zip(OHM, S_))


def mul(*ds):
    return tuple(sum(c) for c in zip(*ds))


def puis(d, k):
    return tuple(k * c for c in d)


homogene("Δi_L = α(1 − α) E T / L en A", mul(V_, S_, puis(HENRY, -1)) == A_)
homogene("P_com = ½ V I t f en W", mul(V_, A_, S_, puis(S_, -1)) == W_)
homogene("R_B = (v_c − V_BE)/I_B en Ω", mul(V_, puis(A_, -1)) == OHM)
homogene("τ = L/R en s", mul(HENRY, puis(OHM, -1)) == S_)
homogene("½ L I² en J", mul(HENRY, A_, A_) == mul(W_, S_))
homogene("P = R_DS,on I² en W", mul(OHM, A_, A_) == W_)

print()
print("Aucun écart." if not ECARTS else f"{len(ECARTS)} écart(s) : {', '.join(ECARTS)}")
raise SystemExit(1 if ECARTS else 0)
