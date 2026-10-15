"""Applications numériques du chapitre T26, refaites en Python.

    python3 cours/calculs/T26.py

Chaque bloc reprend une valeur publiée dans cours/textes/T26.html ; un
écart de plus de 0,5 % sur la valeur arrondie fait échouer le script.
Les transformées de Laplace sont vérifiées par intégration numérique, les
fonctions de transfert par évaluation en des points p complexes et par
simulation temporelle des équations différentielles (Euler, pas fin).
"""
from math import sqrt, pi, log, log10, exp, acos, atan, degrees

import numpy as np

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


def laplace(fn, p, T=60.0, n=600001):
    t = np.linspace(0, T, n)
    y = fn(t) * np.exp(-p * t)
    return np.trapezoid(y, t) if hasattr(np, 'trapezoid') else np.trapz(y, t)


def reponse2(m, u):
    """Réponse indicielle unitaire réduite d'un second ordre (temps ω0·t)."""
    if m < 1:
        w = sqrt(1 - m * m)
        return 1 - np.exp(-m * u) / w * np.sin(w * u + acos(m))
    if m == 1:
        return 1 - (1 + u) * np.exp(-u)
    r = sqrt(m * m - 1); a1, a2 = -(m - r), -(m + r)
    return 1 - (a2 * np.exp(a1 * u) - a1 * np.exp(a2 * u)) / (a2 - a1)


def t5_reduit(m, T=None):
    T = T or max(40.0, 14 / m, 14 * m)
    u = np.linspace(0, T, 400001)
    s = reponse2(m, u)
    return u[np.where(np.abs(s - 1) > 0.05)[0][-1] + 1]


print("— §1 Linéarisation (2025-E2)")
Eb0, un_a0 = 48.0, 48 / 230
verifier("pente ∂V_DC/∂α ≈ 1 102 V", Eb0 / un_a0 ** 2, 1102, tol=0.001)
verifier("échelon de 1 % : 11,0 V", 0.01 * Eb0 / un_a0 ** 2, 11.0, tol=0.003)
# Vérification par la non-linéarité elle-même : V(α0 + 0,005) − V(α0 − 0,005)
a0 = 1 - un_a0
verifier("… différence finie de E_b/(1 − α) sur ±0,5 %", 48 / (1 - (a0 + 0.005)) - 48 / (1 - (a0 - 0.005)), 11.0, tol=0.01)

print("— §2 Table de Laplace (intégration numérique en p = 2)")
p, tau, a, w = 2.0, 0.7, 1.3, 3.0
verifier("échelon : 1/p", laplace(lambda t: np.ones_like(t), p), 1 / p, tol=1e-4)
verifier("rampe a t : a/p²", laplace(lambda t: a * t, p), a / p ** 2, tol=1e-4)
verifier("exponentielle : τ/(1 + τp)", laplace(lambda t: np.exp(-t / tau), p), tau / (1 + tau * p), tol=1e-4)
verifier("montée du premier ordre : 1/[p(1 + τp)]", laplace(lambda t: 1 - np.exp(-t / tau), p), 1 / (p * (1 + tau * p)), tol=1e-4)
verifier("sinus : ω/(p² + ω²)", laplace(lambda t: np.sin(w * t), p, n=2000001), w / (p * p + w * w), tol=1e-4)
f0 = 0.4
verifier("dérivée ordinaire : pF(p) − f(0⁺), f = 0,4 + e^{−t}",
         laplace(lambda t: -np.exp(-t), p), p * laplace(lambda t: f0 + np.exp(-t), p) - (f0 + 1), tol=1e-4)
# Au sens des distributions, le saut de 1,4 en 0 ajoute 1,4·δ : ℒ{f'} = pF(p) − f(0⁻), f(0⁻) = 0
verifier("dérivée au sens des distributions : pF(p) − f(0⁻)",
         laplace(lambda t: -np.exp(-t), p) + (f0 + 1), p * laplace(lambda t: f0 + np.exp(-t), p) - 0, tol=1e-4)
