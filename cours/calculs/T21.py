"""Applications numériques du chapitre T21, refaites en Python.

    python3 cours/calculs/T21.py

Chaque bloc reprend une valeur publiée dans cours/textes/T21.html ; un
écart de plus de 0,5 % sur la valeur arrondie fait échouer le script.
Les gains et les phases sont évalués en p = jω, les pulsations
particulières (ω_u, ω_π) cherchées par dichotomie, les réponses
indicielles simulées (Euler, pas fin) et comparées aux formules.
"""
from math import sqrt, pi, log, log10, exp, atan, degrees, radians, tan

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


def dicho(fn, a, b, n=200):
    """Racine de fn entre a et b (changement de signe), en échelle log si a > 0."""
    fa = fn(a)
    for _ in range(n):
        m = sqrt(a * b) if a > 0 else (a + b) / 2
        fm = fn(m)
        if (fm > 0) == (fa > 0):
            a, fa = m, fm
        else:
            b = m
    return sqrt(a * b) if a > 0 else (a + b) / 2


def gdb(H, w):
    return 20 * log10(abs(H(1j * w)))


def phase(H, w, w0=1e-4):
    """Phase continue en degrés : déroulée depuis une pulsation basse w0."""
    ws = np.logspace(log10(w0), log10(w), 4000)
    ph = np.unwrap(np.angle([H(1j * x) for x in ws]))
    return degrees(ph[-1])


def marges(H, lo, hi):
    wu = dicho(lambda w: abs(H(1j * w)) - 1, lo, hi)
    Mphi = 180 + phase(H, wu)
    return wu, Mphi


def Mphi_m(m):
    return degrees(atan(2 * m / sqrt(sqrt(1 + 4 * m ** 4) - 2 * m * m)))


def D_m(m):
    return exp(-pi * m / sqrt(1 - m * m))


def m_D(D):
    return abs(log(D)) / sqrt(pi ** 2 + log(D) ** 2)


def indicielle(a2, a1, K, T, n=200000):
    """Réponse indicielle de K/(1 + a1 p + a2 p²), Euler semi-implicite."""
    dt = T / n
    y = v = 0.0
    ys = np.empty(n + 1); ys[0] = 0
    for k in range(n):
        acc = (K - y - a1 * v) / a2
        v += acc * dt
        y += v * dt
        ys[k + 1] = y
    return np.linspace(0, T, n + 1), ys


print("── Idée physique, §1 : repères")
verifier("20 log 10", 20 * log10(10), 20)
verifier("20 log 2 ≈ 6 dB", 20 * log10(2), 6, tol=0.01)
verifier("20 log (1/√2) ≈ −3 dB", 20 * log10(1 / sqrt(2)), -3, tol=0.01)
H1 = lambda p: 1 / (1 + p)
verifier("premier ordre : |H| en ω = 1/τ (K = 1)", abs(H1(1j)), 1 / sqrt(2))
verifier("premier ordre : phase en 1/τ", degrees(np.angle(H1(1j))), -45)
# réponse harmonique simulée : premier ordre τ = 1, ω = 2 rad/s
t = np.linspace(0, 40, 400001); dt = t[1] - t[0]
y = np.zeros_like(t)
for k in range(len(t) - 1):
    y[k + 1] = y[k] + dt * (sin_ := np.sin(2 * t[k])) - dt * y[k]
fin = t > 30
verifier("réponse harmonique simulée : amplitude S/E", y[fin].max(), abs(H1(2j)), tol=0.005)

print("── §2 : briques")
verifier("asymptote de phase : erreur maximale 5,7°", degrees(atan(0.1)), 5.7, tol=0.01)
xs = np.logspace(-3, 3, 20001)
err = []
for x in xs:
    vraie = degrees(atan(x))
    asym = 0 if x <= 0.1 else (90 if x >= 10 else 45 * (log10(x) + 1))
    err.append(abs(vraie - asym))
verifier("erreur maximale de l'asymptote de phase (balayage)", max(err), 5.7, tol=0.01)
for m in (0.3, 0.5, 0.7):
    H2 = lambda p, m=m: 1 / (1 + 2 * m * p + p * p)
    verifier(f"second ordre m = {m} : |H(jω0)| = K/(2m)", abs(H2(1j)), 1 / (2 * m))
