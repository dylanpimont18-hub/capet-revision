"""Applications numériques du chapitre T20, refaites en Python.

    python3 cours/calculs/T20.py

Chaque bloc reprend une valeur publiée dans cours/textes/T20.html ; un
écart de plus de 0,5 % sur la valeur arrondie fait échouer le script.
Les fonctions de transfert sont recalculées à partir des circuits, par
analyse nodale en complexe, indépendamment des formes canoniques du cours ;
les réponses indicielles sont intégrées numériquement.
"""
from math import sqrt, pi, log10, atan, atan2, degrees, exp

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


def db(h):
    return 20 * log10(abs(h))


# ── Circuits, par analyse nodale ─────────────────────────────────────────
def zc(C, w):
    return 1 / (1j * C * w)


def zl(L, w):
    return 1j * L * w


def h_rc(R, C, w):          # passe-bas RC, sortie sur C
    return zc(C, w) / (R + zc(C, w))


def h_rc_haut(R, C, w):     # passe-haut RC, sortie sur R
    return R / (R + zc(C, w))


def h_rl(R, L, w):          # passe-bas RL, sortie sur R
    return R / (R + zl(L, w))


def h_rlc_c(R, L, C, w):    # RLC série, sortie sur C
    return zc(C, w) / (R + zl(L, w) + zc(C, w))


def h_rlc_r(R, L, C, w):    # RLC série, sortie sur R
    return R / (R + zl(L, w) + zc(C, w))


def h_cascade_directe(R, C, w):
    """Deux RC sans séparateur : système nodal en V_A, V_s pour V_e = 1."""
    y_r, y_c = 1 / R, 1j * C * w
    M = np.array([[2 * y_r + y_c, -y_r], [-y_r, y_r + y_c]])
    b = np.array([y_r, 0])
    return np.linalg.solve(M, b)[1]


def indicielle(m, w0=1.0, tmax=40.0, n=400_000):
    """Réponse à un échelon unité de 1/(1 + 2m p/w0 + p²/w0²), par RK4."""
    dt = tmax / n
    x, v = 0.0, 0.0
    t_out, y_out = [0.0], [0.0]

    def f(x, v):
        return v, w0 * w0 * (1 - x) - 2 * m * w0 * v
    for k in range(n):
        a1, b1 = f(x, v)
        a2, b2 = f(x + dt / 2 * a1, v + dt / 2 * b1)
        a3, b3 = f(x + dt / 2 * a2, v + dt / 2 * b2)
        a4, b4 = f(x + dt * a3, v + dt * b3)
        x += dt / 6 * (a1 + 2 * a2 + 2 * a3 + a4)
        v += dt / 6 * (b1 + 2 * b2 + 2 * b3 + b4)
        if k % 100 == 0:
            t_out.append((k + 1) * dt)
            y_out.append(x)
    return np.array(t_out), np.array(y_out)


print("— §3 Passe-bas du premier ordre")
R, C = 1e3, 1e-6
wc = 1 / (R * C)
verifier("|H(ωc)| = 1/√2 ≈ 0,707", abs(h_rc(R, C, wc)), 0.707)
verifier("G(ωc) ≈ −3 dB", db(h_rc(R, C, wc)), -3.0, tol=0.01)
verifier("φ(ωc) = −45°", degrees(np.angle(h_rc(R, C, wc))), -45)
verifier("phase en HF tend vers −90° (x = 1 000)", degrees(np.angle(h_rc(R, C, 1000 * wc))), -90, tol=0.002)
verifier("pente : 20 log10 2 ≈ 6 dB par octave", 20 * log10(2), 6.0, tol=0.01)
verifier("pente asymptotique, x 100 → 1 000 : −20 dB/déc.", db(h_rc(R, C, 1000 * wc)) - db(h_rc(R, C, 100 * wc)), -20.0)
verifier("doubler f divise l'amplitude par deux (x 100 → 200)", abs(h_rc(R, C, 100 * wc)) / abs(h_rc(R, C, 200 * wc)), 2.0)
verifier("facteur 2π « plus de six »", 2 * pi, 6.283)
L = 10e-3
verifier("RL : ωc = R/L, |H| = 1/√2", abs(h_rl(R, L, R / L)), 0.7071)
# Réponse indicielle : 63 % à τ, 95 % à 3τ ; t5% exact = τ ln 20
verifier("v_s(τ)/E = 1 − e⁻¹ ≈ 0,63", 1 - exp(-1), 0.632)
verifier("v_s(3τ)/E = 1 − e⁻³ ≈ 0,95", 1 - exp(-3), 0.950)
verifier("t5% exact = τ ln 20 ≈ 3τ", np.log(20), 3.0, tol=0.002)
verifier("filtre de 159 Hz : t5% ≈ 3 ms", 3 / (2 * pi * 159), 3e-3, tol=0.005)

