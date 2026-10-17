"""Applications numériques du chapitre T12, refaites en Python.

    python3 cours/calculs/T12.py

Chaque bloc reprend une valeur publiée dans cours/textes/T12.html ; un
écart de plus de 0,5 % sur la valeur arrondie fait échouer le script.
Les figures 4, 6 et 9 sont recontrôlées : régime d'excitation, courbes en V,
couple constant du BLDC.
"""
from math import sqrt, pi, hypot, sin, cos, asin, atan, atan2, radians, degrees

ECARTS = []


def verifier(nom, calcule, publie, tol=0.005):
    ok = abs(calcule - publie) <= tol * max(abs(publie), 1e-12)
    print(f"{'ok ' if ok else 'ÉCART'} {nom:62s} calculé {calcule:.6g} · publié {publie:g}")
    if not ok:
        ECARTS.append(nom)


def vrai(nom, ok):
    print(f"{'ok ' if ok else 'ÉCART'} {nom}")
    if not ok:
        ECARTS.append(nom)


def bissection(fn, a, b, n=200):
    fa = fn(a)
    for _ in range(n):
        m = (a + b) / 2
        fm = fn(m)
        if (fm > 0) == (fa > 0):
            a, fa = m, fm
        else:
            b = m
    return (a + b) / 2


tr = lambda N: 2 * pi * N / 60          # tr/min → rad/s

# ── Idée physique et §1 ───────────────────────────────────────────────────
verifier("Idée : p = 1, 50 Hz → N (tr/min)", 60 * 50 / 1, 3000, tol=1e-9)
verifier("§1 : p = 2, 50 Hz → N (tr/min)", 60 * 50 / 2, 1500, tol=1e-9)
verifier("§1 : alternateur à 100 tr/min → p", 60 * 50 / 100, 30, tol=1e-9)
verifier("§2 : X_s à 3 000 / X_s à 1 000 tr/min", 3000 / 1000, 3, tol=1e-9)

# ── Figure 4 : moteur surexcité (phi = 20° d'avance, X I = 0,5 V) ────────
V4, phi4, xi4 = 1.0, radians(20), 0.5
I4 = complex(cos(phi4), sin(phi4))                  # courant en avance
E4 = V4 - 1j * xi4 * I4
d4 = -atan2(E4.imag, E4.real)
vrai("Figure 4 : E en retard (delta > 0) et E cos delta > V_s (surexcitée)",
     d4 > 0 and abs(E4) * cos(d4) > V4)
vrai("§3 : X I cos phi = E sin delta (figure 4)", abs(xi4 * cos(phi4) - abs(E4) * sin(d4)) < 1e-12)
vrai("§4 : V = E cos delta + X I sin(phi), phi = phi_v − phi_i = −20°",
     abs(V4 - (abs(E4) * cos(d4) + xi4 * sin(-phi4))) < 1e-12)

# ── Figure 6 : courbes en V, en valeurs réduites ─────────────────────────
def courbe_v(e, Pr):
    """I/(V/X) à P/(3V²/X) = Pr fixé : E cos delta = sqrt(E² − Pr²), E sin delta = Pr."""
    return abs(1 - complex(sqrt(e * e - Pr * Pr), -Pr)) if e >= Pr else float("nan")


for Pr in (0.4, 0.8):
    I_min, E_min = Pr, sqrt(1 + Pr ** 2)            # cos phi = 1
    E_lim, I_lim = Pr, sqrt(1 + Pr ** 2)            # delta = 90°
    vrai(f"Figure 6, P = {Pr} : minimum I = P à E = sqrt(1 + P²)",
         abs(courbe_v(E_min, Pr) - I_min) < 1e-12
         and all(courbe_v(E_min + h, Pr) > I_min for h in (-0.05, 0.05)))
    vrai(f"Figure 6, P = {Pr} : limite delta = 90° en E = P, I = sqrt(1 + P²)",
         abs(courbe_v(E_lim, Pr) - I_lim) < 1e-12)
vrai("Figure 6, P = 0 : deux droites, I = |1 − E|",
     all(abs(courbe_v(e, 0) - abs(1 - e)) < 1e-12 for e in (0, 0.5, 1.5, 2)))