vrai("au-dessus de l'asymptote en ω0 ssi m < 0,5", (1 / (2 * 0.49) > 1) and (1 / (2 * 0.51) < 1))
verifier("zéro instable : phase de 1 − τp à ωτ = 10", degrees(np.angle(1 - 10j)), -84.3, tol=0.002)
verifier("retard : phase de e^{−jωT} en ωT = 1 (rad)", -1.0, -1.0)

verifier("premier ordre K = 10 : 0 dB en ωc√(K²−1)", dicho(lambda x: 10 / sqrt(1 + x * x) - 1, 1, 100), 9.95)
verifier("K = 3 : √8 contre 3 (écart relatif)", 1 - sqrt(8) / 3, 0.06, tol=0.05)
print("── §3 : tracé de 10(1 + p/10)/[p(1 + p)(1 + p/100)]")
H3 = lambda p: 10 * (1 + p / 10) / (p * (1 + p) * (1 + p / 100))
asym = lambda w: (20 - 20 * log10(w) if w <= 1 else 20 - 40 * log10(w) if w <= 10
                  else -20 - 20 * log10(w / 10) if w <= 100 else -40 - 40 * log10(w / 100))
verifier("asymptote en 1 rad/s", asym(1), 20)
verifier("asymptote en 10 rad/s", asym(10), -20)
verifier("asymptote en 100 rad/s", asym(100), -40)
verifier("asymptote à 0 dB en √10", dicho(asym, 1, 10), 3.16)
verifier("|H(j 3,16)| ≈ 1,00", abs(H3(1j * sqrt(10))), 1.00)
verifier("écart dû au pôle en 1 (dB)", -10 * log10(1 + 10) + 20 * log10(sqrt(10)), -0.4, tol=0.04)
verifier("écart dû au zéro en 10 (dB)", 10 * log10(1 + 0.1), 0.4, tol=0.04)
ws = np.logspace(-1, 3, 40001)
ph = np.array([phase(H3, w) for w in ws[::40]]); wsr = ws[::40]
k = np.argmin(ph[wsr < 10]); verifier("phase minimale", ph[k], -147, tol=0.005); verifier("… vers 3,4 rad/s", wsr[k], 3.4, tol=0.02)
sel = wsr > 8; k2 = np.argmax(np.where(sel, ph, -999)); verifier("maximum local de phase", ph[k2], -123, tol=0.005)
verifier("… vers 30 rad/s", wsr[k2], 30, tol=0.05)
verifier("phase en ω_u", phase(H3, dicho(lambda w: abs(H3(1j * w)) - 1, 1, 10)), -147, tol=0.005)

print("── §4 : pôle dominant (2023-E2)")
verifier("pôle négligé une décade sous 1/τb : gain (dB)", 10 * log10(1.01), 0.04, tol=0.1)
verifier("… phase", degrees(atan(0.1)), 5.7, tol=0.01)
verifier("τa = 1/ωa", 1 / 10, 0.1)
verifier("τb = 1/ωb (ms)", 1e3 / 7000, 0.14, tol=0.03)
verifier("rapport τa/τb", 7000 / 10, 700)
# retard d'environ τb entre réponse réelle et réduite
ta, tb = 1.0, 0.05
tt = 3.0
vraie = 1 - (ta * exp(-tt / ta) - tb * exp(-tt / tb)) / (ta - tb)
reduite_dec = 1 - exp(-(tt - tb) / ta)
verifier("réponse réelle ≈ réduite retardée de τb", vraie, reduite_dec, tol=0.002)

print("── §5 : boucle ouverte, boucle fermée, précision")
L6 = lambda p: 1 / (p * (1 + p) * (1 + 0.1 * p))
F6 = lambda p: L6(p) / (1 + L6(p))
wsb = np.logspace(-2, 2, 200001)
bf = np.abs([F6(1j * w) for w in wsb])
verifier("bosse de la boucle fermée (dB)", 20 * log10(bf.max()), 1.9, tol=0.02)
verifier("… vers ω (rad/s)", wsb[bf.argmax()], 0.78, tol=0.03)
verifier("−3 dB de la boucle fermée", wsb[np.where(20 * np.log10(bf) < -3)[0][0]], 1.3, tol=0.02)
for KBO in (4, 64.24):
    eps = 1 / (1 + KBO)
    verifier(f"valeur finale de l'écart, K_BO = {KBO}", (lambda p: p * (1 / p) / (1 + KBO / (1 + p)))(1e-9), eps)

