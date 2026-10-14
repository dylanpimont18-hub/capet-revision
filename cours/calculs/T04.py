"""Applications numériques du chapitre T04, refaites en Python.

    python3 cours/calculs/T04.py

Chaque bloc reprend une valeur publiée dans cours/textes/T04.html ; un
écart de plus de 0,5 % sur la valeur arrondie fait échouer le script.
Les séries de Fourier sont recalculées par intégration numérique.
"""
from math import sqrt, pi, sin, cos, acos, tan, log10

ECARTS = []


def verifier(nom, calcule, publie, tol=0.005):
    ok = abs(calcule - publie) <= tol * max(abs(publie), 1e-12)
    print(f"{'ok ' if ok else 'ÉCART'} {nom:62s} calculé {calcule:.6g} · publié {publie:g}")
    if not ok:
        ECARTS.append(nom)


def fourier(fn, n, N=20000):
    """Valeur efficace du rang n de fn (période 2π)."""
    a = b = 0.0
    for k in range(N):
        t = 2 * pi * (k + 0.5) / N
        a += fn(t) * cos(n * t)
        b += fn(t) * sin(n * t)
    a, b = 2 * a / N, 2 * b / N
    return sqrt(a * a + b * b) / sqrt(2)


def efficace(fn, N=20000):
    return sqrt(sum(fn(2 * pi * (k + 0.5) / N) ** 2 for k in range(N)) / N)


def creneau(t):
    return 1.0 if (t % (2 * pi)) < pi else -1.0


def cren120(t):
    d = (t % (2 * pi)) * 180 / pi
    return 1.0 if 30 < d < 150 else (-1.0 if 210 < d < 330 else 0.0)


# ── §1 : créneau ───────────────────────────────────────────────────────
verifier("Créneau : amplitude du fondamental 4E/π (× E)", fourier(creneau, 1) * sqrt(2), 1.27)
verifier("Créneau : V1 = 2√2 E/π (× E)", fourier(creneau, 1), 0.90)
verifier("Créneau : V3/V1", fourier(creneau, 3) / fourier(creneau, 1), 1 / 3)
verifier("Créneau : V5/V1", fourier(creneau, 5) / fourier(creneau, 1), 1 / 5)
verifier("Créneau : rang 2 nul", fourier(creneau, 2) + 1, 1)
# Gibbs : dépassement de la somme partielle près du front
S = lambda t, N: sum(4 / (pi * n) * sin(n * t) for n in range(1, N + 1, 2))
dep = max(S(k * pi / 20000, 201) for k in range(1, 400)) - 1
verifier("Gibbs : dépassement relatif (rapporté au saut 2E)", dep / 2, 0.09, tol=0.02)

# ── §2 : créneau de 120° du PD3 ────────────────────────────────────────
I1r = fourier(cren120, 1)
verifier("PD3 : amplitude du fondamental 2√3/π (× Id)", I1r * sqrt(2), 2 * sqrt(3) / pi)
verifier("PD3 : I1 = √6/π Id (× Id)", I1r, 0.78)
verifier("PD3 : I = √(2/3) Id (× Id)", efficace(cren120), 0.82)
for n in (2, 3, 4, 6, 9):
    verifier(f"PD3 : rang {n} nul", fourier(cren120, n) + 1, 1)
for n in (5, 7, 11, 13):
    verifier(f"PD3 : I{n}/I1 = 1/{n}", fourier(cren120, n) / I1r, 1 / n)
for n in (5, 7, 11, 13, 1):
    verifier(f"PD3 : |b_n| = 4/(nπ) |cos(nπ/6)| (rang {n})", fourier(cren120, n) * sqrt(2),
             4 / (n * pi) * abs(cos(n * pi / 6)))