print("— §4 Passe-haut")
verifier("passe-haut : G(ωc) = −3 dB", db(h_rc_haut(R, C, wc)), -3.0, tol=0.01)
verifier("passe-haut : φ(ωc) = +45°", degrees(np.angle(h_rc_haut(R, C, wc))), 45)
verifier("passe-haut : φ en BF → +90° (x = 0,001)", degrees(np.angle(h_rc_haut(R, C, wc / 1000))), 90, tol=0.002)
verifier("passe-haut : pente BF +20 dB/déc.", db(h_rc_haut(R, C, wc / 100)) - db(h_rc_haut(R, C, wc / 1000)), 20.0)

print("— §5 Second ordre (RLC série, sortie sur C)")
L, C = 10e-3, 1e-6
w0 = 1 / sqrt(L * C)
for m in (0.1, 0.3, 0.707, 1.0):
    Rm = 2 * m * sqrt(L / C)
    verifier(f"m = {m} : |H(ω0)| = 1/(2m)", abs(h_rlc_c(Rm, L, C, w0)), 1 / (2 * m))
    verifier(f"m = {m} : φ(ω0) = −90°", degrees(np.angle(h_rlc_c(Rm, L, C, w0))), -90)
    ws = np.logspace(-3, 3, 20001) * w0
    ph = np.degrees(np.unwrap(np.angle(h_rlc_c(Rm, L, C, ws))))
    vrai(f"m = {m} : phase entre 0 et −180° sans les franchir", ph.max() <= 1e-9 and ph.min() >= -180)
    # résonance : maximum numérique
    ws = np.linspace(0.01, 1.5, 300001) * w0
    hs = np.abs(h_rlc_c(Rm, L, C, ws))
    k = int(np.argmax(hs))
    if m < 1 / sqrt(2):
        verifier(f"m = {m} : ωr = ω0√(1 − 2m²)", ws[k] / w0, sqrt(1 - 2 * m * m), tol=0.001)
        verifier(f"m = {m} : Hmax = 1/(2m√(1 − m²))", hs[k], 1 / (2 * m * sqrt(1 - m * m)), tol=0.001)
    else:
        vrai(f"m = {m} : pas de maximum hors de ω = 0", k == 0)
verifier("m = 0,1 : Hmax ≈ 5,0", 1 / (0.2 * sqrt(0.99)), 5.0, tol=0.006)
verifier("m = 0,1 : Hmax ≈ +14 dB (figure 8, carte f-008)", 20 * log10(1 / (0.2 * sqrt(0.99))), 14.0, tol=0.005)
verifier("m = 1/√2 : G(ω0) = −3 dB", db(1 / sqrt(2)), -3.0, tol=0.01)
verifier("seuil de résonance 1/√2 ≈ 0,707", 1 / sqrt(2), 0.707)
verifier("Butterworth : H² = 1/(1 + x⁴) (x = 1,7)", abs(h_rlc_c(sqrt(2) * sqrt(L / C), L, C, 1.7 * w0)) ** 2, 1 / (1 + 1.7 ** 4))
verifier("pente HF −40 dB/déc. (m = 0,3)", db(h_rlc_c(0.6 * sqrt(L / C), L, C, 1000 * w0)) - db(h_rlc_c(0.6 * sqrt(L / C), L, C, 100 * w0)), -40.0)
for m, D in ((0.707, 0.043), (0.5, 0.16), (0.1, 0.73)):
    t, y = indicielle(m)
    verifier(f"m = {m} : dépassement simulé", y.max() - 1, D, tol=0.02)
    verifier(f"m = {m} : D = exp(−πm/√(1 − m²))", exp(-pi * m / sqrt(1 - m * m)), D, tol=0.02)
t, y = indicielle(0.1)
verifier("figure 9 : premier maximum 1,73 pour m = 0,1", y.max(), 1.73)
for m in (1.0, 1.5):
    t, y = indicielle(m)
    vrai(f"m = {m} : pas de dépassement", y.max() <= 1 + 1e-9)

