"""Applications numériques du chapitre T27, refaites en Python.

    python3 cours/calculs/T27.py

Chaque bloc reprend une valeur publiée dans cours/textes/T27.html ; un
écart de plus de 0,5 % sur la valeur arrondie fait échouer le script.
Les fréquences sont recomptées dans cards.json et cours/releve-sujets.json ;
les marges sont cherchées par dichotomie en p = jω ; les réponses
temporelles sont simulées (Euler, pas fin), en continu et en échantillonné.
Les lectures de documents des sujets (« notre lecture ») ne sont vérifiées
que dans leur cohérence interne.
"""
import json
from collections import Counter
from math import sqrt, pi, log, log10, exp, atan, asin, degrees, radians
from pathlib import Path

import numpy as np

RACINE = Path(__file__).resolve().parents[2]
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


def phase(H, w, w0=1e-4):
    """Phase continue en degrés : déroulée depuis une pulsation basse w0."""
    ws = np.logspace(log10(w0), log10(w), 4000)
    ph = np.unwrap(np.angle([H(1j * x) for x in ws]))
    return degrees(ph[-1])


def marges(H, lo, hi):
    wu = dicho(lambda w: abs(H(1j * w)) - 1, lo, hi)
    return wu, 180 + phase(H, wu)


def D_m(m):
    return exp(-pi * m / sqrt(1 - m * m))


def m_D(D):
    return abs(log(D)) / sqrt(pi ** 2 + log(D) ** 2)


def lsim(num, den, u, t):
    """Sortie de num/den (polynômes en p, puissances décroissantes) pour l'entrée u(t),
    par représentation d'état et Euler semi-implicite sur la grille t."""
    den = np.asarray(den, float); num = np.asarray(num, float)
    num = np.concatenate([np.zeros(len(den) - len(num)), num]) / den[0]
    den = den / den[0]
    n = len(den) - 1
    b0 = num[0]
    c = num[1:] - b0 * den[1:]
    x = np.zeros(n); y = np.empty(len(t)); dt = t[1] - t[0]
    for k in range(len(t)):
        y[k] = c[::-1] @ x + b0 * u[k]
        xd = np.empty(n)
        xd[:-1] = x[1:]
        xd[-1] = u[k] - den[1:][::-1] @ x
        x = x + dt * xd
    return y


def indicateurs(t, y, final):
    D = (y.max() - final) / final
    hors = np.where(np.abs(y - final) > 0.05 * abs(final))[0]
    return D, t[hors[-1] + 1] if len(hors) else 0.0


print("── En bref : fréquence")
cartes = json.loads((RACINE / "cards.json").read_text())
th = next(t for t in cartes["themes"] if t["code"] == "T27")
verifier("présence dans les sujets (cartes)", th["presence_n"], 9)
verifier("… sur", th["presence_sur"], 13)
releve = json.loads((RACINE / "cours/releve-sujets.json").read_text())
qs = [(e["id"], q) for e in releve["epreuves"] for q in e["questions"] if "T27" in q["themes"]]
verifier("questions mobilisant T27", len(qs), 31)
verifier("épreuves concernées", len({e for e, _ in qs}), 9)
verifier("questions où T27 est principal", sum(q["themes"][0] == "T27" for _, q in qs), 23)
formes = Counter(q["forme"].split("/")[0] for _, q in qs)
print("   formes :", dict(formes))
verifier("forme « conclure »", sum(v for k, v in formes.items() if k.startswith("conclure")), 9)
verifier("forme « justifier »", sum(v for k, v in formes.items() if k.startswith("justifier")), 5)
verifier("forme « établir »", sum(v for k, v in formes.items() if k.startswith("établir")), 5)
verifier("forme « lire une documentation »", formes["lecture de documentation"], 4)
verifier("forme « calculer »", formes["calcul"], 3)
verifier("forme « choix »", formes["choix"], 3)
ids = {(e, q["q"]) for e, q in qs}
for e, liste in (("2022-E2", ("27", "28", "29")), ("2021-E1", ("33",)), ("2023-E1", ("45", "48", "49")),
                 ("2015-E1", ("13", "14", "15")), ("2023-E2", ("D8", "D9")),
                 ("2024-E2", ("C5", "C6", "C7", "C8", "C9", "C10", "C11", "C12", "C13")),
                 ("2025-E1", ("18", "28")), ("2025-E2", ("Q42",))):
    vrai(f"{e} : questions citées présentes dans le relevé ({', '.join(liste)})",
         all((e, q) in ids for q in liste))