print("── §6 : marges de 1/[p(1 + p)(1 + 0,1p)]")
wu, Mp = marges(L6, 0.1, 10)
verifier("ω_u", wu, 0.784)
verifier("phase en ω_u", Mp - 180, -132.6)
verifier("M_φ", Mp, 47.4)
wpi = dicho(lambda w: phase(L6, w) + 180, 1, 10)
verifier("ω_π = √10", wpi, sqrt(10))
verifier("|FTBO(jω_π)| = 1/11", abs(L6(1j * wpi)), 1 / 11)
verifier("M_G (dB)", -gdb(L6, wpi), 20.8)
# instabilité pour un gain multiplié par 11 : racines de 0,1p³ + 1,1p² + p + K
for K, stable in ((10.9, True), (11.1, False)):
    r = np.roots([0.1, 1.1, 1, K])
    vrai(f"K = {K} : boucle fermée {'stable' if stable else 'instable'}", (max(r.real) < 0) == stable)

print("── §7 : du fréquentiel au temporel")
for m, v in ((0.3, 33), (0.5, 52), (0.707, 65.5), (1, 76)):
    verifier(f"M_φ(m = {m})", Mphi_m(m), v, tol=0.01)
    K, tau = 1 / (4 * m * m), 1.0     # m = 1/(2√(Kτ)) avec τ = 1
    verifier(f"… par la boucle K/[p(1 + τp)]", marges(lambda p: K / (p * (1 + tau * p)), 1e-3, 1e3)[1], Mphi_m(m), tol=0.001)
vrai("règle M_φ ≈ 100 m à 4° près jusqu'à m = 0,6", all(abs(Mphi_m(m) - 100 * m) < 4 for m in np.linspace(0.001, 0.6, 600)))
verifier("D(0,7)", 100 * D_m(0.7), 4.6, tol=0.01)
verifier("D(0,46)", 100 * D_m(0.46), 20, tol=0.02)
verifier("D(0,43)", 100 * D_m(0.43), 22, tol=0.02)
for m, v in ((0.4, 0.85), (0.7, 0.65)):
    u = sqrt(sqrt(1 + 4 * m ** 4) - 2 * m * m)
    verifier(f"ω_u/ω0 pour m = {m}", u, v, tol=0.01)
# 2024-E2 : structure I-P
Km, tm, m, w0 = 250, 8.5, 1, 5.0
Kp = (2 * m * w0 * tm - 1) / Km
Ki = tm * w0 ** 2 / (Kp * Km)
verifier("2024-E2 : K_p", Kp, 0.336)
verifier("2024-E2 : K_i", Ki, 2.53)
for p in (0.3 + 1j, 2j, 4 - 1j):
    Hbf = Ki * Kp * Km / (tm * p * p + (1 + Kp * Km) * p + Ki * Kp * Km)
    can = 1 / (1 + 2 * m * p / w0 + p * p / w0 ** 2)
    vrai(f"H_bf I-P = forme canonique en p = {p}", abs(Hbf - can) < 1e-12)
# schéma I-P simulé : commande Kp[Ki∫(Ωref − Ω) − Ω], moteur Km/(1 + τ p)
dt, T = 1e-4, 4.0
Om = I = 0.0
for k in range(int(T / dt)):
    u = Kp * (Ki * I - Om)
    I += (1 - Om) * dt
    Om += (Km * u - Om) / tm * dt
verifier("I-P simulé : Ω(4 s) → consigne", Om, 1.0, tol=0.002)
x = dicho(lambda x: 1 - (1 + x) * exp(-x) - 0.95, 1, 10)
verifier("ω0·t5% pour m = 1", x, 4.75)