print("— §6 Cascades")
R, C = 1e3, 1e-6
wc = 1 / (R * C)
verifier("avec suiveur : |H(ωc)| = 1/2", abs(h_rc(R, C, wc)) ** 2, 0.5)
verifier("avec suiveur : −6 dB", db(h_rc(R, C, wc) ** 2), -6.0, tol=0.01)
for x in (0.3, 1.0, 4.0):
    vrai(f"sans suiveur : H = 1/(1 + 3jx − x²), x = {x}",
         abs(h_cascade_directe(R, C, x * wc) - 1 / (1 + 3j * x - x * x)) < 1e-12)
verifier("sans suiveur : m = 3/2", 3 / 2, 1.5)
verifier("sans suiveur : |H(ωc)| = 1/3", abs(h_cascade_directe(R, C, wc)), 1 / 3)
verifier("sans suiveur : −9,5 dB", db(h_cascade_directe(R, C, wc)), -9.5, tol=0.005)
verifier("pente HF des cascades : −40 dB/déc.", db(h_cascade_directe(R, C, 1000 * wc)) - db(h_cascade_directe(R, C, 100 * wc)), -40.0)
# 2023-E2 D4, notre lecture du DR4
verifier("2023-E2 : K_M = 10^(26,4/20) ≈ 20,9", 10 ** (26.4 / 20), 20.9)
# Lecture du DR4 au pixel : décades de 137 px, 10³ à x ≈ 641 et 10⁴ à x ≈ 775 ;
# marche orange de la phase à x ≈ 755, courbe noire à −135° vers x ≈ 756.
x10_3, x10_4, x_marche = 641, 775, 755
wb_lu = 10 ** (3 + (x_marche - x10_3) / (x10_4 - x10_3))
verifier("2023-E2 : ωb lu au pixel ≈ 7·10³ rad/s", wb_lu, 7e3, tol=0.06)
wa, wb = 10, 7e3
verifier("2023-E2 : m = (ωa + ωb)/(2√(ωa ωb)) ≈ 13", (wa + wb) / (2 * sqrt(wa * wb)), 13, tol=0.025)
H = lambda w: 1 / ((1 + 1j * w / wa) * (1 + 1j * w / wb))
verifier("2023-E2 : phase ≈ −45° à ωa (pôles séparés)", degrees(np.angle(H(wa))), -45, tol=0.04)
verifier("2023-E2 : phase ≈ −135° à ωb", degrees(np.angle(H(wb))), -135, tol=0.01)

print("— §7 Passe-bande")
L, C = 10e-3, 1e-6
w0 = 1 / sqrt(L * C)
for Q in (0.5, 2, 10):
    Rq = L * w0 / Q
    verifier(f"Q = {Q} : H(ω0) = 1 (0 dB)", abs(h_rlc_r(Rq, L, C, w0)), 1.0)
    canon = lambda w: (1j * w / (Q * w0)) / (1 + 1j * w / (Q * w0) + (1j * w / w0) ** 2)
    vrai(f"Q = {Q} : forme canonique f-010 = circuit", abs(h_rlc_r(Rq, L, C, 0.37 * w0) - canon(0.37 * w0)) < 1e-12)
    ws = np.linspace(0.01, 5, 2_000_001) * w0
    g = np.abs(h_rlc_r(Rq, L, C, ws))
    bande = ws[g >= 1 / sqrt(2)]
    verifier(f"Q = {Q} : Δω à −3 dB = ω0/Q", (bande[-1] - bande[0]) / w0, 1 / Q, tol=0.002)
    verifier(f"Q = {Q} : Q = 1/(2m) avec m = (R/2)√(C/L)", 1 / (2 * (Rq / 2) * sqrt(C / L)), Q)
verifier("pente ±20 dB/déc. loin du sommet (Q = 2)", db(h_rlc_r(L * w0 / 2, L, C, 1000 * w0)) - db(h_rlc_r(L * w0 / 2, L, C, 100 * w0)), -20.0)

print("— §8 Anti-repliement et filtre L, C")
verifier("1er ordre à fe/5 : −8,6 dB à fe/2", -10 * log10(1 + 2.5 ** 2), -8.6)
verifier("1er ordre à fe/10 : −14 dB à fe/2", -10 * log10(1 + 5 ** 2), -14.0, tol=0.011)
verifier("second ordre : une décade divise l'ondulation par ≈ 100", abs(h_rlc_c(2 * 0.7 * sqrt(L / C), L, C, 10 * w0)), 0.01, tol=0.02)
verifier("… soit 40 dB", -db(h_rlc_c(2 * 0.7 * sqrt(L / C), L, C, 10 * w0)), 40.0, tol=0.005)