T0 = 0.4
verifier("retard : e^{−T0 p}/p", laplace(lambda t: (t >= T0).astype(float), p, n=2000001), exp(-T0 * p) / p, tol=1e-3)

print("— §4 Premier ordre")
verifier("s(τ) = 63,2 %", 1 - exp(-1), 0.632, tol=0.001)
verifier("s(3τ) = 95,0 %", 1 - exp(-3), 0.950, tol=0.001)
verifier("s(5τ) = 99,3 %", 1 - exp(-5), 0.993, tol=0.001)
verifier("t5 % = τ ln 20 ≈ 3,0 τ", log(20), 3.0, tol=0.002)

print("— §5 Second ordre")
D = lambda m: exp(-pi * m / sqrt(1 - m * m))
verifier("D(0,707) = 4,3 %", 100 * D(0.707), 4.3, tol=0.01)
verifier("D(0,69) ≈ 5 %", 100 * D(0.69), 5.0, tol=0.01)
verifier("D(0,5) = 16 %", 100 * D(0.5), 16.0, tol=0.02)
verifier("D(0,3) = 37 %", 100 * D(0.3), 37.0, tol=0.01)
for m in (0.2, 0.5):
    u = np.linspace(0, 40, 400001)
    s = reponse2(m, u)
    verifier(f"m = {m} : maximum simulé = 1 + D", s.max(), 1 + D(m), tol=1e-4)
    verifier(f"m = {m} : instant du maximum = π/ω_p", u[np.argmax(s)], pi / sqrt(1 - m * m), tol=1e-3)
for m in (0.1, 0.3, 0.6):
    Dm = D(m)
    verifier(f"inversion m = |ln D|/√(π² + ln² D), m = {m}", abs(log(Dm)) / sqrt(pi ** 2 + log(Dm) ** 2), m, tol=1e-9)
ms = np.arange(0.60, 0.80, 0.001)
v = [t5_reduit(m) for m in ms]
i = int(np.argmin(v))
verifier("minimum de ω0·t5 % ≈ 2,9", v[i], 2.9, tol=0.02)
verifier("… pour m ≈ 0,69", ms[i], 0.69, tol=0.01)
verifier("ω0·t5 % ≈ 4,75 pour m = 1", t5_reduit(1.0), 4.75, tol=0.003)
verifier("m petit : ω0·t5 % ≈ 3/m (m = 0,05)", t5_reduit(0.05), 3 / 0.05, tol=0.05)
verifier("m grand : ω0·t5 % ≈ 6m (m = 10)", t5_reduit(10.0), 60, tol=0.01)

print("— §6 Schémas-blocs")
pz = 0.37 + 1.1j
HD, HR = 5 / (1 + 0.3 * pz), 0.8 / (1 + 0.05 * pz)
# boucle : système ε + H_R S = E, −H_D ε + S = 0, résolu pour E = 1
eps, S = np.linalg.solve(np.array([[1, HR], [-HD, 1]]), np.array([1, 0]))
verifier("boucle : H_D/(1 + H_D H_R) (module)", abs(S), abs(HD / (1 + HD * HR)), tol=1e-9)
Ka = Km = 2.0; Hc = 3 / (1 + pz)
verifier("retour unitaire : K_a H/(1 + K_m H) = K_m H/(1 + K_m H)", abs(Ka * Hc / (1 + Km * Hc)), abs(Km * Hc / (1 + Km * Hc)), tol=1e-12)
ph = lambda w: degrees(atan(w / 10) + atan(w / 1000))
lo, hi = 100.0, 10000.0
for _ in range(100):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if ph(mid) < 135 else (lo, mid)
wc = lo
G1 = -20 * log10(sqrt(1 + (wc / 10) ** 2) * sqrt(1 + (wc / 1000) ** 2))
verifier("figure 11 : ω_c ≈ 1 020 rad/s", wc, 1020, tol=0.002)
verifier("… G1 ≈ −43 dB", G1, -43.3, tol=0.002)
verifier("… K_C ≈ 146", 10 ** (-G1 / 20), 146, tol=0.003)