# ── Figure 9 : BLDC, couple constant ─────────────────────────────────────
def trapeze(t):
    """f.é.m. de la phase a, palier +1 de 30° à 150°, −1 de 210° à 330°."""
    t %= 360
    if t < 30:
        return t / 30
    if t < 150:
        return 1.0
    if t < 210:
        return 1 - (t - 150) / 30
    if t < 330:
        return -1.0
    return -1 + (t - 330) / 30


def creneau(t):
    t %= 360
    return 1.0 if 30 <= t < 150 else (-1.0 if 210 <= t < 330 else 0.0)


puiss = [sum(trapeze(t - k) * creneau(t - k) for k in (0, 120, 240)) for t in [x / 4 for x in range(1440)]]
vrai("Figure 9 : e_a i_a + e_b i_b + e_c i_c = 2 E_0 I à chaque instant", max(abs(q - 2) for q in puiss) < 1e-12)
hall = [(30, 210), (150, 330), (270, 450)]
fronts = sorted({a % 360 for a, b in hall} | {b % 360 for a, b in hall})
vrai("Figure 9 : six fronts de Hall, tous les 60°, aux commutations", fronts == [30, 90, 150, 210, 270, 330])

# ── Méthode : 2024-E1 ────────────────────────────────────────────────────
v0 = 60 / 3.6
W45 = v0 / 0.2
verifier("Q45 : v = 60 km/h (m/s)", v0, 16.67, tol=0.001)
verifier("Q45 : Omega (rad/s)", W45, 83.3, tol=0.001)
verifier("Q45 : N (tr/min)", W45 * 30 / pi, 796, tol=0.001)
verifier("Q45 : f0 (Hz), p = 14", 14 * W45 / (2 * pi), 186, tol=0.002)
verifier("Q45 : f0 avec p = 28 par erreur (Hz)", 28 * W45 / (2 * pi), 371, tol=0.002)
verifier("Q46 : 72/sqrt(3) (V)", 72 / sqrt(3), 41.6, tol=0.001)
verifier("Q50 : énergie cinétique, 1 t à 60 km/h (kJ)", 0.5 * 1000 * v0 ** 2 / 1e3, 139, tol=0.002)

# ── Méthode : 2020-E1 ────────────────────────────────────────────────────
F6 = 78 * (9.81 + 1)
verifier("Q6 : F_m (N)", F6, 843, tol=0.001)
verifier("Q7 : P à 1 m/s (W)", F6 * 1, 843, tol=0.001)
verifier("Q8 : P à l'arbre, rendement 0,8 (W)", F6 / 0.8, 1054, tol=0.001)
verifier("Q8 : 3 000 tr/min en rad/s", tr(3000), 314.2, tol=0.001)
verifier("Q8 : LT098-2-B, 4,6 N·m (W)", 4.6 * tr(3000), 1445, tol=0.001)
verifier("Q8 : LT088-4-B, 2,5 N·m (W)", 2.5 * tr(3000), 785, tol=0.001)
verifier("Q8 : LT098-1-B, 2,3 N·m (W)", 2.3 * tr(3000), 723, tol=0.001)
verifier("Q8 : couple requis à 3 000 tr/min (N·m)", F6 / 0.8 / tr(3000), 3.36, tol=0.003)
d_pig = 3.18 * 24
verifier("Q8 : diamètre du pignon mZ (mm)", d_pig, 76.3, tol=0.001)
N_pig = 1 / (d_pig / 2000) * 30 / pi
verifier("Q8 : pignon à 1 m/s (tr/min)", N_pig, 250, tol=0.002)
verifier("Q8 : rapport de réduction", 3000 / N_pig, 12, tol=0.002)

# ── Pièges ────────────────────────────────────────────────────────────────
verifier("Piège : composée crête / 1000 tr/min ↔ simple efficace / rad/s", sqrt(3) * sqrt(2) * tr(1000), 256.5, tol=0.0005)
verifier("Piège : 1 000 tr/min en rad/s", tr(1000), 104.7, tol=0.0005)