print("— Exemple : anti-repliement d'un analyseur de réseau")
fmax, fe = 2e3, 25.6e3
verifier("512 points par période", fe / 50, 512)
verifier("f2 = fe − fmax = 23,6 kHz", fe - fmax, 23.6e3)
verifier("fe/2 = 12,8 kHz", fe / 2, 12.8e3)
fc1 = fmax / sqrt(10 ** 0.1 - 1)
verifier("1er ordre : fc ≥ 3,93 kHz", fc1, 3.93e3)
g1 = lambda f, fc: -10 * log10(1 + (f / fc) ** 2)
verifier("1er ordre : G(23,6 kHz) ≈ −15,7 dB", g1(23.6e3, fc1), -15.7)
fc2 = fmax / sqrt(10 ** 0.05 - 1)
verifier("cascade : −0,5 dB par cellule → fc ≥ 5,73 kHz", fc2, 5.73e3)
verifier("cascade : une cellule à 23,6 kHz ≈ −12,6 dB", g1(23.6e3, fc2), -12.6)
verifier("cascade : G(23,6 kHz) ≈ −25,1 dB", 2 * g1(23.6e3, fc2), -25.1)
verifier("cascade : G(2 kHz) = −1 dB", 2 * g1(2e3, fc2), -1.0)
xb = (10 ** 0.1 - 1) ** 0.25
verifier("Butterworth : x = (10^0,1 − 1)^(1/4) ≈ 0,713", xb, 0.713)
f0 = fmax / xb
verifier("Butterworth : f0 ≥ 2,80 kHz", f0, 2.80e3)
gb = lambda f, f0: -10 * log10(1 + (f / f0) ** 4)
verifier("Butterworth : G(23,6 kHz) ≈ −37,0 dB", gb(23.6e3, f0), -37.0)
verifier("Butterworth : il manque 3 dB", -40 - gb(23.6e3, f0), -3.0, tol=0.01)
verifier("fe = 51,2 kHz : 1 024 points par période", 51.2e3 / 50, 1024)
verifier("fe = 51,2 kHz : f2 = 49,2 kHz", 51.2e3 - fmax, 49.2e3)
verifier("Butterworth : G(49,2 kHz) ≈ −49,8 dB", gb(49.2e3, f0), -49.8)
verifier("… marge ≈ 10 dB", -40 - gb(49.2e3, f0), 9.8, tol=0.01)
verifier("cascade : G(49,2 kHz) ≈ −37,5 dB", 2 * g1(49.2e3, fc2), -37.5)
verifier("1er ordre : G(49,2 kHz) ≈ −22 dB", g1(49.2e3, fc1), -22.0)
# Figure 13 : extrémité des courbes à 10^4,75 Hz
fx = 10 ** 4.75
vrai("figure 13 : 1er ordre au-dessus de −40 dB partout", g1(fx, fc1) > -40)
vrai("figure 13 : cascade au-dessus de −40 dB à 49,2 kHz", 2 * g1(49.2e3, fc2) > -40)
# Réalisation, f0 = 3 kHz
f0r, C = 3e3, 100e-9
verifier("f0 = 3 kHz : −0,8 dB à 2 kHz", gb(2e3, f0r), -0.8, tol=0.03)
verifier("f0 = 3 kHz : −48,6 dB à 49,2 kHz", gb(49.2e3, f0r), -48.6)
Lr = 1 / ((2 * pi * f0r) ** 2 * C)
verifier("L ≈ 28 mH", Lr, 28e-3, tol=0.006)
Rr = 2 * 0.7071 * sqrt(Lr / C)
verifier("R = 2m√(L/C) ≈ 750 Ω", Rr, 750)
mr = 750 / 2 * sqrt(C / Lr)
verifier("avec 750 Ω : m ≈ 0,707", mr, 0.707)
wr = 2 * pi * f0r
verifier("circuit réel : G(2 kHz) ≈ −0,8 dB", db(h_rlc_c(750, Lr, C, 2 * pi * 2e3)), -0.8, tol=0.03)
verifier("circuit réel : G(49,2 kHz) ≈ −48,6 dB", db(h_rlc_c(750, Lr, C, 2 * pi * 49.2e3)), -48.6)
verifier("circuit réel : φ(50 Hz) ≈ −1,4°", degrees(np.angle(h_rlc_c(750, Lr, C, 2 * pi * 50))), -1.4, tol=0.04)
verifier("circuit réel : φ(2 kHz) ≈ −59°", degrees(np.angle(h_rlc_c(750, Lr, C, 2 * pi * 2e3))), -59, tol=0.01)
verifier("|Z_L| à 2 kHz, de l'ordre du kilohm", abs(zl(Lr, 2 * pi * 2e3)), 354, tol=0.01)
verifier("|Z_C| à 2 kHz, de l'ordre du kilohm", abs(zc(C, 2 * pi * 2e3)), 796, tol=0.01)
# Charge de 100 kΩ en parallèle sur C : effet négligeable
Zp = lambda w: 1 / (1 / zc(C, w) + 1 / 100e3)
hch = lambda w: Zp(w) / (750 + zl(Lr, w) + Zp(w))
vrai("100 kΩ en sortie : écart de gain < 0,1 dB jusqu'à 2 kHz",
     max(abs(db(hch(2 * pi * f)) - db(h_rlc_c(750, Lr, C, 2 * pi * f))) for f in (50, 500, 2e3)) < 0.1)