print("— §7 et exemple : machine à courant continu")
R, L, K, J, Cp, Cr, U = 0.8, 1.6e-3, 0.06, 4e-4, 0.02, 0.30, 24.0
te, tm = L / R, R * J / K ** 2
verifier("τe = 2,0 ms", te, 2.0e-3)
verifier("τm ≈ 88,9 ms", tm, 88.9e-3, tol=0.001)
verifier("1/K ≈ 16,7 rad·s⁻¹·V⁻¹", 1 / K, 16.7, tol=0.003)
verifier("τe τm ≈ 1,78·10⁻⁴ s²", te * tm, 1.78e-4, tol=0.002)
verifier("ω0 = 75 rad/s", 1 / sqrt(te * tm), 75)
verifier("m ≈ 3,33", 0.5 * sqrt(tm / te), 3.33, tol=0.002)
pl = sorted(np.roots([te * tm, tm, 1]).real)
verifier("pôle lent ≈ −11,5 rad/s", pl[1], -11.5, tol=0.002)
verifier("pôle rapide ≈ −488 rad/s", pl[0], -488, tol=0.002)
verifier("écart de constante de temps du premier ordre ≈ 2,4 %", (tm - (-1 / pl[1])) / (-1 / pl[1]), 0.024, tol=0.02)
# Fonction de transfert : formule du §7 contre représentation d'état (§8)
f_ = 1e-4
A = np.array([[-R / L, -K / L], [K / J, -f_ / J]]); B = np.array([[1 / L, 0], [0, -1 / J]]); C = np.array([[0, 1]])
for pz in (3 + 4j, 50j, 200 + 10j):
    Hs = (C @ np.linalg.inv(pz * np.eye(2) - A) @ B)[0]
    verifier(f"Ω/U, état contre formule, p = {pz}", abs(Hs[0]), abs(K / ((R + L * pz) * (f_ + J * pz) + K * K)), tol=1e-9)
    Hc_ = -(R + L * pz) / ((R + L * pz) * (f_ + J * pz) + K * K)
    verifier(f"Ω/C_r, état contre superposition, p = {pz}", abs(Hs[1]), abs(Hc_), tol=1e-9)
vrai("pôles = valeurs propres de A", np.allclose(sorted(np.linalg.eigvals(A).real),
                                                 sorted(np.roots([L * J, R * J + L * f_, R * f_ + K * K]).real)))
# Simulation de l'exemple, frottement nul, couple de pertes constant
dt = 1e-6; N = int(0.9 / dt)
i_, w_ = 0.0, 0.0
imax, timax, w_vide, t5 = 0.0, 0.0, None, None
traj = []
for k in range(N):
    t = k * dt
    cr = Cp + (Cr if t >= 0.5 else 0.0)
    di = (U - R * i_ - K * w_) / L
    dw = (K * i_ - cr) / J
    i_ += di * dt; w_ += dw * dt
    if i_ > imax:
        imax, timax = i_, t
    if k % 100 == 0 and t < 0.5:
        traj.append((t, w_))
    if abs(t - 0.4999) < dt / 2:
        w_vide = w_