print("── §2 : dépassement et amortissement")
verifier("m pour D = 5 %", m_D(0.05), 0.69, tol=0.002)
verifier("m pour D = 15 %", m_D(0.15), 0.52, tol=0.01)
vrai("m ≥ 0,69 donne D ≤ 5 %", D_m(0.69) <= 0.0501)
vrai("m ≥ 0,52 donne D ≤ 15 %", D_m(0.52) <= 0.15)
# simulation : second ordre sans zéro, m = 0,4
t = np.linspace(0, 20, 200001)
y = lsim([1], [1, 0.8, 1], np.ones_like(t), t)
verifier("formule du dépassement contre simulation (m = 0,4)", y.max() - 1, D_m(0.4), tol=0.002)

print("── §3 : stabilité")
# FTBO = K/[p(1 + p)(1 + 0,1p)] : dénominateur de la FTBF
den = np.polymul([1, 0], np.polymul([1, 1], [0.1, 1]))
vrai("dénominateur 0,1p³ + 1,1p² + p + K", np.allclose(den, [0.1, 1.1, 1, 0]))
verifier("Routh : K critique", 1.1 * 1 / 0.1, 11)
verifier("marge de gain 20,8 dB ↔ facteur 11", 20 * log10(11), 20.8, tol=0.002)
for K, stable in ((10.95, True), (11.05, False)):
    r = np.roots([0.1, 1.1, 1, K])
    vrai(f"K = {K} : boucle fermée {'stable' if stable else 'instable'}", (max(r.real) < 0) == stable)
r = np.roots([0.1, 1.1, 1, 11])
rim = r[np.argmax(r.imag)]
verifier("K = 11 : pôles en ±j√10 (partie imaginaire)", rim.imag, sqrt(10))
vrai("… partie réelle nulle", abs(rim.real) < 1e-9)
s_sep = max(np.roots([0.3, 2.2, 1]))          # dK/dp = 0 sur l'axe réel
verifier("point de séparation du lieu", s_sep, -0.49, tol=0.01)
vrai("séparation entre 0 et −1", -1 < s_sep < 0)
verifier("droite m = 0,5 : angle arccos m (°)", degrees(np.arccos(0.5)), 60)
m, w0 = 0.5, 3.0
pole = complex(-m * w0, w0 * sqrt(1 - m * m))
verifier("pôle de m = 0,5 : angle avec l'axe réel négatif", degrees(np.angle(-pole.conjugate())), 60)
# amortissement décroissant avec K, une fois les pôles complexes
ms = []
for K in (0.5, 1, 2, 5, 8):
    rc = [x for x in np.roots([0.1, 1.1, 1, K]) if x.imag > 1e-9]
    ms.append(-rc[0].real / abs(rc[0]))
vrai("amortissement des pôles complexes décroissant en K", all(a > b for a, b in zip(ms, ms[1:])))

print("── §4 : précision")
for alpha, ech, rampe in ((0, 1 / (1 + 4), None), (1, 0, 1 / 4), (2, 0, 0)):
    L = lambda p, a=alpha: 4 / p ** a / (1 + 0.5 * p)
    e_ech = (lambda p: p * (1 / p) / (1 + L(p)))(1e-9)
    verifier(f"classe {alpha} : erreur en échelon unité (K_BO = 4)", e_ech, ech, tol=1e-6) if ech else vrai(
        f"classe {alpha} : erreur en échelon nulle", abs(e_ech) < 1e-6)
    if rampe is not None:
        e_r = (lambda p: p * (1 / p ** 2) / (1 + L(p)))(1e-9)
        verifier(f"classe {alpha} : erreur en rampe unité", e_r, rampe, tol=1e-6) if rampe else vrai(
            f"classe {alpha} : erreur en rampe nulle", abs(e_r) < 1e-6)