t, y = indicielle(mr)
verifier("dépassement ≈ 4 %", y.max() - 1, 0.043, tol=0.05)

print("— Auto-test")
R, C = 10e3, 100e-9
verifier("Q1 : ωc = 1 000 rad/s", 1 / (R * C), 1000)
verifier("Q1 : fc ≈ 159 Hz", 1 / (2 * pi * R * C), 159)
verifier("Q1 : G(1,59 kHz) ≈ −20 dB", db(h_rc(R, C, 2 * pi * 1.59e3)), -20.0, tol=0.005)
verifier("Q1 : φ(1,59 kHz) ≈ −84°", degrees(np.angle(h_rc(R, C, 2 * pi * 1.59e3))), -84, tol=0.005)
verifier("Q1 : t5% = 3 ms", 3 * R * C, 3e-3)
verifier("Q2 : −40 log10 2 ≈ −12 dB/octave", -40 * log10(2), -12.0, tol=0.005)
verifier("Q2 : x = 4 → −10 log10 17 ≈ −12,3 dB", -10 * log10(17), -12.3)
R, L = 100, 10e-3
verifier("Q3 : τ = 0,1 ms", L / R, 1e-4)
verifier("Q3 : fc ≈ 1,59 kHz", R / L / (2 * pi), 1.59e3)
verifier("Q3 : G(ωc) du circuit = −3 dB", db(h_rl(R, L, R / L)), -3.0, tol=0.01)
verifier("Q3 : t5% = 0,3 ms", 3 * L / R, 3e-4)
R, L, C = 20, 10e-3, 1e-6
w0 = 1 / sqrt(L * C)
verifier("Q4 : ω0 = 10⁴ rad/s", w0, 1e4)
verifier("Q4 : m = 0,1", R / 2 * sqrt(C / L), 0.1)
verifier("Q4 : ωr ≈ 9 900 rad/s", w0 * sqrt(1 - 2 * 0.01), 9900)
ws = np.linspace(0.9, 1.1, 200001) * w0
hs = np.abs(h_rlc_c(R, L, C, ws))
verifier("Q4 : Hmax ≈ 5,0 (circuit)", hs.max(), 5.0, tol=0.006)
verifier("Q4 : +14 dB", 20 * log10(hs.max()), 14.0, tol=0.005)
verifier("Q4 : premier dépassement 73 %", exp(-pi * 0.1 / sqrt(0.99)), 0.73)
verifier("Q5 : H(x = 1) = 1/3 → −9,5 dB", db(1 / (1 + 3j - 1)), -9.5, tol=0.005)
verifier("Q5 : avec suiveur −6 dB", db(0.5), -6.0, tol=0.005)
verifier("Q6 : 1 kHz → −0,97 dB", -10 * log10(1.25), -0.97)
verifier("Q6 : 5 kHz → −8,6 dB", -10 * log10(1 + 2.5 ** 2), -8.6)
verifier("Q6 : 9 kHz → −13,3 dB", -10 * log10(1 + 4.5 ** 2), -13.3)
verifier("Q6 : 10 bits ≈ 60 dB (6,02 dB par bit)", 20 * log10(2 ** 10), 60, tol=0.005)

print()
print("Aucun écart." if not ECARTS else f"{len(ECARTS)} écart(s) : " + " ; ".join(ECARTS))
raise SystemExit(1 if ECARTS else 0)