traj = np.array(traj)
hors = np.where(np.abs(traj[:, 1] - w_vide) > 0.05 * w_vide)[0][-1] + 1
verifier("à vide : Ω = (U − R C_p/K)/K ≈ 395,6 rad/s", (U - R * Cp / K) / K, 395.6, tol=0.001)
verifier("… simulé à 0,5 s, résidu e^{−0,5/0,0868} compris", w_vide, 395.6 - 400 * exp(-0.5 / 0.08684) * 1.0, tol=0.002)
verifier("… soit 3 777 tr/min", (U - R * Cp / K) / K * 60 / (2 * pi), 3777, tol=0.001)
verifier("… I = C_p/K ≈ 0,33 A", Cp / K, 0.33, tol=0.02)
verifier("t5 % simulé ≈ 0,26 s", traj[hors, 0], 0.26, tol=0.03)
verifier("pic de courant ≈ 28 A", imax, 28, tol=0.01)
verifier("… vers 7,9 ms", timax, 7.9e-3, tol=0.01)
verifier("courant sans L : U/R = 30 A", U / R, 30)
verifier("pic / courant en charge > 5", imax / ((Cr + Cp) / K), 5.26, tol=0.01)
verifier("chute de vitesse R C_r/K² ≈ 66,7 rad/s", R * Cr / K ** 2, 66.7, tol=0.001)
Wc = (U - R * (Cr + Cp) / K) / K
verifier("en charge : Ω ≈ 328,9 rad/s", Wc, 328.9, tol=0.001)
verifier("… simulé", w_, 328.9, tol=0.002)
verifier("… soit 3 141 tr/min", Wc * 60 / (2 * pi), 3141, tol=0.001)
I = (Cr + Cp) / K
verifier("I ≈ 5,33 A", I, 5.33, tol=0.001)
verifier("E = KΩ ≈ 19,73 V", K * Wc, 19.73, tol=0.001)
verifier("RI ≈ 4,27 V", R * I, 4.27, tol=0.002)
verifier("P_A = UI ≈ 128 W", U * I, 128)
verifier("P_JR ≈ 22,8 W", R * I * I, 22.8, tol=0.002)
verifier("P_EM = EI ≈ 105,2 W", K * Wc * I, 105.2, tol=0.001)
verifier("… = C_em Ω", (Cr + Cp) * Wc, 105.2, tol=0.001)
verifier("P_FM ≈ 6,6 W", Cp * Wc, 6.6, tol=0.005)
verifier("P_U ≈ 98,7 W", Cr * Wc, 98.7, tol=0.001)
verifier("η ≈ 77 %", Cr * Wc / (U * I), 0.77, tol=0.005)
CU = lambda w, u: K / R * (u - K * w) - Cp
verifier("C_U(0) = 1,78 N·m", CU(0, U), 1.78)
verifier("pente 0,0045 N·m·s/rad", K * K / R, 0.0045)
verifier("C_U = 0,30 → Ω ≈ 328,9", (CU(0, U) - 0.30) / (K * K / R), 328.9, tol=0.001)
verifier("sous 12 V, la droite descend de 0,90 N·m", CU(0, U) - CU(0, 12), 0.90)
verifier("sous 12 V : Ω ≈ 128,9 rad/s", (CU(0, 12) - 0.30) / (K * K / R), 128.9, tol=0.001)
verifier("K_e = 6,28 V par millier de tr/min", K * 1000 * 2 * pi / 60, 6.28, tol=0.001)
verifier("0,06 V·s/rad = 6,28 mV/(tr/min)", K * 2 * pi / 60 * 1000, 6.28, tol=0.001)

print("— Méthode : 2024-E2")
f, Jm = 4e-3, 0.035
verifier("K_meca = 1/f = 250", 1 / f, 250)
verifier("τ_meca = J/f = 8,75 s", Jm / f, 8.75)
verifier("écart à 8,5 s ≈ 3 %", (Jm / f - 8.5) / 8.5, 0.03, tol=0.05)
Km_, tau_, Kp, Ki = 250.0, 8.5, 0.3, 2.5
for pz in (0.5 + 1j, 3j, 2 + 0.1j):
    Hm = Km_ / (1 + tau_ * pz)
    # Ω = Hm·Kp·(Ki/p·(Ωref − Ω) − Ω)  →  Ω/Ωref
    Hbf = (Hm * Kp * Ki / pz) / (1 + Hm * Kp + Hm * Kp * Ki / pz)
    kap = Ki * Kp * Km_
    verifier(f"H_bf = κ/(τ p² + (1 + K_p K_meca) p + κ), p = {pz}", abs(Hbf), abs(kap / (tau_ * pz ** 2 + (1 + Kp * Km_) * pz + kap)), tol=1e-9)