e_r0 = (lambda p: p * (1 / p ** 2) / (1 + 4 / (1 + 0.5 * p)))(1e-9)
vrai("classe 0 : erreur en rampe infinie", e_r0 > 1e7)
# perturbation : S = H2/(1 + H1H2) P, échelon P0
P0 = 1.0
for nom, H1, H2, attendu in (
        ("intégrateur en aval seulement : P0/H1(0)", lambda p: 10, lambda p: 2 / (p * (1 + 0.1 * p)), P0 / 10),
        ("intégrateur en amont : effet nul", lambda p: 10 * (1 + p) / p, lambda p: 2 / (p * (1 + 0.1 * p)), 0),
        ("sans intégrateur : H2(0)P0/(1 + K_BO)", lambda p: 10, lambda p: 2 / (1 + 0.1 * p), 2 * P0 / (1 + 20))):
    s = 1e-9
    eff = s * H2(s) / (1 + H1(s) * H2(s)) * P0 / s
    verifier(nom, eff, attendu, tol=1e-6) if attendu else vrai(nom, abs(eff) < 1e-6)

print("── §5 : correcteur proportionnel (figure 7)")
for K, fin, D in ((2, 0.67, 0), (10, 0.91, 14), (50, 0.98, 45)):
    w0 = sqrt(10 * (1 + K)); m = 11 / (2 * w0)
    verifier(f"K = {K} : valeur finale K/(1 + K)", K / (1 + K), fin, tol=0.006)
    t = np.linspace(0, 3, 300001)
    y = lsim([10 * K], [1, 11, 10 * (1 + K)], np.ones_like(t), t)
    Dsim = (y.max() - K / (1 + K)) / (K / (1 + K))
    if D:
        verifier(f"K = {K} : m", m, {10: 0.52, 50: 0.24}[K], tol=0.02)
        verifier(f"K = {K} : dépassement (%) formule", 100 * D_m(m), D, tol=0.035)
        verifier(f"K = {K} : dépassement (%) simulé", 100 * Dsim, D, tol=0.035)
    else:
        vrai(f"K = {K} : m ≥ 1, pas de dépassement (m = {m:.3f})", m >= 1 and Dsim < 1e-4)
vrai("forme canonique : ω0² = 10(1 + K), 2mω0 = 11",
     np.allclose(np.polymul([1, 1], [0.1, 1]) * 10, [1, 11, 10]))
# réglage sur une marge : K_C = 10^(−G1/20)
G = lambda p: 1 / (p * (1 + p) * (1 + 0.1 * p))
w45 = dicho(lambda w: phase(G, w) + 135, 0.05, 3)
KC = 10 ** (-20 * log10(abs(G(1j * w45))) / 20)
verifier("K_C = 10^(−G1/20) donne bien M_φ = 45°", marges(lambda p: KC * G(p), 0.01, 10)[1], 45, tol=0.002)

print("── §6 : correcteur PI")
C = lambda p: 1 + 1 / p                        # K_p = 1, T_i = 1
verifier("PI : 3 dB au-dessus de l'asymptote en 1/T_i", 20 * log10(abs(C(1j))), 3.0, tol=0.01)
verifier("PI : phase en 1/T_i", degrees(np.angle(C(1j))), -45)
verifier("PI : phase en 10/T_i", degrees(np.angle(C(10j))), -5.7, tol=0.01)
verifier("PI : phase = −90° + arctan(ωT_i) en ωT_i = 3", degrees(np.angle(C(3j))), -90 + degrees(atan(3)), tol=1e-6)
verifier("|C| / K_p en 10/T_i (écart 0,5 %)", abs(C(10j)), 1.005, tol=0.0005)
# figure 9 : procédé 1/[(1 + p)(1 + 0,1p)]
verifier("P, K = 10 : erreur statique", 1 / 11, 0.09, tol=0.02)
m9 = 1 / (2 * sqrt(5 * 0.1))
verifier("PI compensé : m = 1/(2√0,5)", m9, 0.71, tol=0.005)
verifier("PI compensé : dépassement (%)", 100 * D_m(m9), 4, tol=0.1)
Lpi = lambda p: 5 * (1 + p) / p / ((1 + p) * (1 + 0.1 * p))
Lref = lambda p: 5 / (p * (1 + 0.1 * p))
vrai("compensation : FTBO = 5/[p(1 + 0,1p)]", all(abs(Lpi(s) - Lref(s)) < 1e-12 for s in (0.3j, 2 + 1j, 7j)))
t = np.linspace(0, 3, 300001)
y = lsim([50], [1, 10, 50], np.ones_like(t), t)
verifier("PI compensé : dépassement simulé (%)", 100 * (y.max() - 1), 100 * D_m(m9), tol=0.01)
vrai("PI compensé : erreur finale nulle", abs(y[-1] - 1) < 1e-4)
vrai("PI plus amorti que P (K = 10, D = 14 %)", D_m(m9) < D_m(11 / (2 * sqrt(110))))

