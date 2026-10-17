"""Applications numériques du chapitre T14, refaites en Python.

    python3 cours/calculs/T14.py

Chaque bloc reprend une valeur publiée dans cours/textes/T14.html ; un
écart supérieur à la demi-unité du dernier chiffre publié fait échouer le
script (tolérance relative explicite pour une valeur annoncée « environ »).
La figure 4 est resimulée (redresseur à diodes, bus LC, charge résistive).
"""
from decimal import Decimal
from math import sqrt, pi, sin

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


tr = lambda N: 2 * pi * N / 60          # tr/min → rad/s

# ── §1 : pompes et ventilateurs ──────────────────────────────────────────
verifier("§1 : puissance à 80 % de la vitesse (%)", 100 * 0.8 ** 3, 51)

# ── §2 : bus continu, onduleur ───────────────────────────────────────────
verifier("§2 : 3 sqrt(2) U / pi, U = 400 V (V)", 3 * sqrt(2) * 400 / pi, 540)
verifier("§2 : sqrt(2) U (V)", sqrt(2) * 400, 566)
verifier("§2 : 0,612 × 540 (V)", sqrt(3) / (2 * sqrt(2)) * 540, 331)
verifier("§2 : 0,707 × 540 (V)", 540 / sqrt(2), 382)


def sim_pd3(L, C=1e-3, P=11e3, U=400, f=50, T=0.4, dt=2e-6):
    """Pont à diodes, bus L puis C, charge résistive de puissance P.

    Renvoie le THD du courant de ligne, le courant de bus minimal et la part de la période
    où la phase a conduit, sur la dernière période."""
    w = 2 * pi * f
    Vm = U * sqrt(2) / sqrt(3)
    R = (1.35 * U) ** 2 / P
    i, v = 0.0, U * sqrt(2) * 0.95
    n = int(T / dt)
    N = int(round(1 / f / dt))
    ia, ibus = [], []
    for k in range(n):
        t = k * dt
        va, vb, vc = (Vm * sin(w * t - 2 * pi * m / 3) for m in range(3))
        vmax, vmin = max(va, vb, vc), min(va, vb, vc)
        i = max(0.0, i + (vmax - vmin - v) / L * dt)
        v += (i - v / R) / C * dt
        if k >= n - N:
            ia.append(i if va == vmax else (-i if va == vmin else 0.0))
            ibus.append(i)
    # composantes de Fourier, rangs 1 à 59
    amp = []
    for h in range(1, 60):
        a = sum(x * __import__('math').cos(2 * pi * h * j / N) for j, x in enumerate(ia)) * 2 / N
        b = sum(x * sin(2 * pi * h * j / N) for j, x in enumerate(ia)) * 2 / N
        amp.append(sqrt(a * a + b * b))
    thd = sqrt(sum(x * x for x in amp[1:])) / amp[0]
    return thd, min(ibus), sum(1 for x in ia if abs(x) > 1e-9) / N


(thd_05, imin_05, cond_05), (thd_5, imin_5, cond_5) = sim_pd3(0.5e-3), sim_pd3(5e-3)
verifier("Fig. 4 : THD avec 0,5 mH (%)", 100 * thd_05, 100, tol=0.03)
verifier("Fig. 4 : THD avec 5 mH (%)", 100 * thd_5, 33, tol=0.03)
vrai("§2 : conduction discontinue à 0,5 mH (courant de bus nul par instants)", imin_05 == 0.0)
vrai("§2 : conduction continue à 5 mH (courant de bus jamais nul)", imin_5 > 0.0)
verifier("§2 : 5 mH, conduction de la phase a par période (°)", 360 * cond_5, 240, tol=0.01)

# ── §6 : énergie stockée par le bus ──────────────────────────────────────
E_bus = 0.5 * 1e-3 * (750 ** 2 - 540 ** 2)
verifier("§6 : énergie du bus 1 mF, 540 → 750 V (J)", E_bus, 135)
vrai("§6 : moins d'un dixième de seconde à 1,6 kW", E_bus / 1600 < 0.1)

# ── §3 : figure 5 ─────────────────────────────────────────────────────────
verifier("§3 : cassure du transitoire, 2,5/1,5 (N/N_n)", 2.5 / 1.5, 1.67)
trans = lambda x: 1.5 if x <= 1 else min(1.5 / x, 2.5 / x ** 2)
vrai("§3 : transitoire en 1,5/x entre 1 et 1,67", all(abs(trans(x) - 1.5 / x) < 1e-12 for x in (1.1, 1.4, 1.66)))
vrai("§3 : transitoire en 2,5/x² au-delà de 1,67", all(abs(trans(x) - 2.5 / x ** 2) < 1e-12 for x in (1.7, 2.0, 2.5)))