# 12 pulsations : le second pont, alimenté par des tensions décalées de −30°, voit son rang n
# décalé de −30° n ; le couplage Dy du transformateur ajoute +30° (séquence directe, n = 6k + 1)
# ou −30° (séquence inverse, n = 6k − 1). Somme des deux ponts, ramenée au primaire :
for n in (1, 5, 7, 11, 13, 17, 19, 23, 25):
    seq = 1 if n % 6 == 1 else -1
    dephasage = -30 * n + 30 * seq
    somme = abs(1 + complex(cos(dephasage * pi / 180), sin(dephasage * pi / 180))) / 2
    attendu = 1.0 if n % 12 in (1, 11) else 0.0
    verifier(f"12 pulsations : rang {n} conservé (1) ou annulé (0)", somme + 1, attendu + 1)

s12 = sum(1 / n**2 for k in range(1, 100000) for n in (12 * k - 1, 12 * k + 1))
verifier("12 pulsations : THD théorique", sqrt(s12), 0.15, tol=0.02)
verifier("12 pulsations : THD rangs 11 et 13", sqrt(1 / 121 + 1 / 169), 0.119)

# onduleur triphasé en pleine onde : tension simple en six marches
def six_marches(t):
    d = (t % (2 * pi)) * 180 / pi
    return [1, 2, 1, -1, -2, -1][int(d // 60) % 6] / 3


verifier("Six marches : THD", sqrt(efficace(six_marches)**2 / fourier(six_marches, 1)**2 - 1), 0.31, tol=0.01)
for n in (2, 3, 9):
    verifier(f"Six marches : rang {n} nul", fourier(six_marches, n) + 1, 1)

# ── §3 : THD ───────────────────────────────────────────────────────────
verifier("THD du créneau √(π²/8 − 1)", sqrt(pi**2 / 8 - 1), 0.483)
verifier("THD du créneau par la série", sqrt(efficace(creneau)**2 / fourier(creneau, 1)**2 - 1), 0.483)
verifier("THD du PD3 √(π²/9 − 1)", sqrt(pi**2 / 9 - 1), 0.311)
verifier("THD du PD3 par la série", sqrt(efficace(cren120)**2 / I1r**2 - 1), 0.311)
s6 = sum(1 / n**2 for k in range(1, 100000) for n in (6 * k - 1, 6 * k + 1))
verifier("THD du PD3 par Σ 1/n²", sqrt(s6), 0.311)
verifier("THD_R pour THD = 100 %", 1 / sqrt(2), 0.71, tol=0.01)

# ── §4 : puissances ────────────────────────────────────────────────────
verifier("FP = 0,95/√1,25", 0.95 / sqrt(1.25), 0.85, tol=0.01)
verifier("FP du PD3 = I1/I = 3/π", I1r / efficace(cren120), 0.955)
# orthogonalité : moyenne de sin t · sin 3t
moy = sum(sin(2 * pi * (k + .5) / 10000) * sin(3 * 2 * pi * (k + .5) / 10000) for k in range(10000)) / 10000
verifier("Figure 6 : moyenne de v·i3 nulle", moy + 1, 1)

# ── §5 : effets ────────────────────────────────────────────────────────
verifier("Pertes Joule : 1 + 0,5²", 1 + 0.5**2, 1.25)
verifier("Neutre : 3 × 0,6", 3 * 0.6, 1.8)
verifier("Phase : √(1 + 0,6²)", sqrt(1 + 0.36), 1.17, tol=0.01)
# courant de neutre : somme des trois courants de phase déformés
def phase(t, k):
    t = t - 2 * k * pi / 3
    return sin(t) + 0.6 * sin(3 * t) + 0.3 * sin(5 * t)
N = 20000
iN = [sum(phase(2 * pi * (j + .5) / N, k) for k in range(3)) for j in range(N)]
verifier("Neutre : I_N = 3 I3 (simulation, I3 = 0,6/√2)", sqrt(sum(x * x for x in iN) / N), 3 * 0.6 / sqrt(2))
verifier("Self anti-harmonique : rang 4,3 à 50 Hz (Hz)", 4.3 * 50, 215)
verifier("Résonance : √(12 000/500)", sqrt(12000 / 500), 4.9, tol=0.01)

# ── Méthode : 2024-E2, B10 (notre lecture de DT3) ──────────────────────
po = {1: 170, 3: 95, 5: 31, 7: 31, 9: 18}
ml = {1: 171, 3: 2, 5: 38, 7: 21, 9: 2}
verifier("2024-E2 B10 : THD pleine onde", sqrt(sum(po[n]**2 for n in (3, 5, 7, 9))) / po[1], 0.62, tol=0.01)
verifier("2024-E2 B10 : THD MLI", sqrt(sum(ml[n]**2 for n in (3, 5, 7, 9))) / ml[1], 0.25, tol=0.02)
verifier("2024-E2 B10 : THD MLI, lecture basse", sqrt(36.8**2 + 20.4**2 + 0.7**2 + 1**2) / 172.2, 0.24, tol=0.02)
verifier("2024-E2 B10 : THD MLI, lecture haute", sqrt(38.8**2 + 22.4**2 + 2.7**2 + 3**2) / 170.2, 0.26, tol=0.02)
# raies MLI : fréquence lue sur l'échelle log de DT3 (10 Hz à y = 1062 px, 259,5 px par décade)
for y, fr in ((569, 0.8e3), (523, 1.2e3)):
    verifier(f"2024-E2 B12 : raie MLI à y = {y} px (Hz)", 10 * 10 ** ((1062 - y) / 259.5), fr, tol=0.02)
verifier("2024-E2 B12 : rang de 0,8 kHz", 800 / 50, 16)
verifier("2024-E2 B12 : rang de 1,2 kHz", 1200 / 50, 24)

# ── Méthode : 2023-E1, Q16 ─────────────────────────────────────────────
verifier("2023-E1 Q16 : 400√2 (V)", 400 * sqrt(2), 565, tol=0.002)
verifier("2023-E1 Q16 : 3,9√2 (A)", 3.9 * sqrt(2), 5.5, tol=0.01)
verifier("2023-E1 Q16 : raie de 50 Hz de i1 (A)", 2 * sqrt(3) / pi * 2.6, 2.9, tol=0.02)
verifier("2023-E1 Q16 : Ud0 = 3√2·400/π (V)", 3 * sqrt(2) * 400 / pi, 540)
verifier("2023-E1 Q16 : ondulation de u_red à 6 f (Hz)", 6 * 50, 300)

# ── Méthode : 2018-E2 (notre lecture de DRS 3 et DRS 4) ────────────────
rel = {"LUBIO nominal": (0.75, 0.288, 0.71), "LUBIO éco": (0.67, 0.289, 0.64),
       "COMPACTO nominal": (1.00, 0.296, 0.96), "COMPACTO éco": (0.98, 0.285, 0.94)}
publie = {"LUBIO nominal": 0.72, "LUBIO éco": 0.64, "COMPACTO nominal": 0.96, "COMPACTO éco": 0.94}
for nom, (c1, thd, fp) in rel.items():
    calc = c1 / sqrt(1 + thd**2)
    verifier(f"2018-E2 : cos φ1/√(1+THD²), {nom}", calc, publie[nom], tol=0.01)
    verifier(f"2018-E2 : écart arrondi au FP affiché ≤ 0,01, {nom}", abs(round(calc, 2) - fp) + 1, 1, tol=0.0101)
verifier("2018-E2 : S en moins (1 − 1,98/2,72)", 1 - 1.98 / 2.72, 0.27, tol=0.01)
for nom, (i1, thd, ie) in {"LUBIO nominal": (11.12, .288, 11.57), "COMPACTO nominal": (8.15, .296, 8.51)}.items():
    verifier(f"2018-E2 : I1 √(1+THD²) contre I affiché, {nom}", i1 * sqrt(1 + thd**2), ie)

# ── Méthode « établir » : 2018-E2, Q8 ──────────────────────────────────
verifier("2018-E2 Q8 : D COMPACTO nominal (kVA)", sqrt(1.98**2 - 1.90**2), 0.56, tol=0.01)
Q1L = 1.93 * tan(acos(0.75))
verifier("2018-E2 Q8 : Q1 LUBIO nominal (kvar)", Q1L, 1.70)
verifier("2018-E2 Q8 : D LUBIO nominal (kVA)", sqrt(2.72**2 - 1.93**2 - Q1L**2), 0.88, tol=0.01)
verifier("2018-E2 Q8 : S1·THD LUBIO nominal (kVA)", 1.93 / 0.75 * 0.288, 0.74, tol=0.01)
# identité S² − P² − Q1² = D² sur un courant synthétique
import random
random.seed(1)
V1, I1s, ph = 230.0, 10.0, 0.4
Ih = [random.uniform(0, 3) for _ in range(6)]
S2 = (V1 * sqrt(I1s**2 + sum(x * x for x in Ih)))**2
verifier("Établir : S² − P² − Q1² = V² Σ In²", S2 - (V1 * I1s)**2, V1**2 * sum(x * x for x in Ih))
verifier("Établir : FP = cos φ1/√(1 + THD²)", V1 * I1s * cos(ph) / sqrt(S2),
         cos(ph) / sqrt(1 + sum(x * x for x in Ih) / I1s**2))

# ── Méthode : 2025-E2, Q23 ─────────────────────────────────────────────
verifier("2025-E2 Q23 : THD du créneau", sqrt(pi**2 / 8 - 1), 0.48, tol=0.01)
verifier("2025-E2 Q23 : rapport au niveau de 8 %", 0.48 / 0.08, 6)

# ── Exemple : PD3, Id = 50 A ───────────────────────────────────────────
U, Id = 400.0, 50.0
V = U / sqrt(3)
I = Id * sqrt(2 / 3)
I1 = sqrt(6) / pi * Id
verifier("Ex. : √(2/3)", sqrt(2 / 3), 0.816, tol=0.001)
verifier("Ex. : √6/π", sqrt(6) / pi, 0.780, tol=0.001)
verifier("Ex. : I (A)", I, 40.8)
verifier("Ex. : I1 (A)", I1, 39.0)
for n, val in ((5, 7.80), (7, 5.57), (11, 3.54), (13, 3.00)):
    verifier(f"Ex. : I{n} (A)", I1 / n, val)
thd513 = sqrt(7.80**2 + 5.57**2 + 3.54**2 + 3.00**2) / 39.0
verifier("Ex. : THD rangs 5 à 13", thd513, 0.273)
verifier("Ex. : I1 √(1 + 0,311²) (A)", 39.0 * sqrt(1 + 0.311**2), 40.8)
verifier("Ex. : facteur 1,047", sqrt(1 + 0.311**2), 1.047, tol=0.001)
Ud0 = 3 * sqrt(2) * U / pi
verifier("Ex. : Ud0 (V)", Ud0, 540)
P = Ud0 * Id
verifier("Ex. : P = Ud0 Id (kW)", P / 1e3, 27.0)
verifier("Ex. : P = √3 U I1 (kW)", sqrt(3) * U * I1 / 1e3, 27.0)
Sx = sqrt(3) * U * I
verifier("Ex. : S (kVA)", Sx / 1e3, 28.3)
verifier("Ex. : D = √(S² − P²) (kVA)", sqrt(Sx**2 - P**2) / 1e3, 8.40)
verifier("Ex. : FP", P / Sx, 0.955)
IH = sqrt(I**2 - I1**2)
verifier("Ex. : I_H (A)", IH, 12.1)
verifier("Ex. : 3 V I_H (kVA)", 3 * V * IH / 1e3, 8.40)
verifier("Ex. : 3 × 230,9 × 12,12 (kVA)", 3 * 230.9 * 12.12 / 1e3, 8.40)
Xcc = U**2 / 2e6
verifier("Ex. : Xcc (Ω)", Xcc, 0.080)
verifier("Ex. : V_n = Xcc I1 (V)", Xcc * I1, 3.12)
verifier("Ex. : V_n / V (%)", Xcc * I1 / V * 100, 1.35)
verifier("Ex. : THD_u rangs 5 à 13 (%)", sqrt(4) * Xcc * I1 / V * 100, 2.7)
rangs49 = [n for k in range(1, 9) for n in (6 * k - 1, 6 * k + 1) if n <= 49]
rangs40 = [n for k in range(1, 8) for n in (6 * k - 1, 6 * k + 1) if n <= 40]
verifier("Ex. : nombre de rangs 6k ± 1 jusqu'au rang 40", len(rangs40), 12)
verifier("Ex. : THD_u jusqu'au rang 40 (%)", sqrt(12) * 1.35, 4.7, tol=0.01)
verifier("Ex. : THD_u jusqu'au rang 40, exact (%)", sqrt(len(rangs40)) * Xcc * I1 / V * 100, 4.7, tol=0.01)
verifier("Ex. : THD_u jusqu'au rang 49 (%)", sqrt(len(rangs49)) * Xcc * I1 / V * 100, 5.4)

# ── Auto-test ──────────────────────────────────────────────────────────
verifier("AT1 : I_H (A)", sqrt(9 + 4 + 1), 3.74)
verifier("AT1 : THD", sqrt(14) / 10, 0.374)
verifier("AT1 : I (A)", sqrt(114), 10.7)
verifier("AT1 : THD_R", sqrt(14) / sqrt(114), 0.350)
verifier("AT2 : V1 (V)", 4 * 48 / (pi * sqrt(2)), 43.2)
verifier("AT2 : V3 (V)", 4 * 48 / (3 * pi * sqrt(2)), 14.4)
verifier("AT3 : I phase (A)", sqrt(136), 11.7)
verifier("AT3 : I neutre (A)", 3 * 6, 18)
verifier("AT4 : I (A)", 20 * sqrt(2 / 3), 16.3)
verifier("AT4 : I1 (A)", sqrt(6) * 20 / pi, 15.6)
verifier("AT4 : I5 (A)", sqrt(6) * 20 / pi / 5, 3.12)
verifier("AT5 : FP de A", 0.98 / sqrt(1.64), 0.77, tol=0.01)
verifier("AT5 : FP de B", 0.95 / sqrt(1.01), 0.95, tol=0.01)
L = 1 / (4 * pi**2 * 1e3**2 * 10e-6)
verifier("AT6 : L (mH)", L * 1e3, 2.53)
verifier("AT6 : gain à 10 kHz, 1/|1 − 100|", 1 / 99, 1 / 99)
verifier("AT6 : gain en dB à 10 kHz", 20 * log10(1 / 99), -40, tol=0.01)
verifier("AT6 : gain à 50 Hz", 1 / (1 - 0.05**2), 1.003, tol=0.001)


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
HZ = inv(SEC)
RELATIONS = [
    ("T04-f-002 THD = √(ΣI²)/I1", SANS, mul(AMP, inv(AMP))),
    ("T04-f-004 I = I1 √(1 + THD²)", AMP, AMP),
    ("T04-f-005 P = V1 I1 cos φ1", WATT, mul(VOLT, AMP)),
    ("T04-f-006 Q1 = V1 I1 sin φ1", WATT, mul(VOLT, AMP)),
    ("T04-f-007 D = V1 √(ΣIn²)", WATT, mul(VOLT, AMP)),
    ("T04-f-008 S² = P² + Q1² + D²", puis(WATT, 2), puis(WATT, 2)),
    ("T04-f-009 FP = P/S", SANS, mul(WATT, inv(WATT))),
    ("T04-f-013 α = t_on/T", SANS, mul(SEC, inv(SEC))),
    ("T04-f-015 f_c = 1/(2π√(LC))", HZ, puis(mul(HENRY, FARAD), -0.5)),
    ("V_n = n Xcc I_n", VOLT, mul(OHM, AMP)),
    ("Xcc = U²/S_cc", OHM, mul(puis(VOLT, 2), inv(WATT))),
    ("n_r = √(S_cc/|Q_C|)", SANS, mul(WATT, inv(WATT))),
    ("P = Ud0 Id", WATT, mul(VOLT, AMP)),
]
for nom, g, d in RELATIONS:
    ok = g == d
    print(f"{'ok ' if ok else 'ÉCART'} homogénéité · {nom}")
    if not ok:
        ECARTS.append(nom)

print()
print("Aucun écart." if not ECARTS else f"{len(ECARTS)} écart(s) : {ECARTS}")
raise SystemExit(1 if ECARTS else 0)