print("── §7 : PID et avance de phase")
Td = 0.25; Ti = 4 * Td
vrai("T_i = 4T_d : T_iT_d p² + T_i p + 1 = (1 + 2T_d p)²", np.allclose([Ti * Td, Ti, 1], np.polymul([2 * Td, 1], [2 * Td, 1])))
verifier("zéro double : 1/(2T_d) = 1/√(T_iT_d)", 1 / (2 * Td), 1 / sqrt(Ti * Td), tol=1e-9)
verifier("… = 2 rad/s (T_i = 1 s, T_d = 0,25 s)", 1 / sqrt(Ti * Td), 2)
Cpid = lambda p: 1 + 1 / (Ti * p) + Td * p
ws = np.logspace(-2, 3, 50001)
g = np.abs([Cpid(1j * w) for w in ws])
verifier("gain minimal du PID vers", ws[g.argmin()], 2, tol=0.002)
verifier("phase du PID idéal en BF", degrees(np.angle(Cpid(1e-4j))), -90, tol=0.001)
verifier("phase du PID idéal en HF", degrees(np.angle(Cpid(1e4j))), 90, tol=0.001)
for N in (5, 20):
    Cf = lambda p, N=N: 1 + 1 / (Ti * p) + Td * p / (1 + Td * p / N)
    verifier(f"PID filtré N = {N} : gain HF = K_p(1 + N)", abs(Cf(1e7j)), 1 + N, tol=1e-4)
    vrai(f"PID filtré N = {N} : phase HF → 0", abs(degrees(np.angle(Cf(1e7j)))) < 0.01)
for a, v in ((4, 36.9), (10, 54.9)):
    verifier(f"avance a = {a} : φ_max", degrees(asin((a - 1) / (a + 1))), v, tol=0.002)
    tau = 0.01
    Ca = lambda p: (1 + a * tau * p) / (1 + tau * p)
    wsa = np.logspace(0, 4, 40001)
    pa = np.degrees(np.angle([Ca(1j * w) for w in wsa]))
    verifier(f"avance a = {a} : ω_m = 1/(τ√a)", wsa[pa.argmax()], 1 / (tau * sqrt(a)), tol=0.002)
    verifier(f"avance a = {a} : gain √a en ω_m", abs(Ca(1j / (tau * sqrt(a)))), sqrt(a), tol=1e-6)

print("── §9 : correcteur numérique")
verifier("bloqueur : ω_uT_e/2 pour ω_uT_e = 0,1 (°)", degrees(0.05), 2.9, tol=0.02)
# retard moyen du bloqueur : phase du bloqueur d'ordre zéro (1 − e^{−pTe})/(pTe)
Te = 0.1; w = 1.0
B = (1 - np.exp(-1j * w * Te)) / (1j * w * Te)
verifier("bloqueur d'ordre zéro : phase = −ωT_e/2", np.angle(B), -w * Te / 2, tol=1e-9)
# récurrence du PI contre la forme intégrale
Kp, Ti, Te = 2.0, 0.1, 0.01
eps = np.sin(np.arange(200) * 0.37) + 0.3
I = np.cumsum(Te * eps)
u_int = Kp * eps + Kp / Ti * I
u = np.zeros(200); a0, a1 = Kp * (1 + Te / Ti), -Kp
u[0] = a0 * eps[0]
for k in range(1, 200):
    u[k] = u[k - 1] + a0 * eps[k] + a1 * eps[k - 1]