# ── Méthode : 2021-E2 ────────────────────────────────────────────────────
In_m = 90000 / (0.942 * sqrt(3) * 400 * 0.86)
verifier("2021-E2 Q16 : I_n du moteur (A)", In_m, 160.4)
verifier("2021-E2 Q16 : 150 % de I_n (A)", 1.5 * In_m, 240.5)
vrai("2021-E2 Q16 : D90N4 en usage intensif, 145 A < I_n", 145 < In_m)
vrai("2021-E2 Q16 : C11N4 en usage intensif, 173 A ≥ I_n et 259,5 A ≥ 1,5 I_n", 173 >= In_m and 259.5 >= 1.5 * In_m)
verifier("2021-E2 Q16 : transitoire HD = 1,5 × 173 (A)", 1.5 * 173, 259.5)
verifier("2021-E2 Q16 : C11N4 en usage normal, transitoire / permanent", 232.1 / 211, 1.1)
verifier("2021-E2 Q18 : 0,2 × 173 (A)", 0.2 * 173, 34.6)
verifier("2021-E2 Q18 : borne haute de I_th = 1,1 × 173 (A)", 1.1 * 173, 190.3)
verifier("2021-E2 Q18 : usage normal, 0,2 × 211 (A)", 0.2 * 211, 42.2)
verifier("2021-E2 Q18 : usage normal, 1,1 × 211 (A)", 1.1 * 211, 232.1)
vrai("2021-E2 Q18 : 160 A dans la plage en usage normal", 42.2 <= 160 <= 232.1)
vrai("2021-E2 Q18 : 160 A dans la plage", 34.6 <= 160 <= 190.3)

verifier("2021-E2 Q15 : majorant du seuil, sqrt(135/162)", sqrt(135 / 162), 0.91)

# ── Méthode : 2023-E1 ────────────────────────────────────────────────────
for Q_, N_ in ((6900, 380), (10300, 570), (13700, 760), (16800, 950)):
    verifier(f"2023-E1 Q15 : débit / vitesse, {Q_} / {N_}, « environ »", Q_ / N_, 18, tol=0.03)
verifier("2023-E1 Q15 : 8 100 / 18 (tr/min)", 8100 / 18, 450)
verifier("2023-E1 Q15 : 14 200 / 18 (tr/min)", 14200 / 18, 790, tol=0.002)
kv = 16 / (1000 - 950)
verifier("2023-E1 Q19 : k (N·m par tr/min)", kv, 0.32)
for N_, Cr_p, dN_p, f_p in ((450, 3.58, 11.2, 23.1), (800, 11.3, 35.4, 41.8)):
    Cr_ = 1.77e-5 * N_ ** 2
    verifier(f"2023-E1 Q20 : C_r à {N_} tr/min (N·m)", Cr_, Cr_p)
    verifier(f"2023-E1 Q20 : N_s − N à {N_} tr/min", Cr_ / kv, dN_p)
    verifier(f"2023-E1 Q20 : f à {N_} tr/min (Hz)", (N_ + Cr_ / kv) / 20, f_p)
verifier("2023-E1 Q25 : 0x01A2 / 10 (Hz)", 0x01A2 / 10, 41.8)
verifier("2023-E1 Q25 : 0x0FA0", 0x0FA0, 4000)

# ── Méthode : 2024-E2 ────────────────────────────────────────────────────
A = 3 * 2 * 230 ** 2 / (0.1 * (2 * pi * 50) ** 2)
verifier("2024-E2 C2 : A (N·m·s/rad)", A, 32.2)
verifier("2024-E2 C3 : K_méca = 1/f", 1 / 4e-3, 250)
verifier("2024-E2 C3 : tau_méca = J/f (s)", 0.035 / 4e-3, 8.75)

# ── Méthode : 2024-E1 ────────────────────────────────────────────────────
Ec_caps = 0.5 * 1000 * (60 / 3.6) ** 2
verifier("2024-E1 Q50 : énergie cinétique (kJ)", Ec_caps / 1e3, 138.9)
verifier("2024-E1 Q51 : 5 × 16,2 V", 5 * 16.2, 81)
verifier("2024-E1 Q51 : 65 F / 5", 65 / 5, 13)
Ef = 0.5 * 13 * 72 ** 2 + 0.8 * Ec_caps
verifier("2024-E1 Q52 : énergie initiale, 72 V (kJ)", 0.5 * 13 * 72 ** 2 / 1e3, 33.7)
verifier("2024-E1 Q52 : 80 % de 138,9 kJ (kJ)", 0.8 * 138.9, 111.1)
verifier("2024-E1 Q52 : énergie finale (kJ)", Ef / 1e3, 144.8)
verifier("2024-E1 Q52 : tension finale (V)", sqrt(2 * Ef / 13), 149)