# ── Exemple chiffré ──────────────────────────────────────────────────────
p, Ke, Rs, Ls, Vdc = 4, 0.6, 0.15, 2.5e-3, 560
N1 = 3000
f1 = p * N1 / 60
w1 = 2 * pi * f1
W1 = tr(N1)
E1 = Ke * W1
X1 = Ls * w1
verifier("Ex. 1 : f (Hz)", f1, 200, tol=1e-9)
verifier("Ex. 1 : omega (rad/s)", w1, 1256.6, tol=0.0001)
verifier("Ex. 1 : Omega (rad/s)", W1, 314.16, tol=0.0001)
verifier("Ex. 1 : E (V)", E1, 188.5, tol=0.001)
verifier("Ex. 1 : X_s (ohms)", X1, 3.14, tol=0.002)
I1 = 20 / (3 * Ke)
verifier("Ex. 2 : I_q (A)", I1, 11.1, tol=0.002)
verifier("Ex. 2 : 3 K_e (N·m/A)", 3 * Ke, 1.8, tol=1e-9)
verifier("Ex. 2 : P_em = C Omega (W)", 20 * W1, 6283, tol=0.001)
verifier("Ex. 2 : P_em = 3 E I_q (W)", 3 * E1 * I1, 6283, tol=0.001)
vq, vd = E1 + Rs * I1, X1 * I1
V1 = hypot(vq, vd)
verifier("Ex. 3 : R_s I_s (V)", Rs * I1, 1.7, tol=0.02)
verifier("Ex. 3 : E + R_s I_s (V)", vq, 190.2, tol=0.001)
verifier("Ex. 3 : X_s I_s (V)", vd, 34.9, tol=0.002)
verifier("Ex. 3 : V_s (V)", V1, 193.3, tol=0.001)
phi1 = degrees(atan(vd / vq))
verifier("Ex. 3 : phi (°)", phi1, 10.4, tol=0.003)
verifier("Ex. 3 : cos phi", cos(radians(phi1)), 0.984, tol=0.001)
verifier("Ex. 3 : U (V)", sqrt(3) * V1, 334.9, tol=0.001)
Umax = sqrt(3) / (2 * sqrt(2)) * Vdc
verifier("Ex. 3 : 0,612 V_DC (V)", Umax, 342.9, tol=0.001)
verifier("Ex. 3 : coefficient 0,612", sqrt(3) / (2 * sqrt(2)), 0.612, tol=0.001)
verifier("Ex. 3 : m_a", sqrt(3) * V1 / Umax, 0.977, tol=0.001)
PJ = 3 * Rs * I1 ** 2
Pem = 20 * W1
Pa = Pem + PJ
verifier("Ex. 4 : P_Js (W)", PJ, 55.6, tol=0.001)
verifier("Ex. 4 : P_a (W)", Pa, 6339, tol=0.001)
verifier("Ex. 4 : 3 V I cos phi = P_a (W)", 3 * V1 * I1 * cos(radians(phi1)), 6339, tol=0.001)
Pu = Pem - 180
verifier("Ex. 4 : P_u (W)", Pu, 6103, tol=0.001)
verifier("Ex. 4 : C_u (N·m)", Pu / W1, 19.4, tol=0.003)
verifier("Ex. 4 : rendement (%)", 100 * Pu / Pa, 96.3, tol=0.001)
Vmax = Umax / sqrt(3)
verifier("Ex. 5 : V_s max (V)", Vmax, 198.0, tol=0.001)
Wb = bissection(lambda W: hypot(Ke * W + Rs * I1, Ls * p * W * I1) - Vmax, 250, 400)
verifier("Ex. 5 : vitesse de base à 20 N·m, psi = 0 (tr/min)", Wb * 30 / pi, 3070, tol=0.002)
W2 = tr(3600)
E2, X2 = Ke * W2, Ls * p * W2
Iq2 = 10 / (3 * Ke)
verifier("Ex. 5 : Omega à 3 600 tr/min (rad/s)", W2, 377.0, tol=0.001)
verifier("Ex. 5 : E (V)", E2, 226.2, tol=0.001)
verifier("Ex. 5 : X_s (ohms)", X2, 3.77, tol=0.002)
verifier("Ex. 5 : I_q (A)", Iq2, 5.56, tol=0.002)
Vd2 = -X2 * Iq2
Vq2 = sqrt(Vmax ** 2 - Vd2 ** 2)
Id2 = (Vq2 - E2) / X2
I2 = hypot(Id2, Iq2)
verifier("Ex. 5 : V_d (V)", Vd2, -20.9, tol=0.003)
verifier("Ex. 5 : V_q (V)", Vq2, 196.9, tol=0.001)
verifier("Ex. 5 : I_d (A)", Id2, -7.8, tol=0.005)
verifier("Ex. 5 : I_s (A)", I2, 9.6, tol=0.005)
verifier("Ex. 5 : psi (°)", degrees(atan(-Id2 / Iq2)), 54, tol=0.01)
verifier("Ex. 5 : I_s / I à 20 N·m (%)", 100 * I2 / I1, 86, tol=0.005)
vrai("Ex. 5 : chute R_s I_s ≤ 1,5 V", Rs * I2 <= 1.5)
Vd2r, Vq2r = -X2 * Iq2 + Rs * Id2, E2 + X2 * Id2 + Rs * Iq2
vrai("Ex. 5 : avec R_s, |V_s| reste à 1 % de 198 V", abs(hypot(Vd2r, Vq2r) - Vmax) / Vmax < 0.01)
verifier("Ex. 6 : constante catalogue (V par 1 000 tr/min)", sqrt(3) * sqrt(2) * Ke * tr(1000), 154, tol=0.003)
verifier("Ex. 6 : X_s I_s / E (%)", 100 * vd / E1, 18, tol=0.03)
verifier("Ex. 6 : angle E → V_s (°)", phi1, 10, tol=0.05)