vrai("récurrence u_k = u_{k−1} + a0 ε_k + a1 ε_{k−1} = forme intégrale", np.allclose(u, u_int))
Kco, Tco = 3.0, 0.05
u_int2 = Kco * (Tco * eps + I)
u2 = np.zeros(200); b0, b1 = Kco * (Te + Tco), -Kco * Tco
u2[0] = b0 * eps[0]
for k in range(1, 200):
    u2[k] = u2[k - 1] + b0 * eps[k] + b1 * eps[k - 1]
vrai("forme K_co(1 + T_co p)/p : a0 = K_co(T_e + T_co), a1 = −K_co T_co", np.allclose(u2, u_int2))

print("── Méthode")
# 2022-E2, Q27 (notre lecture de sa figure 16)
verifier("2022-E2 : erreur gain 1 = 750 − 742,4", 750 - 742.4, 7.6, tol=1e-9)
verifier("2022-E2 : erreur gain 10 = 750 − 749,2", 750 - 749.2, 0.8, tol=1e-9)
Kbo1 = 50 / 7.6 - 1
vrai("2022-E2 : lectures cohérentes avec une classe 0 (gain 10 → environ 0,9 N·m)",
     abs(50 / (1 + 10 * Kbo1) - 0.8) < 0.15)
# 2021-E1, Q33 (notre lecture de son annexe A7)
verifier("2021-E1 : réglage 2, 2 000/2 800 (%)", 100 * 2000 / 2800, 71, tol=0.01)
verifier("2021-E1 : réglage 3, 250/2 800 (%)", 100 * 250 / 2800, 9, tol=0.01)
verifier("2021-E1 : réglage 3, 300/2 800 (%)", 100 * 300 / 2800, 11, tol=0.03)
vrai("2021-E1 : réglage 3 sous 15 %", 300 / 2800 < 0.15)
# 2015-E1, Q13 à Q15
KcAc, K12, lam, dT = 1.6 * 110.74, 200, 142e3, 39 - 23
verifier("2015-E1 : K_cA_c", KcAc, 177.2, tol=0.001)
K0 = K12 / KcAc
verifier("2015-E1 : K0 pour K_p = 1", K0, 1.13, tol=0.002)
tau = lam / KcAc
verifier("2015-E1 : constante de temps de l'abri (s)", tau, 801, tol=0.001)
verifier("… boucle fermée 801/2,13 (s)", tau / (1 + K0), 376, tol=0.002)
verifier("… t5 = 3 × 376 (s)", 3 * tau / (1 + K0), 1129, tol=0.002)
verifier("… en minutes", 3 * tau / (1 + K0) / 60, 18.8, tol=0.003)
verifier("… erreur 16/2,13 (°C)", dT / (1 + K0), 7.5, tol=0.003)
Kpmin = 15 * KcAc / K12
verifier("Q14 : K_p minimal", Kpmin, 13.3, tol=0.002)
verifier("Q14 : t5 = 3 × 801/16 (s)", 3 * tau / 16, 150, tol=0.002)
verifier("… en minutes", 3 * tau / 16 / 60, 2.5, tol=0.002)
P0 = K12 * 13.3 * dT
verifier("Q15 : puissance demandée au départ (kW)", P0 / 1e3, 42.6, tol=0.001)
vrai("Q15 : plus de cinq fois 7,9 kW", 5 < P0 / 7.9e3 < 6)
# 2025-E2 (valeurs reprises du chapitre 12, vérifiées dans cours/calculs/T26.py)
vrai("2025-E2 : zéro +77 rad/s et gain 1 102 V repris du chapitre 12",
     "77" in (RACINE / "cours/calculs/T26.py").read_text() and "1102" in (RACINE / "cours/calculs/T26.py").read_text())