# ── Méthode : 2023-E2 et 2017-E1 ─────────────────────────────────────────
eta_ch = 0.98 * 0.8 * 0.8
verifier("2023-E2 A7 : rendement de la chaîne", eta_ch, 0.627)
for M_, Pm_p, Pe_p in ((2500, 3585, 5715), (2450, None, 5672), (2400, None, 5629)):
    Pm_ = (0.05 * M_ * 9.81 + 2000) * 4 / 3.6
    if Pm_p:
        verifier(f"2023-E2 A6 : P_m pour {M_} kg (W)", Pm_, Pm_p)
    verifier(f"2023-E2 A7 : P_e pour {M_} kg (W)", Pm_ / eta_ch, Pe_p)
verifier("2017-E1 Q7 : beta M6 (kW par km/h)", 1.36e-2 * 181000 / 1e3, 2.46)
pts = ((48, 123), (53, 110))         # notre relevé du DR1, autour de l'intersection
(v1, p1), (v2, p2) = pts
b_ = 1.36e-2 * 181000 / 1e3
vi = (p1 - (p2 - p1) / (v2 - v1) * v1) / (b_ - (p2 - p1) / (v2 - v1))
verifier("2017-E1 Q7 : vitesse d'intersection (km/h)", vi, 49)
verifier("2017-E1 Q7 : puissance à l'intersection, « environ » (kW)", b_ * vi, 120, tol=0.01)
verifier("2017-E1 : puissance en 1/V, 123 × 48/70 (kW)", 123 * 48 / 70, 84)
for v_, p_ in ((53, 110), (57.5, 101), (62, 93.5), (70, 84)):   # autres points de notre relevé
    verifier(f"2017-E1 : loi en 1/V à {v_} km/h, relevé {p_} kW", 123 * 48 / v_, p_, tol=0.025)
W48 = 7.28 * 48 / 3.6 / 0.4
verifier("2017-E1 : couple de décrochage à 48 km/h (N·m)", 123e3 / W48, 507)
verifier("2017-E1 : ramené à 29 km/h en (48/29)², « environ » (N·m)", 123e3 / W48 * (48 / 29) ** 2, 1390, tol=0.005)
verifier("2017-E1 : 885 N·m en 1/f² dès 29 km/h, à 48 km/h, « environ » (kW)", 885 * (29 / 48) ** 2 * W48 / 1e3, 78, tol=0.01)
verifier("2017-E1 : vitesse du moteur à 29 km/h (rad/s)", 7.28 * 29 / 3.6 / 0.4, 146.6)
verifier("2017-E1 : couple à 29 km/h pour 135 kW, « environ » (N·m)", 135e3 / (7.28 * 29 / 3.6 / 0.4), 920, tol=0.005)