kap = Ki * Kp * Km_
w0 = sqrt(kap / tau_); m = (1 + Kp * Km_) / (2 * sqrt(kap * tau_))
verifier("forme canonique : 2m/ω0 = (1 + K_p K_meca)/κ", 2 * m / w0, (1 + Kp * Km_) / kap, tol=1e-9)
verifier("forme canonique : 1/ω0² = τ/κ", 1 / w0 ** 2, tau_ / kap, tol=1e-9)

# C8 : m = 1, ω0 = 5 rad/s, K_meca = 250, τ = 8,5 s
Kp8 = (2 * 1 * 5 * 8.5 - 1) / 250
kap8 = 8.5 * 25
verifier("C8 : 1 + K_p K_meca = 2mω0τ = 85", 2 * 1 * 5 * 8.5, 85)
verifier("C8 : K_p = 0,336", Kp8, 0.336, tol=0.001)
verifier("C8 : κ = τω0² = 212,5", kap8, 212.5)
verifier("C8 : K_i ≈ 2,53 s⁻¹", kap8 / (Kp8 * 250), 2.53, tol=0.002)

print("— Méthode : 2025-E2")
L2, C2, R0 = 10e-3, 220e-6, 17.7
Kg = Eb0 / un_a0 ** 2
w0b = un_a0 / sqrt(L2 * C2)
Tz = L2 / (R0 * un_a0 ** 2)
verifier("Q38 : gain statique ≈ 1 102 V", Kg, 1102, tol=0.001)
verifier("Q38 : ω0 ≈ 141 rad/s", w0b, 141, tol=0.003)
verifier("Q38 : m ≈ 0,91", w0b * Tz / 2, 0.91, tol=0.005)
verifier("Q38 : zéro ≈ +77 rad/s", 1 / Tz, 77, tol=0.003)
# Q37 → Q38 : expression du sujet et forme canonique, évaluées en p complexes
iL0 = Eb0 / (R0 * un_a0 ** 2); V0 = Eb0 / un_a0
for pz in (10 + 5j, 100j, 300 + 40j):
    h37 = (un_a0 * V0 - L2 * pz * iL0) / (un_a0 ** 2 + L2 / R0 * pz + L2 * C2 * pz ** 2)
    h38 = Kg * (1 - Tz * pz) / (1 + Tz * pz + L2 * C2 / un_a0 ** 2 * pz ** 2)
    verifier(f"Q37 = Q38, p = {pz}", abs(h37), abs(h38), tol=1e-9)
    DV = un_a0 ** 2 + L2 / R0 * pz + L2 * C2 * pz ** 2
    H1_, H2_, H3_ = un_a0 / DV, un_a0 / DV, -L2 * pz / DV
    verifier(f"H2 V_DC0 + H3 i_L0 = δV/δα, p = {pz}", abs(H2_ * V0 + H3_ * iL0), abs(h37), tol=1e-9)
    verifier(f"H1 = δV/δE_b = (1/(1 − α0))/(…), p = {pz}", abs(H1_), abs((1 / un_a0) / (1 + Tz * pz + L2 * C2 / un_a0 ** 2 * pz ** 2)), tol=1e-9)
# Réponse inverse : pente initiale négative (théorème de la valeur initiale sur s')
vrai("zéro positif : pente initiale de la réponse indicielle < 0", -Kg * Tz / (L2 * C2 / un_a0 ** 2) < 0)
verifier("Q39 : δV∞ ≈ 11,0 V", 0.01 * Kg, 11.0, tol=0.003)
verifier("Q40 : gain 1/(1 − α0) ≈ 4,79", 1 / un_a0, 4.79, tol=0.001)
verifier("Q39 : 1 % de α0 donnerait ≈ 8,7 V", 0.01 * (1 - un_a0) * Kg, 8.7, tol=0.003)
# Q37 : réduction des deux sommateurs (bobine et condensateur) en p complexes
for pz in (20 + 3j, 150j):
    dV = (un_a0 * V0 - L2 * iL0 * pz) / (un_a0 ** 2 + L2 / R0 * pz + L2 * C2 * pz ** 2)
    di = (V0 - un_a0 * dV) / (L2 * pz)
    vrai(f"Q37 : équation du condensateur vérifiée, p = {pz}", abs(C2 * pz * dV - (un_a0 * di - iL0 - dV / R0)) < 1e-9)