print("── Exemple : PI de la boucle de vitesse du convoyeur")
Kmot, R, Lm, J, Kt, Kh = 0.06, 0.8, 1.6e-3, 4e-4, 0.02, 2.4
te, tm = Lm / R, R * J / Kmot ** 2
K0 = Kh * Kt / Kmot
verifier("gain de la FTBO pour K_C = 1", K0, 0.8, tol=1e-9)
p_a, p_b = sorted(np.roots([te * tm, tm, 1]).real)
T1, T2 = -1 / p_b, -1 / p_a
verifier("τ1 (ms)", 1e3 * T1, 86.8, tol=0.001)
verifier("τ2 (ms)", 1e3 * T2, 2.05, tol=0.002)
verifier("rappel ch. 13 : écart ajouté par la charge (rad/s), K_BO = 64,2", R * 0.30 / Kmot ** 2 / (1 + 64.2), 1.0, tol=0.03)
verifier("rappel ch. 13 : erreur relative 1/(1 + K_BO), M_φ = 45° (%)", 100 / 65.2, 1.5, tol=0.03)
G = lambda p: K0 / ((1 + T1 * p) * (1 + T2 * p))
verifier("m pour 10 % de dépassement", m_D(0.10), 0.59, tol=0.005)
m = 0.65
verifier("m² ", m * m, 0.4225, tol=1e-9)
Kl = 1 / (4 * m * m * T2)
verifier("K' = 1/(4m²τ2) (s⁻¹)", Kl, 289, tol=0.002)
verifier("… avec les données arrondies", 1 / (4 * 0.4225 * 2.05e-3), 289, tol=0.002)
Ti = T1
Kp = Kl * Ti / K0
verifier("K_p = K'T_i/0,8", Kp, 31.4, tol=0.002)
verifier("… avec K' = 289 et T_i = 86,8 ms", 289 * 0.0868 / 0.8, 31.4, tol=0.002)
verifier("ω0 = √(K'/τ2) (rad/s)", sqrt(Kl / T2), 376, tol=0.002)
verifier("D théorique (%)", 100 * D_m(m), 6.8, tol=0.005)
L = lambda p: Kp * (1 + Ti * p) / (Ti * p) * G(p)
wu, Mp = marges(L, 10, 1e4)
verifier("ω_u (rad/s)", wu, 256, tol=0.003)
verifier("M_φ (°)", Mp, 62, tol=0.01)
verifier("commande initiale K_p × 0,02 × 10 (V)", Kp * Kt * 10, 6.3, tol=0.005)
verifier("… sur le moteur (V)", Kh * Kp * Kt * 10, 15, tol=0.01)
vrai("… sous 10 V : pas de saturation", Kp * Kt * 10 < 10)


def sim(Kp, Ti, Te=None, T=0.6, dt=2e-6, tcharge=0.15):
    """Boucle de vitesse complète (moteur à deux constantes de temps), consigne 10 rad/s
    à t = 0, charge 0,30 N·m à tcharge ; PI continu ou récurrence échantillonnée."""
    n = int(T / dt); Om = i = integ = u = ek1 = 0.0; ys = np.empty(n)
    nk = int(round(Te / dt)) if Te else None
    a0, a1 = (Kp * (1 + Te / Ti), -Kp) if Te else (0, 0)
    for k in range(n):
        Cr = 0.30 if k * dt >= tcharge else 0.0
        if Te:
            if k % nk == 0:
                ek = Kt * (10 - Om); u = u + a0 * ek + a1 * ek1; ek1 = ek
            U = Kh * u
        else:
            eps = Kt * (10 - Om); integ += eps * dt; U = Kh * Kp * (eps + integ / Ti)
        i += (U - R * i - Kmot * Om) / Lm * dt
        Om += (Kmot * i - Cr) / J * dt
        ys[k] = Om
    t = np.arange(n) * dt
    a = t < tcharge; b = ~a
    D = (ys[a].max() - 10) / 10
    tmax = t[a][ys[a].argmax()]
    t5 = t[np.where(np.abs(ys[a] - 10) > 0.5)[0][-1] + 1]
    dmin = ys[b].min(); tdip = t[b][ys[b].argmin()] - tcharge
    r = np.where(np.abs(ys[b] - 10) > 0.05 * (10 - dmin))[0]
    rec = t[b][r[-1] + 1] - tcharge if r[-1] + 1 < b.sum() else float("nan")
    return dict(D=D, tmax=tmax, t5=t5, dip=dmin, tdip=tdip, rec=rec, fin=ys[-1])