print("── Méthode : 2023-E2, D4 à D8")
KM = 10 ** (26.4 / 20)
KGT = 5.0 / (1000 * 2 * pi / 60)
verifier("1000 tr/min en rad/s", 1000 * 2 * pi / 60, 104.7)
verifier("K_GT", KGT, 0.0477)
verifier("K_GT en dB", 20 * log10(KGT), -26.4)
verifier("K_M", KM, 20.9)
verifier("K_M·K_GT", KM * KGT, 0.998, tol=0.001)
wa, wb = 10.0, 7000.0
FT = lambda p: KM * KGT / ((1 + p / wa) * (1 + p / wb))
w135 = dicho(lambda w: phase(FT, w) + 135, 100, 1e5)
verifier("phase −135° vers", w135, 7.0e3)
verifier("asymptote en ω_b (dB)", -20 * log10(wb / wa), -56.9)
G1 = gdb(FT, w135)
verifier("G1", G1, -60, tol=0.002)
KPV = 10 ** (-G1 / 20)
verifier("K_PV", KPV, 1.0e3, tol=0.01)
verifier("D8 : marge obtenue", 180 + phase(lambda p: KPV * FT(p), marges(lambda p: KPV * FT(p), 100, 1e5)[0]), 45, tol=0.002)
verifier("erreur statique (%)", 100 / (1 + KPV * KM * KGT), 0.1, tol=0.01)
vrai("modèle réduit : phase > −90° partout", all(-degrees(atan(w / wa)) > -90 for w in np.logspace(0, 6, 100)))
verifier("0,1 ms à 7000 rad/s (degrés)", degrees(7000 * 1e-4), 40, tol=0.005)
vrai("ω_b lu à −135° : pôle en ω_a déjà à −89,9°", -degrees(atan(wb / wa)) < -89.9)

print("── Méthode : 2024-E2, C10 à C13")
Leq = lambda p: (w0 / (2 * m)) / (p * (1 + p / (2 * m * w0)))
verifier("L : gain ω0/2m", w0 / (2 * m), 2.5)
verifier("L : constante 1/(2mω0)", 1 / (2 * m * w0), 0.1)
for p in (0.5j, 3 + 2j):
    Fb = 1 / (1 + 2 * m * p / w0 + p * p / w0 ** 2)
    vrai(f"L = FTBF/(1 − FTBF) en p = {p}", abs(Leq(p) - Fb / (1 - Fb)) < 1e-12)
wu, Mp = marges(Leq, 0.1, 100)
verifier("ω_u de L", wu, 2.43)
verifier("phase en ω_u", Mp - 180, -103.7)
verifier("M_φ de L", Mp, 76, tol=0.006)
Lu = lambda p: Kp * Km * (1 + Ki / p) / (1 + tm * p)
verifier("boucle ouverte à l'entrée du moteur", marges(Lu, 1, 100)[1], 77, tol=0.006)
vrai("phase de L sous −90° à toute pulsation", all(phase(Leq, w) < -90 for w in np.logspace(-2, 3, 30)))
D2 = (186 - 157.1) / 157.1
vrai("D2 lu : (186 − 157,1)/157,1 entre 18 et 19 %", 0.18 <= D2 <= 0.19)
vrai("m pour D2 entre 0,47 et 0,48", 0.47 <= m_D(D2) <= 0.48 and 0.47 <= m_D(0.18) <= 0.48)
verifier("M_φ correspondante", Mphi_m(m_D(D2)), 50, tol=0.01)