# ── Auto-test ────────────────────────────────────────────────────────────
verifier("Q1 : p à 125 tr/min", 3000 / 125, 24, tol=1e-9)
verifier("Q2 : 400/sqrt(3) (V)", 400 / sqrt(3), 231, tol=0.002)
V, E, X, P = 230, 250, 5, 20e3
verifier("Q3 : sin delta", P * X / (3 * V * E), 0.580, tol=0.001)
verifier("Q3 : 3 V E", 3 * V * E, 172500, tol=1e-9)
d = asin(P * X / (3 * V * E))
verifier("Q3 : delta (°)", degrees(d), 35.4, tol=0.002)
verifier("Q3 : P_max (kW)", 3 * V * E / X / 1e3, 34.5, tol=1e-9)
verifier("Q3 : Omega, 4 pôles (rad/s)", tr(1500), 157.08, tol=0.0001)
verifier("Q3 : C_max (N·m)", 3 * V * E / X / tr(1500), 220, tol=0.003)
verifier("Q3 : couple de charge (N·m)", P / tr(1500), 127, tol=0.003)
verifier("Q4 : E cos delta (V)", E * cos(d), 203.7, tol=0.001)
Q = 3 * V * (V - E * cos(d)) / X
verifier("Q4 : Q (kvar)", Q / 1e3, 3.63, tol=0.002)
Ic = (V - E * complex(cos(d), -sin(d))) / (1j * X)
verifier("Q4 : I_s (A), par le complexe", abs(Ic), 29.5, tol=0.002)
verifier("Q4 : I_s = sqrt(P² + Q²)/(3V) (A)", hypot(P, Q) / (3 * V), 29.5, tol=0.002)
verifier("Q4 : phi (°)", degrees(atan(Q / P)), 10.3, tol=0.003)
vrai("Q4 : courant en retard (phi > 0 avec phi = phi_v − phi_i)", -atan2(Ic.imag, Ic.real) > 0)
verifier("Q4 : I à cos phi = 1 (A)", P / (3 * V), 29.0, tol=0.002)
verifier("Q4 : E pour cos phi = 1 (V)", hypot(V, X * P / (3 * V)), 272, tol=0.002)
verifier("Q5 : fréquence de Hall (Hz)", 4 * 3000 / 60, 200, tol=1e-9)
verifier("Q5 : commutations par seconde", 6 * 200, 1200, tol=1e-9)
verifier("Q5 : commutations par tour", 6 * 4, 24, tol=1e-9)
Id6 = (Vmax - E2) / X2
verifier("Q6 : I_d à vide, 3 600 tr/min (A)", Id6, -7.5, tol=0.005)
verifier("Q6 : pertes Joule (W)", 3 * Rs * Id6 ** 2, 25, tol=0.02)

print()
if ECARTS:
    print(f"{len(ECARTS)} écart(s) :", ", ".join(ECARTS))
    raise SystemExit(1)
print("Aucun écart.")