s1 = sim(Kp, Ti, T=1.0)
verifier("simulation : dépassement (%)", 100 * s1["D"], 6.8, tol=0.01)
verifier("simulation : instant du maximum (ms)", 1e3 * s1["tmax"], 11, tol=0.03)
verifier("simulation : t5 (ms)", 1e3 * s1["t5"], 13.4, tol=0.005)
vrai("t5 ≤ 20 ms", s1["t5"] <= 0.020)
verifier("charge : vitesse minimale (rad/s)", s1["dip"], 7.2, tol=0.006)
verifier("… atteinte après (ms)", 1e3 * s1["tdip"], 7, tol=0.075)
vrai("… erreur permanente nulle", abs(s1["fin"] - 10) < 0.01)
verifier("… 95 % de la chute effacés en (s)", s1["rec"], 0.26, tol=0.02)
verifier("pôle compensé −1/τ1 (rad/s)", -1 / T1, -11.5, tol=0.002)
verifier("… constante de temps (ms)", 1e3 * T1, 87, tol=0.003)
# variante : règle de la décade à même marge
lag = degrees(atan(0.1))
wr = dicho(lambda w: phase(G, w) + 180 - Mp - lag, 10, 5000)
Tir = 10 / wr
Kpr = 1 / abs(G(1j * wr) * (1 + 1 / (Tir * 1j * wr)))
verifier("décade : ω_u (rad/s)", wr, 226, tol=0.003)
verifier("décade : T_i (ms)", 1e3 * Tir, 44, tol=0.01)
verifier("décade : K_p", Kpr, 27.0, tol=0.002)
verifier("décade : M_φ obtenue", marges(lambda p: Kpr * (1 + 1 / (Tir * p)) * G(p), 10, 1e4)[1], 62, tol=0.01)
s2 = sim(Kpr, Tir, T=1.0)
verifier("décade : dépassement (%)", 100 * s2["D"], 8.8, tol=0.01)
verifier("décade : t5 (ms)", 1e3 * s2["t5"], 18.5, tol=0.005)
vrai("décade : dans le cahier des charges", s2["D"] <= 0.10 and s2["t5"] <= 0.020)
verifier("décade : chute un peu plus profonde (rad/s)", s2["dip"], 7.0, tol=0.007)
verifier("décade : 95 % effacés en (s)", s2["rec"], 0.13, tol=0.04)
verifier("… deux fois plus vite", s1["rec"] / s2["rec"], 2, tol=0.05)
# implantation numérique
Te = 0.2e-3
verifier("T_e = 0,2 ms : ω_uT_e/2 (rad)", wu * Te / 2, 0.026, tol=0.02)
verifier("… en degrés", degrees(wu * Te / 2), 1.5, tol=0.025)
verifier("a0 = K_p(1 + T_e/T_i)", Kp * (1 + Te / Ti), 31.45, tol=0.0005)
verifier("… facteur 1 + T_e/T_i", 1 + Te / Ti, 1.0023, tol=0.00003)
verifier("a1 = −K_p", -Kp, -31.38, tol=0.0005)
s3 = sim(Kp, Ti, Te=Te, T=0.2)
verifier("T_e = 0,2 ms : dépassement simulé (%)", 100 * s3["D"], 7.8, tol=0.01)
Te = 1e-3
verifier("T_e = 1 ms : perte de phase (°)", degrees(wu * Te / 2), 7.3, tol=0.01)
s4 = sim(Kp, Ti, Te=Te, T=0.2)
verifier("T_e = 1 ms : dépassement simulé (%)", 100 * s4["D"], 12.7, tol=0.01)
vrai("… hors cahier des charges", s4["D"] > 0.10)
verifier("incrément intégral K_pT_e/T_i (T_e = 0,2 ms)", Kp * 0.2e-3 / Ti, 0.07, tol=0.04)
verifier("… = a0 + a1", Kp * (1 + 0.2e-3 / Ti) - Kp, Kp * 0.2e-3 / Ti, tol=1e-9)