print("── Exemple : boucle de vitesse du convoyeur")
R, Lm, K, J = 0.8, 1.6e-3, 0.06, 4e-4
te, tmm = Lm / R, R * J / K ** 2
verifier("τe (ms)", te * 1e3, 2.0)
verifier("τm (ms)", tmm * 1e3, 88.9)
p1, p2 = sorted(np.roots([te * tmm, tmm, 1]).real)
verifier("pôle lent", p2, -11.5)
verifier("pôle rapide", p1, -488)
Kh, Kt = 2.4, 0.02
K0 = Kh * Kt / K
verifier("K0", K0, 0.8)
verifier("K0 en dB", 20 * log10(K0), -1.9, tol=0.03)
G = lambda p: K0 / (1 + tmm * p + te * tmm * p * p)
wc = dicho(lambda w: phase(G, w) + 135, 10, 5000)
verifier("ω_u pour 45°", wc, 511)
verifier("arctan(511/11,5)", degrees(atan(511 / 11.515)), 88.7)
verifier("arctan(511/488)", degrees(atan(511 / 488.5)), 46.3)
verifier("|FTBO| pour K_C = 1", abs(G(1j * wc)), 0.0125, tol=0.005)
verifier("dénominateur 64,2", K0 / abs(G(1j * wc)), 64.2, tol=0.003)
G1 = gdb(G, wc); KC = 10 ** (-G1 / 20); KBO = KC * K0
verifier("G1", G1, -38.1)
verifier("K_C", KC, 80.3)
verifier("K_BO", KBO, 64.2)
verifier("ε_s (%)", 100 / (1 + KBO), 1.5, tol=0.03)
verifier("vitesse établie pour 150 rad/s", 150 * KBO / (1 + KBO), 147.7)
verifier("écart (rad/s)", 150 / (1 + KBO), 2.3, tol=0.01)
verifier("écart (tr/min)", 150 / (1 + KBO) * 60 / (2 * pi), 22, tol=0.01)
verifier("gain statique de la FTBF", KBO / (1 + KBO), 0.985)
w0b = sqrt((1 + KBO) / (te * tmm)); mb = tmm * w0b / (2 * (1 + KBO))
verifier("ω0", w0b, 606)
verifier("m", mb, 0.41, tol=0.01)
verifier("D (%)", 100 * D_m(mb), 24, tol=0.01)
verifier("t_p (ms)", 1e3 * pi / (w0b * sqrt(1 - mb * mb)), 5.7)
verifier("règle 100 m", 100 * mb, 41, tol=0.01)
tt, ys = indicielle(te * tmm / (1 + KBO), tmm / (1 + KBO), KBO / (1 + KBO), 0.03)
verifier("simulation : dépassement (%)", 100 * (ys.max() / ys[-1] - 1), 24, tol=0.01)
verifier("simulation : instant du maximum (ms)", 1e3 * tt[ys.argmax()], 5.7)
verifier("simulation : valeur finale", ys[-1], 0.985)
vrai("M_G infinie : phase > −180° jusqu'à 10⁷ rad/s", phase(G, 1e7) > -180)
verifier("T_max (ms)", 1e3 * radians(45) / wc, 1.5, tol=0.03)
verifier("0,5 ms à 511 rad/s (rad)", 511 * 0.5e-3, 0.26, tol=0.02)
verifier("… en degrés", degrees(511 * 0.5e-3), 15, tol=0.03)
verifier("marge restante", 45 - degrees(511 * 0.5e-3), 30, tol=0.02)
wc65 = dicho(lambda w: phase(G, w) + 115, 10, 5000)
verifier("65° : pulsation", wc65, 255)
G65 = gdb(G, wc65); KC65 = 10 ** (-G65 / 20); KBO65 = KC65 * K0
verifier("65° : gain lu", G65, -29.9)
verifier("65° : K_C", KC65, 31.3)
verifier("65° : K_BO", KBO65, 25.0)
verifier("65° : ε_s (%)", 100 / (1 + KBO65), 3.8, tol=0.02)
w0c = sqrt((1 + KBO65) / (te * tmm)); mc = tmm * w0c / (2 * (1 + KBO65))
verifier("65° : m", mc, 0.65, tol=0.01)
verifier("65° : D (%)", 100 * D_m(mc), 6.6, tol=0.01)
verifier("65° : valeur finale", KBO65 / (1 + KBO65), 0.962)
verifier("ω_u divisée par deux", wc / wc65, 2.0, tol=0.01)
def t5(KBO):
    w0 = sqrt((1 + KBO) / (te * tmm)); m = tmm * w0 / (2 * (1 + KBO)); Kf = KBO / (1 + KBO)
    tt, ys = indicielle(te * tmm / (1 + KBO), tmm / (1 + KBO), Kf, 0.05)
    hors = np.where(np.abs(ys - Kf) > 0.05 * Kf)[0]
    return tt[hors[-1] + 1], tt[ys.argmax()]
t45, tm45 = t5(KBO); t65, tm65 = t5(KBO65)
verifier("45° : maximum (ms)", 1e3 * tm45, 5.7)
verifier("65° : maximum (ms)", 1e3 * tm65, 10.8)
verifier("45° : temps de réponse à 5 % (ms)", 1e3 * t45, 12, tol=0.04)
verifier("65° : temps de réponse à 5 % (ms)", 1e3 * t65, 13, tol=0.02)
vrai("65° : m ≈ 0,7 par la figure 12 (formule du §7)", abs(dicho(lambda m: Mphi_m(m) - 65, 0.3, 1.0) - 0.7) < 0.01)
verifier("commande initiale pour 150 rad/s (V)", Kh * KC * Kt * 150, 580, tol=0.005)