# ── Exemple chiffré : palan ──────────────────────────────────────────────
Pn, Nn, In, cosp, U = 4000, 1440, 8.2, 0.82, 400
Cn = Pn / tr(Nn)
Pa = sqrt(3) * U * In * cosp
verifier("Ex. 1 : C_n (N·m)", Cn, 26.5)
verifier("Ex. 1 : P_a (W)", Pa, 4659)
verifier("Ex. 1 : rendement (%)", 100 * Pn / Pa, 85.9)
k = Cn / (1500 - Nn)
verifier("Ex. 1 : k (N·m par tr/min)", k, 0.442)
m, g, r, red, eta, v = 800, 9.81, 0.1, 50, 0.85, 0.25
Wm = v / r * red
verifier("Ex. 2 : vitesse du tambour (rad/s)", v / r, 2.5)
verifier("Ex. 2 : vitesse du moteur (rad/s)", Wm, 125)
verifier("Ex. 2 : vitesse du moteur (tr/min)", Wm * 30 / pi, 1194)
Cm = m * g * r / (red * eta)
verifier("Ex. 2 : couple en montée (N·m)", Cm, 18.5)
verifier("Ex. 2 : C / C_n (%)", 100 * Cm / Cn, 70)
dN = Cm / k
Ns = Wm * 30 / pi + dN
verifier("Ex. 2 : écart au synchronisme (tr/min)", dN, 41.8)
verifier("Ex. 2 : N_s (tr/min)", Ns, 1235.4)
verifier("Ex. 2 : f (Hz)", 2 * Ns / 60, 41.2)
verifier("Ex. 2 : V_s (V)", 230 * (2 * Ns / 60) / 50, 189)
verifier("Ex. 2 : puissance du moteur (kW)", Cm * Wm / 1e3, 2.31)
verifier("Ex. 2 : m g v (W)", m * g * v, 1962)
Cd = m * g * r * eta / red
dNd = Cd / k
Nsd = Wm * 30 / pi - dNd
verifier("Ex. 3 : couple en descente (N·m)", Cd, 13.3)
verifier("Ex. 3 : |N| du moteur (tr/min)", Wm * 30 / pi, 1193.7)
verifier("Ex. 3 : |N_s| (tr/min)", Nsd, 1163.5)
verifier("Ex. 3 : f (Hz)", 2 * Nsd / 60, 38.8)
verifier("Ex. 3 : Omega_s (rad/s)", tr(Nsd), 121.8)
Pt = Cd * tr(Nsd)
verifier("Ex. 3 : puissance transmise (kW)", Pt / 1e3, 1.63)
verifier("Ex. 4 : énergie du bus (J)", E_bus, 135)
verifier("Ex. 4 : durée de charge du bus (s)", E_bus / Pt, 0.08)
verifier("Ex. 4 : R_f maxi (ohms)", 750 ** 2 / Pt, 346)
verifier("Ex. 4 : 750²/1 625 (ohms)", 750 ** 2 / 1625, 346)
verifier("Ex. 4 : puissance au seuil avec 100 ohms (kW)", 750 ** 2 / 100 / 1e3, 5.6)
verifier("Ex. 4 : énergie d'une descente de 10 m (kJ)", Pt * 10 / v / 1e3, 65)
verifier("Ex. 4 : durée de la descente (s)", 10 / v, 40)
J = 0.012 + m * (r / red) ** 2
verifier("Ex. 5 : (r/50)", r / red, 0.002)
verifier("Ex. 5 : inertie de la charge ramenée (kg·m²)", m * (r / red) ** 2, 0.0032)
Cacc_ch = m * (r / red) ** 2 * Wm / eta
verifier("Ex. 5 : accélération de la charge, rendement compris (N·m)", Cacc_ch, 0.47)
verifier("Ex. 5 : accélération moteur et réducteur (N·m)", 0.012 * Wm, 1.5)
Ctot = Cm + Cacc_ch + 0.012 * Wm
verifier("Ex. 5 : couple total (N·m)", Ctot, 20.4)
verifier("Ex. 5 : couple total / C_n (%)", 100 * Ctot / Cn, 77)
verifier("Ex. 6 : Omega_s − Omega à 41 Hz (rad/s)", tr(dN), 4.37)
verifier("Ex. 6 : pertes Joule du rotor à 41 Hz (W)", Cm * tr(dN), 81)
verifier("Ex. 6 : pertes Joule du rotor au nominal (W)", Cn * tr(60), 167)
verifier("Ex. 6 : vitesse / N_n (%)", 100 * (Wm * 30 / pi) / Nn, 83)

# ── Auto-test ────────────────────────────────────────────────────────────
verifier("Q1 : puissance (%)", 100 * 0.8 ** 3, 51)
verifier("Q2 : bus en charge (V)", 3 * sqrt(2) * 400 / pi, 540)
verifier("Q2 : à vide (V)", sqrt(2) * 400, 566)
thd = sqrt(0.35 ** 2 + 0.20 ** 2 + 0.08 ** 2 + 0.06 ** 2)
verifier("Q3 : THD", thd, 0.415)
verifier("Q3 : THD (%)", 100 * thd, 41.5)
verifier("Q3 : I / I_1", sqrt(1 + thd ** 2), 1.08)
verifier("Q4 : N_s (tr/min)", 900 + 20 / 0.5, 940)
verifier("Q4 : f (Hz)", 2 * 940 / 60, 31.3)
verifier("Q5 : 1 500 tr/min (rad/s)", tr(1500), 157.08)
verifier("Q5 : temps d'accélération (s)", 0.5 * tr(1500) / 30, 2.6)
Ec = 0.5 * 2 * tr(1500) ** 2
verifier("Q6 : énergie cinétique (kJ)", Ec / 1e3, 24.7)
verifier("Q6 : énergie du bus 2 mF (J)", 0.5 * 2e-3 * (780 ** 2 - 560 ** 2), 295)
verifier("Q6 : puissance initiale 2E/t (kW)", 2 * Ec / 2 / 1e3, 24.7)
verifier("Q6 : puissance initiale, sans arrondir (W)", 2 * Ec / 2, 24674)
verifier("Q6 : R_f maxi (ohms)", 780 ** 2 / 24674, 24.7)
verifier("Q6 : R_f maxi, puissance exacte (ohms)", 780 ** 2 / (2 * Ec / 2), 24.7)

print()
if ECARTS:
    print(f"{len(ECARTS)} écart(s) :", ", ".join(ECARTS))
    raise SystemExit(1)
print("Aucun écart.")