print("── Auto-test")
verifier("Q1 : traînage 4/20 (rad)", 4 / 20, 0.2)
m1 = 1 / (2 * sqrt(20 * 0.05))
verifier("Q1 : m", m1, 0.5)
verifier("Q1 : D (%)", 100 * D_m(m1), 16, tol=0.02)
e_r = (lambda p: p * (4 / p ** 2) / (1 + 20 / (p * (1 + 0.05 * p))))(1e-9)
verifier("Q1 : traînage par la valeur finale", e_r, 0.2, tol=1e-6)
den2 = np.polymul(np.polymul([1, 1], [0.5, 1]), [0.2, 1])
vrai("Q2 : 0,1p³ + 0,8p² + 1,7p + 1", np.allclose(den2, [0.1, 0.8, 1.7, 1]))
verifier("Q2 : K critique", 0.8 * 1.7 / 0.1 - 1, 12.6)
for K, stable in ((12.55, True), (12.65, False)):
    r = np.roots([0.1, 0.8, 1.7, 1 + K])
    vrai(f"Q2 : K = {K} {'stable' if stable else 'instable'}", (max(r.real) < 0) == stable)
verifier("Q2 : erreur minimale 1/13,6 (%)", 100 / 13.6, 7.4, tol=0.01)
verifier("Q3 : K_C minimal", (1 / 0.02 - 1) / 2, 24.5)
verifier("Q3 : constante de la boucle fermée (ms)", 1e3 * 0.5 / (1 + 2 * 24.5), 10)
verifier("Q3 : t5 (ms)", 3e3 * 0.5 / (1 + 2 * 24.5), 30)
verifier("Q3 : commande en régime établi", 24.5 / (1 + 2 * 24.5), 0.49)
Kp4 = 0.5 / 0.2
verifier("Q4 : K_p", Kp4, 2.5)
vrai("Q4 : FTBO = 2K_p/[p(1 + 0,1p)]", abs(Kp4 * (1 + 2 * 0.7j) / (2 * 0.7j) * 4 / ((1 + 2 * 0.7j) * (1 + 0.07j))
                                          - 2 * Kp4 / (0.7j * (1 + 0.07j))) < 1e-12)
verifier("Q4 : m", 1 / (2 * sqrt(0.2 * Kp4)), 0.707, tol=0.001)
verifier("Q4 : ω0 (rad/s)", sqrt(2 * Kp4 / 0.1), 7.07, tol=0.001)
verifier("Q4 : D (%)", 100 * D_m(1 / sqrt(2)), 4.3, tol=0.01)
a0, a1 = 2 * (1 + 0.01 / 0.1), -2
verifier("Q5 : a0", a0, 2.2)
uu, e1 = 0.0, 0.0
us = []
for k in range(1, 4):
    uu = uu + a0 * 1 + a1 * e1; e1 = 1; us.append(uu)
for k, v in zip((1, 2, 3), (2.2, 2.4, 2.6)):
    verifier(f"Q5 : u{k}", us[k - 1], v)
verifier("Q5 : incrément K_pT_e/T_i", 2 * 0.01 / 0.1, 0.2)
# Q6 : position, K_C = 10 V/rad, moteur 2/(1 + 0,1p), intégration 1/p, c0 = 0,5 V retranchée
dt, T = 1e-4, 20.0
th = om = 0.0
for k in range(int(T / dt)):
    U = 10 * (0 - th) - 0.5
    om += (2 * U - om) / 0.1 * dt
    th += om * dt
verifier("Q6 : erreur sous la charge (rad), simulée", -th, 0.05, tol=0.002)
th = om = integ = 0.0
for k in range(int(T / dt)):
    eps = 0 - th; integ += eps * dt
    U = 10 * (eps + integ / 2.0) - 0.5
    om += (2 * U - om) / 0.1 * dt
    th += om * dt
vrai("Q6 : avec un PI (T_i = 2 s), erreur annulée", abs(th) < 1e-3)
th = om = 0.0
for k in range(int(T / dt)):
    U = 10 * (1 - th)
    om += (2 * U - om) / 0.1 * dt
    th += om * dt
vrai("Q6 : erreur nulle en consigne (classe 1)", abs(1 - th) < 1e-4)

print()
if ECARTS:
    print(f"{len(ECARTS)} écart(s) :", ", ".join(ECARTS))
    raise SystemExit(1)
print("Aucun écart.")