Eb1, Eb2, V1 = 53.3, 42.8, 254.0
verifier("Q41 : δE_b ≈ −10,5 V", Eb2 - Eb1, -10.5)
verifier("Q41 : α ≈ 0,79", 1 - Eb1 / V1, 0.79, tol=0.002)
verifier("Q41 : 1 − α ≈ 0,21", Eb1 / V1, 0.21, tol=0.002)
verifier("Q41 : valeur finale ≈ 204 V", V1 + (Eb2 - Eb1) / (Eb1 / V1), 204, tol=0.002)

print("— Méthode : 2023-E2 et 2015-E1")
KGT = 5.0 / (1000 * 2 * pi / 60)
verifier("1 000 tr/min = 104,7 rad/s", 1000 * 2 * pi / 60, 104.7, tol=0.001)
verifier("K_GT ≈ 0,0477 V·s/rad", KGT, 0.0477, tol=0.002)
verifier("K_M K_GT ≈ 1,0 (K_M ≈ 20,9)", 20.9 * KGT, 1.0, tol=0.005)
verifier("26,4 dB → K_M ≈ 20,9", 10 ** (26.4 / 20), 20.9, tol=0.003)
ph = lambda w: degrees(atan(w / 10) + atan(w / 7000))
lo, hi = 100.0, 1e6
for _ in range(200):
    mid = sqrt(lo * hi)
    lo, hi = (mid, hi) if ph(mid) < 135 else (lo, mid)
G8 = 20 * log10(20.9 * KGT / (sqrt(1 + (lo / 10) ** 2) * sqrt(1 + (lo / 7000) ** 2)))
verifier("D8 : ω_c ≈ 7,0·10³ rad/s", lo, 7.0e3, tol=0.005)
verifier("D8 : gain ≈ −60 dB", G8, -60, tol=0.005)
verifier("D8 : K_PV ≈ 1,0·10³", 10 ** (-G8 / 20), 1.0e3, tol=0.005)
KcAc = 1.6 * 110.74
lam, K1K2 = 142e3, 2 * 100
K0 = K1K2 / KcAc
verifier("K_c A_c ≈ 177 W/°C", KcAc, 177, tol=0.002)
verifier("K0 ≈ 1,13", K0, 1.13, tol=0.002)
verifier("K_c1 ≈ 0,53", K0 / (1 + K0), 0.53, tol=0.003)
verifier("1 + K0 ≈ 2,13", 1 + K0, 2.13, tol=0.002)
verifier("baisse de θi ≈ 8,5 °C", 16 * K0 / (1 + K0), 8.5, tol=0.003)
verifier("θi final ≈ 30,5 °C", 39 - 16 * K0 / (1 + K0), 30.5, tol=0.002)
verifier("erreur ≈ 7,5 °C", 16 / (1 + K0), 7.5, tol=0.004)
tc = lam / (KcAc * (1 + K0))
verifier("τc ≈ 376 s", tc, 376, tol=0.003)
verifier("t5 % ≈ 19 min", 3 * tc / 60, 19, tol=0.02)
# Simulation de la boucle 2015-E1 : λ dθ/dt = P_f − K_cA_c(θ − θe), P_f = K1K2(θc − θi), Kp = 1
th, dt = 39.0, 0.05
for k in range(int(20000 / dt)):
    Pf = K1K2 * (23 - th)
    th += dt * (Pf - KcAc * (th - 39)) / lam