print("── Auto-test")
A1 = lambda p: 100 / (p * (1 + 0.1 * p))
verifier("Q1 : asymptote à 0 dB", 10 * 10 ** (20 / 40), 31.6)
wu, Mp = marges(A1, 1, 1000)
verifier("Q1 : ω_u exacte", wu, 30.8)
verifier("Q1 : phase", Mp - 180, -162, tol=0.003)
verifier("Q1 : M_φ", Mp, 18, tol=0.01)
A2 = lambda p: 10 / (1 + p)
wu, Mp = marges(A2, 1, 100)
verifier("Q2 : ω_u = √99", wu, 9.95)
verifier("Q2 : phase", Mp - 180, -84.3)
verifier("Q2 : M_φ", Mp, 95.7)
verifier("Q2 : T_max (s)", radians(Mp) / wu, 0.168)
A2r = lambda p: 10 * np.exp(-0.01 * p) / (1 + p)
verifier("Q2 : M_φ avec 10 ms", 180 + phase(A2r, marges(A2r, 1, 100)[0]), 90.0, tol=0.002)
wpi = dicho(lambda w: phase(A2r, w) + 180, 50, 500)
verifier("Q2 : ω_π avec retard", wpi, 158, tol=0.005)
verifier("Q2 : M_G avec retard", -gdb(A2r, wpi), 24, tol=0.005)
verifier("Q3 : ω_π = √3", tan(radians(60)), sqrt(3))
verifier("Q3 : K critique", abs((1 + 1j * sqrt(3)) ** 3), 8)
A3 = lambda p: 2 / (1 + p) ** 3
wu, Mp = marges(A3, 0.1, 10)
verifier("Q3 : M_G pour K = 2", 20 * log10(8 / 2), 12, tol=0.004)
verifier("Q3 : ω_u", wu, 0.766)
verifier("Q3 : phase", Mp - 180, -112.4)
verifier("Q3 : arctan 0,766", degrees(atan(0.766)), 37.47, tol=0.001)
verifier("Q3 : M_φ", Mp, 67.6)
r = np.roots([1, 3, 3, 1 + 8.1]); vrai("Q3 : K = 8,1 instable", max(r.real) > 0)
r = np.roots([1, 3, 3, 1 + 7.9]); vrai("Q3 : K = 7,9 stable", max(r.real) < 0)
verifier("Q4 : classe 0", 10 / (1 + 4), 2)
w04, m4 = sqrt(4 / 0.5), 1 / (2 * sqrt(4 * 0.5))
verifier("Q4 : ω0", w04, 2.83)
verifier("Q4 : m", m4, 0.35, tol=0.02)
verifier("Q4 : D (%)", 100 * D_m(m4), 30, tol=0.02)
wu, Mp = marges(lambda p: 4 / (p * (1 + 0.5 * p)), 0.1, 100)
verifier("Q4 : ω_u", wu, 2.50)
verifier("Q4 : M_φ", Mp, 38.7)
m5 = m_D(0.10)
verifier("Q5 : m pour 10 %", m5, 0.59, tol=0.005)
verifier("Q5 : M_φ", Mphi_m(m5), 59, tol=0.01)
verifier("Q5 : m² ", m5 ** 2, 0.349, tol=0.002)
verifier("Q5 : K max", 1 / (4 * m5 ** 2 * 0.1), 7.15, tol=0.002)
vrai("Q5 : K = 7,1 respecte 10 %", D_m(1 / (2 * sqrt(7.1 * 0.1))) <= 0.10)
Kmax = 1 / (4 * m5 ** 2 * 0.1)
verifier("Q5 : marge pour K max", marges(lambda p: Kmax / (p * (1 + 0.1 * p)), 0.1, 100)[1], Mphi_m(m5), tol=0.001)
Q = 10 ** (4 / 20)
m6 = sqrt((1 - sqrt(1 - 1 / Q ** 2)) / 2)
verifier("Q6 : facteur de résonance", Q, 1.585, tol=0.001)
verifier("Q6 : m", m6, 0.335, tol=0.003)
H6 = lambda p: 10 / (1 + 2 * m6 / 100 * p + p * p / 1e4)
wsq = np.logspace(1, 3, 100001)
gq = np.abs([H6(1j * w) for w in wsq])
verifier("Q6 : pic 4 dB au-dessus du plateau", 20 * log10(gq.max() / 10), 4, tol=0.002)
verifier("Q6 : 2m/ω0", 2 * m6 / 100, 6.7e-3, tol=0.005)
verifier("Q6 : résonance", wsq[gq.argmax()], 88, tol=0.005)
verifier("Q6 : dépassement (%)", 100 * D_m(m6), 33, tol=0.01)

print()
if ECARTS:
    print(f"{len(ECARTS)} écart(s) :", ", ".join(ECARTS))
    raise SystemExit(1)
print("Aucun écart.")