verifier("simulation : θi final ≈ 30,5 °C", th, 30.5, tol=0.002)
verifier("ε_s = θc − θi ≈ −7,5 °C", 23 - (39 - 16 * K0 / (1 + K0)), -7.5, tol=0.004)
verifier("Q14 : K0 ≥ 15 → K_p ≥ 13,3", 15 * KcAc / K1K2, 13.3, tol=0.002)
verifier("Q14 : t5 % ≈ 2,5 min", 3 * lam / (KcAc * 16) / 60, 2.5, tol=0.003)
verifier("Q14 : puissance initiale demandée ≈ 43 kW", K1K2 * (15 * KcAc / K1K2) * 16 / 1000, 42.5, tol=0.02)
vrai("… au-delà des 7,9 kW de l'ASI24B : saturation", K1K2 * 13.3 * 16 > 7900)

print("— Méthode : 2017-E1 (notre lecture de son DR2)")
verifier("bande à ±5 % de 35 − 28 °C : ±0,35 °C", 0.05 * 7, 0.35)
verifier("t5 % ≈ 150 s = 2,5 min", 150 / 60, 2.5)

print("— Méthode : 2021-E1")
verifier("K ≈ 600/10 = 60 kN·m/V", 600 / 10, 60)
verifier("63 % de la variation : ≈ 980 kN·m", 600 + 0.632 * 600, 980, tol=0.003)
verifier("modèle absolu sous 30 V : 1 800 kN·m", 60 * 30, 1800)

print("— Auto-test")
verifier("Q1 : 10 V", 5 * 2, 10)
verifier("Q1 : pente 50 V/s", 10 / 0.2, 50)
verifier("Q1 : s(τ) ≈ 6,32 V", 10 * (1 - exp(-1)), 6.32, tol=0.001)
pz = 0.7 + 0.4j
verifier("Q2 : décomposition 2/p − 3/(p+1) + 1/(p+3)", abs(2 / pz - 3 / (pz + 1) + 1 / (pz + 3)), abs(6 / (pz * (pz + 1) * (pz + 3))), tol=1e-12)
verifier("Q2 : valeur finale 2", 6 / 3, 2)
D3 = D(0.2)
verifier("Q3 : D ≈ 52,7 %", 100 * D3, 52.7, tol=0.002)
verifier("Q3 : maximum ≈ 6,11", 4 * (1 + D3), 6.11, tol=0.002)
verifier("Q3 : t_p ≈ 0,32 s", pi / (10 * sqrt(0.96)), 0.32, tol=0.005)
verifier("Q3 : ω0·t5 % ≈ 13,7", t5_reduit(0.2), 13.7, tol=0.005)
verifier("Q4 : gain 0,909", 10 / 11, 0.909, tol=0.001)
verifier("Q4 : τ ≈ 0,182 s", 2 / 11, 0.182, tol=0.002)
verifier("Q4 : écart 0,091", 1 / 11, 0.091, tol=0.002)
verifier("Q5 : τm = 0,4 s", 2 * 2e-3 / 0.01, 0.4)
verifier("Q5 : m ≈ 4,5", 0.5 * sqrt(0.4 / 0.005), 4.5, tol=0.01)
verifier("Q5 : 4 584 tr/min", 480 * 60 / (2 * pi), 4584, tol=0.001)
verifier("Q5 : 10,5 V par millier de tr/min", 0.1 * 1000 * 2 * pi / 60, 10.5, tol=0.003)
Rr, Lr, Cc = 10.0, 0.1, 1e-4
Ar = np.array([[-Rr / Lr, -1 / Lr], [1 / Cc, 0]]); Br = np.array([[1 / Lr], [0]]); Cr_ = np.array([[0, 1]])
for pz in (5 + 30j, 400j):
    Hs = (Cr_ @ np.linalg.inv(pz * np.eye(2) - Ar) @ Br)[0, 0]
    verifier(f"Q6 : C(pI − A)⁻¹B = 1/(1 + RCp + LCp²), p = {pz}", abs(Hs), abs(1 / (1 + Rr * Cc * pz + Lr * Cc * pz ** 2)), tol=1e-9)

print()
print("Aucun écart." if not ECARTS else f"{len(ECARTS)} écart(s) : " + " ; ".join(ECARTS))
raise SystemExit(1 if ECARTS else 0)
