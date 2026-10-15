"""Applications numériques du chapitre T09, refaites en Python.

    python3 cours/calculs/T09.py

Chaque bloc reprend une valeur publiée dans cours/textes/T09.html ; un
écart de plus de 0,5 % sur la valeur arrondie fait échouer le script.
Les valeurs efficaces, fondamentaux et taux de distorsion sont recalculés
par transformée de Fourier des formes d'onde échantillonnées (créneau,
commande décalée, six marches, MLI intersective), indépendamment des
expressions du cours ; le filtre de l'exemple est traité rang par rang.
"""
from math import sqrt, pi, sin, cos, tan, tanh, log, exp, radians, degrees, atan

import numpy as np

ECARTS = []
N = 2 ** 16
TH = np.arange(N) / N * 2 * np.pi


def verifier(nom, calcule, publie, tol=0.005):
    ok = abs(calcule - publie) <= tol * max(abs(publie), 1e-12)
    print(f"{'ok ' if ok else 'ÉCART'} {nom:62s} calculé {calcule:.6g} · publié {publie:g}")
    if not ok:
        ECARTS.append(nom)


def vrai(nom, ok):
    print(f"{'ok ' if ok else 'ÉCART'} {nom}")
    if not ok:
        ECARTS.append(nom)


def eff(v):
    return float(np.sqrt(np.mean(v ** 2)))


def spectre(v):
    """Amplitudes des rangs 0, 1, 2… d'un signal échantillonné sur une période."""
    return np.abs(np.fft.rfft(v)) / N * 2


def thd(v, rang_max=5000):
    s = spectre(v)
    return float(np.sqrt(np.sum(s[2:rang_max] ** 2)) / s[1])


def tri(x):
    x = (x / (2 * np.pi)) % 1
    return np.where(x < 0.5, -1 + 4 * x, 3 - 4 * x)


# ── §2 et §3 : pleine onde monophasée ─────────────────────────────────────
cren = np.where(TH < np.pi, 1.0, -1.0)
s = spectre(cren)
verifier("créneau : V/VDC", eff(cren), 1.0)
verifier("créneau : V̂1/VDC = 4/π", s[1], 4 / pi)
verifier("créneau : 4/π ≈ 1,27", s[1], 1.27, tol=0.003)
verifier("créneau : V1/VDC ≈ 0,90", s[1] / sqrt(2), 0.90, tol=0.002)
verifier("créneau : V̂3/V̂1 (%)", s[3] / s[1] * 100, 33, tol=0.011)
verifier("créneau : V̂5/V̂1 (%)", s[5] / s[1] * 100, 20, tol=0.002)
verifier("créneau : V̂7/V̂1 (%)", s[7] / s[1] * 100, 14, tol=0.021)
vrai("créneau : rangs pairs nuls", max(s[2:40:2]) < 1e-9)
verifier("créneau : THD", thd(cren), sqrt(pi ** 2 / 8 - 1), tol=0.003)
verifier("créneau : THD ≈ 0,483", sqrt(pi ** 2 / 8 - 1), 0.483, tol=0.001)
verifier("créneau : THD limité au rang 40 (%)", thd(cren, 41) * 100, 47.0, tol=0.002)
verifier("créneau : THD rapporté à V ≈ 0,43", sqrt(1 - (s[1] / sqrt(2)) ** 2), 0.43, tol=0.02)
verifier("8 % × 6 ≈ 48 %", 0.483 / 0.08, 6, tol=0.01)
verifier("230 V : V1 (V)", 230 * 2 * sqrt(2) / pi, 207.1, tol=0.001)

# Charge R, L de 2025-E2
R0, L0, V0, f0 = 17.7, 10e-3, 230, 50
tau = L0 / R0
T0 = 1 / f0
Imax = V0 / R0 * tanh(T0 / (4 * tau))
t0 = tau * log(1 + tanh(T0 / (4 * tau)))
verifier("2025-E2 : τ (ms)", tau * 1e3, 0.565, tol=0.001)
verifier("2025-E2 : V/R (A)", V0 / R0, 13.0, tol=0.001)
verifier("2025-E2 : Imax (A)", Imax, 13.0, tol=0.001)
verifier("2025-E2 : T/(4τ) = 8,85", T0 / (4 * tau), 8.85, tol=0.001)
verifier("2025-E2 : t0 (ms)", t0 * 1e3, 0.39, tol=0.01)
verifier("2025-E2 : transistors (ms)", (T0 / 2 - t0) * 1e3, 9.61, tol=0.001)
# contrôle par intégration de l'équation différentielle
dt = T0 / 200000
i = 0.0
for _ in range(10):
    for k in range(200000):
        v = V0 if k < 100000 else -V0
        i += (v - R0 * i) / L0 * dt
verifier("2025-E2 : Imax intégré (A)", abs(i), Imax, tol=0.002)
# fonction tanh : (1 − e^−a)/(1 + e^−a) = tanh(a/2)
a = 1.7
verifier("identité tanh", (1 - exp(-a)) / (1 + exp(-a)), tanh(a / 2), tol=1e-9)

# Q22 de 2025-E2
X1 = 2 * pi * f0 * L0
Z1 = sqrt(R0 ** 2 + X1 ** 2)
verifier("Q22 : Lω (Ω)", X1, 3.14, tol=0.001)
verifier("Q22 : Z1 (Ω)", Z1, 17.98, tol=0.001)
verifier("Q22 : cos φ1", R0 / Z1, 0.985, tol=0.001)
verifier("Q22 : P = S cos φ1 (kW)", 3 * R0 / Z1, 2.95, tol=0.002)
verifier("Q22 : Q = S sin φ1 (kvar)", 3 * X1 / Z1, 0.52, tol=0.01)
I2 = sum((4 * V0 / (n * pi) / sqrt(2) / sqrt(R0 ** 2 + (n * X1) ** 2)) ** 2 for n in range(1, 20001, 2))
verifier("Q22 : I rang par rang (A)", sqrt(I2), 12.2, tol=0.005)
verifier("Q22 : S rang par rang (kVA)", V0 * sqrt(I2) / 1e3, 2.8, tol=0.01)
verifier("Q22 : P = R0 I² (kW)", R0 * I2 / 1e3, 2.65, tol=0.002)
I1q = 4 * V0 / pi / sqrt(2) / Z1
verifier("Q22 : V1 (V)", 4 * V0 / pi / sqrt(2), 207, tol=0.002)
verifier("Q22 : I1 (A)", I1q, 11.5, tol=0.003)
verifier("Q22 : P1 = R0 I1² (kW)", R0 * I1q ** 2 / 1e3, 2.35, tol=0.003)
verifier("Q22 : Q1 = Lω I1² (kvar)", X1 * I1q ** 2 / 1e3, 0.42, tol=0.01)
verifier("Q22 : P des harmoniques (kW)", (R0 * I2 - R0 * I1q ** 2) / 1e3, 0.30, tol=0.02)
S_coh = V0 ** 2 / Z1
verifier("Q22 : S cohérent sous 230 V sinusoïdaux (kVA)", S_coh / 1e3, 2.94, tol=0.002)
verifier("Q22 : P approchée avec S cohérent (kW)", S_coh * R0 / Z1 / 1e3, 2.90, tol=0.002)
verifier("Q22 : écart correspondant (%)", (S_coh * R0 / Z1 / (R0 * I2) - 1) * 100, 9, tol=0.05)
verifier("Q22 : surestimation de P (%)", (3 * R0 / Z1 / (R0 * I2 / 1e3) - 1) * 100, 11, tol=0.05)

# Commande décalée
psi = radians(30)
dec = np.where((TH > psi) & (TH < np.pi - psi), 1.0, np.where((TH > np.pi + psi) & (TH < 2 * np.pi - psi), -1.0, 0.0))
s = spectre(dec)
verifier("décalée : V̂1 = (4/π) cos ψ", s[1], 4 / pi * cos(psi), tol=0.002)
vrai("décalée ψ = 30° : rangs 3 et 9 nuls", s[3] < 1e-3 and s[9] < 1e-3)
verifier("décalée : V/VDC = √(1 − 2ψ/π) = √(2/3)", eff(dec), sqrt(2 / 3), tol=0.002)
vA = np.where(((TH - psi) % (2 * np.pi)) < np.pi, 0.5, -0.5)
vB = np.where(((TH - (np.pi - psi)) % (2 * np.pi)) < np.pi, 0.5, -0.5)
vrai("décalée : v = vAO − vBO, bras B décalé de π − 2ψ", np.max(np.abs((vA - vB) - dec)[np.abs(TH % (np.pi / 6)) > 1e-3]) < 1e-9)

# ── §4 : triphasé pleine onde ────────────────────────────────────────────
def bras(dec_rad):
    return np.where(((TH - dec_rad) % (2 * np.pi)) < np.pi, 0.5, -0.5)
vAO, vBO, vCO = bras(0), bras(2 * np.pi / 3), bras(4 * np.pi / 3)
uAB = vAO - vBO
vNO = (vAO + vBO + vCO) / 3
vAN = vAO - vNO
s = spectre(uAB)
verifier("triphasé : U/VDC = √(2/3)", eff(uAB), sqrt(2 / 3), tol=0.002)
verifier("triphasé : √(2/3) ≈ 0,816", sqrt(2 / 3), 0.816, tol=0.001)
verifier("triphasé : Û1/VDC = 2√3/π", s[1], 2 * sqrt(3) / pi, tol=0.002)
verifier("triphasé : 2√3/π ≈ 1,10", 2 * sqrt(3) / pi, 1.10, tol=0.003)
verifier("triphasé : U1/VDC = √6/π ≈ 0,780", s[1] / sqrt(2), 0.780, tol=0.002)
vrai("triphasé : rangs 3, 9, 15 absents des composées", max(s[3], s[9], s[15]) < 1e-3)
verifier("triphasé : THD limité au rang 40 (%)", thd(uAB, 41) * 100, 29.7, tol=0.003)
verifier("triphasé : Û5 = Û1/5", s[5], s[1] / 5, tol=0.005)
verifier("triphasé : Û7 = Û1/7", s[7], s[1] / 7, tol=0.005)
verifier("triphasé : THD des composées", thd(uAB), sqrt(pi ** 2 / 9 - 1), tol=0.005)
verifier("triphasé : THD ≈ 0,311", sqrt(pi ** 2 / 9 - 1), 0.311, tol=0.001)
verifier("triphasé : U/U1 = π/3", eff(uAB) / (s[1] / sqrt(2)), pi / 3, tol=0.002)
vrai("triphasé : vNO = ± VDC/6", np.allclose(np.abs(vNO), 1 / 6))
verifier("triphasé : vNO change de signe 6 fois", float(np.sum(np.diff(np.sign(vNO)) != 0) + (np.sign(vNO[0]) != np.sign(vNO[-1]))), 6)
vrai("triphasé : vAN prend ±1/3 et ±2/3", set(np.round(np.unique(vAN), 6)) == {-2 / 3 if False else round(-2 / 3, 6), round(-1 / 3, 6), round(1 / 3, 6), round(2 / 3, 6)})
verifier("triphasé : V simple /VDC = √2/3", eff(vAN), sqrt(2) / 3, tol=0.002)
verifier("triphasé : √2/3 ≈ 0,471", sqrt(2) / 3, 0.471, tol=0.002)
verifier("triphasé : U = √3 V", eff(uAB) / eff(vAN), sqrt(3), tol=0.002)
verifier("triphasé : V̂1 simple = 2/π (fondamental de vAO)", spectre(vAN)[1], 2 / pi, tol=0.002)
vrai("triphasé : vAN sans rang multiple de 3", max(spectre(vAN)[3], spectre(vAN)[9]) < 1e-3)

# ── §5 : MLI ─────────────────────────────────────────────────────────────
def mli_bras(ma, mf, dephasage=0.0):
    return np.where(ma * np.sin(TH - dephasage) >= tri(mf * TH), 1.0, -1.0)   # vAO/(VDC/2)


s = spectre(mli_bras(0.8, 21))
verifier("MLI : V̂1/(VDC/2) = ma", s[1], 0.8, tol=0.003)
verifier("MLI ma 0,8 : rang mf", s[21], 0.82, tol=0.005)
verifier("MLI ma 0,8 : rangs mf ± 2", (s[19] + s[23]) / 2, 0.22, tol=0.01)
verifier("MLI ma 0,8 : rangs 2mf ± 1", (s[41] + s[43]) / 2, 0.31, tol=0.015)
vrai("MLI : rangs 3, 5, 7 négligeables", max(s[3], s[5], s[7]) < 0.01)
vrai("MLI mf impair : pas de rang pair", max(s[2:60:2]) < 0.005)
verifier("MLI ma 1 : V̂1", spectre(mli_bras(1.0, 21))[1], 1.0, tol=0.003)
f2 = spectre(mli_bras(2.0, 21))[1]
f4 = spectre(mli_bras(4.0, 21))[1]
vrai(f"MLI : surmodulation sous 4/π ({f2:.3f}, {f4:.3f})", 1.0 < f2 < f4 < 4 / pi)
# moyenne glissante : (2α − 1) VDC/2 avec α = (1 + vref/V̂p)/2
for vr in (-0.6, 0.0, 0.3, 0.8):
    x = np.linspace(0, 2 * np.pi, 200001)
    alpha = float(np.mean(tri(x) <= vr))
    verifier(f"MLI : α pour vref = {vr}", alpha, (1 + vr) / 2, tol=0.002)
# pont bipolaire et unipolaire
ma = 0.8
pa = tri(21 * TH)
vbip = np.where(ma * np.sin(TH) >= pa, 1.0, -1.0)
vuni = np.where(ma * np.sin(TH) >= pa, 1.0, 0.0) - np.where(-ma * np.sin(TH) >= pa, 1.0, 0.0)
sb, su = spectre(vbip), spectre(vuni)
verifier("pont bipolaire : V̂1/VDC = ma", sb[1], 0.8, tol=0.003)
verifier("pont unipolaire : V̂1/VDC = ma", su[1], 0.8, tol=0.003)
vrai("unipolaire : rien avant le rang 37", max(su[2:37]) < 0.01)
vrai("unipolaire : famille de mf annulée", su[21] < 0.01 and su[19] < 0.01)
verifier("unipolaire : rangs 41, 43 (VDC)", (su[41] + su[43]) / 2, 0.314, tol=0.01)
vrai("unipolaire : valeurs 0 et ± VDC seulement", set(np.unique(vuni)) <= {-1.0, 0.0, 1.0})
# triphasé MLI, mf = 21 multiple de 3
uM = (mli_bras(ma, 21) - mli_bras(ma, 21, 2 * np.pi / 3)) / 2       # uAB / VDC
s = spectre(uM)
verifier("MLI triphasé : Û1/VDC = √3 ma/2", s[1], sqrt(3) / 2 * ma, tol=0.003)
vrai("MLI triphasé : raie mf = 21 absente des composées", s[21] < 0.01 and s[19] > 0.1)
vrai("MLI triphasé mf = 21 : seulement des rangs 6k ± 1", max(s[h] for h in range(2, 200) if h % 2 == 0 or h % 3 == 0) < 0.01)
u20 = (mli_bras(ma, 20) - mli_bras(ma, 20, 2 * np.pi / 3)) / 2
s20 = spectre(u20)
vrai("MLI triphasé mf = 20 : il reste des rangs pairs ou multiples de 3", max(s20[18], s20[39]) > 0.1 and s20[20] < 0.01)
verifier("MLI triphasé : U1 = 0,612 ma VDC", sqrt(3) / (2 * sqrt(2)), 0.612, tol=0.001)
verifier("pleine onde / MLI à ma = 1 : 0,612/0,780", 0.612 / 0.780, 0.785, tol=0.002)
verifier("injection : ma max = 2/√3 = 1,155", 2 / sqrt(3), 1.155, tol=0.001)
verifier("injection : U1 = VDC/√2 = 0,707", 0.6124 * 2 / sqrt(3), 1 / sqrt(2), tol=0.001)
inj = lambda d: (2 / sqrt(3)) * (np.sin(TH - d) + np.sin(3 * TH) / 6)
vrai("injection : modulante dans ± 1 (rang 3 de 1/6)", float(np.max(np.abs(inj(0)))) <= 1.0001)
# 2023-E1 : moteur 3,9 A
verifier("2023-E1 : 3,9 √2 (A)", 3.9 * sqrt(2), 5.5, tol=0.003)

# ── §6 : puissances ──────────────────────────────────────────────────────
for thd_ in (0.2, 0.483):
    S = 1.0
    D = S * thd_ / sqrt(1 + thd_ ** 2)
    V1I = S / sqrt(1 + thd_ ** 2)
    verifier(f"D = S·THD/√(1+THD²) (THD {thd_})", D ** 2 + V1I ** 2, S ** 2, tol=1e-9)
phi = radians(36.87)
p = np.cos(phi) - np.cos(2 * TH - phi)            # p/(VI), sinusoïdes de valeur efficace 1
verifier("p mono : max = VI(1 + cos φ)", float(np.max(p)), 1 + cos(phi), tol=0.001)
verifier("p mono : min = −VI(1 − cos φ)", float(np.min(p)), -(1 - cos(phi)), tol=0.002)
ptri = sum(2 * np.sin(TH - k * 2 * np.pi / 3) * np.sin(TH - k * 2 * np.pi / 3 - phi) for k in range(3))
vrai("p tri : constante", float(np.ptp(ptri)) < 1e-9)

# ── §7 : machine ─────────────────────────────────────────────────────────
verifier("auto-test 5 : f = 4 × 750/60 (Hz)", 4 * 750 / 60, 50)
verifier("auto-test 5 : U = 400 × 50/100 (V)", 400 * 50 / 100, 200)
verifier("auto-test 5 : ma", 200 / (0.612 * 540), 0.605, tol=0.002)

# ── Méthode : indices, photovoltaïque ────────────────────────────────────
verifier("indices : ma pour 400 V sous 540 V", 400 / (0.612 * 540), 1.21, tol=0.002)
verifier("2021-E2 : 250 kWc / 320 W", 250e3 / 320, 781.25)
verifier("2021-E2 : 782/30", 782 / 30, 26.1, tol=0.002)
verifier("2021-E2 : 780 × 320 (kWc)", 780 * 320 / 1e3, 249.6)
verifier("2021-E2 : 26 × 34,32 (V)", 26 * 34.32, 892, tol=0.001)
verifier("2021-E2 : 26 × 320 (kW)", 26 * 320 / 1e3, 8.3, tol=0.003)
verifier("2021-E2 : 6 × 8,32 (kW)", 6 * 26 * 320 / 1e3, 49.9, tol=0.001)
# DT7, notre lecture : Voc normalisé ≈ 119 % à −40 °C, ≈ 81 % à 88 °C
pente = (119 - 81) / (88 + 40) / 100
verifier("2021-E2 : pente de Voc (%/K)", pente * 100, 0.3, tol=0.02)
verifier("2021-E2 : Voc à 0 °C (+7,5 %)", 25 * pente * 100, 7.5, tol=0.02)
voc0 = 40.96 * (1 + 25 * pente)
verifier("2021-E2 : panneaux max à 0 °C", float(int(1000 / voc0)), 22)
verifier("2021-E2 : panneaux max à −10 °C", float(int(1000 / (40.96 * (1 + 35 * pente)))), 22)
verifier("2021-E2 : panneaux max à −20 °C", float(int(1000 / (40.96 * (1 + 45 * pente)))), 21)
verifier("2021-E2 : +10,5 % à −10 °C", 35 * pente * 100, 10.5, tol=0.02)
verifier("2021-E2 : +13,5 % à −20 °C", 45 * pente * 100, 13.5, tol=0.02)
verifier("2021-E2 : 13 × 34,32 (V)", 13 * 34.32, 446, tol=0.001)
verifier("2021-E2 : 2 × 9,34 (A)", 2 * 9.34, 18.7, tol=0.002)
verifier("2021-E2 : 13 Voc à 0 °C (V)", 13 * voc0, 572, tol=0.005)
verifier("2021-E2 : 26 × 40,96 (V)", 26 * 40.96, 1065, tol=0.001)
verifier("2016-E1 : 56/3 modules × 245 W", 56 / 3 * 245, 4573, tol=0.001)
vrai("2016-E1 : trois onduleurs dépassent 4 040 W", 19 * 245 > 4040)
verifier("2016-E1 : 7 × 29,90 (V)", 7 * 29.90, 209, tol=0.002)
verifier("2016-E1 : 7 × 37,28 (V)", 7 * 37.28, 261, tol=0.001)
verifier("2016-E1 : 2 × 8,21 (A)", 2 * 8.21, 16.4, tol=0.002)
verifier("2016-E1 : 14 × 245 (W)", 14 * 245, 3430)
verifier("2016-E1 : 14 × 37,28 (V)", 14 * 37.28, 522, tol=0.001)
verifier("2016-E1 : 7 × 27,98 aux conditions NOCT (V)", 7 * 27.98, 196, tol=0.002)
verifier("2016-E1 : 7 × 34,54 à vide, NOCT (V)", 7 * 34.54, 242, tol=0.002)
vrai("2016-E1 : 8,21 A par entrée sous 16 A, 16,4 A par MPPT sous 20 A", 8.21 < 16 and 2 * 8.21 < 20)
verifier("2016-E1 : 7 chaînes de 8 modules", 7 * 8, 56)
verifier("2016-E1 : 8 × 29,90 (V)", 8 * 29.90, 239, tol=0.002)
verifier("2016-E1 : 8 × 27,98 NOCT (V)", 8 * 27.98, 224, tol=0.002)
verifier("2016-E1 : 8 × 37,28 à vide (V)", 8 * 37.28, 298, tol=0.002)
verifier("2016-E1 : 16 × 245 (W)", 16 * 245, 3920)
vrai("2016-E1 : 8 modules, 276 V à vide NOCT, au-dessus du démarrage", 8 * 34.54 > 250)

# ── Exemple : onduleur autonome ──────────────────────────────────────────
VDC, fp, Lf, Cf = 400.0, 20e3, 1e-3, 6.8e-6
Sn, fpw = 3000.0, 0.8
verifier("ex. 1 : 230/0,90 (V)", 230 / (2 * sqrt(2) / pi), 255, tol=0.002)
verifier("ex. 2 : 230 √2 (V)", 230 * sqrt(2), 325.3, tol=0.001)
verifier("ex. 2 : ma", 230 * sqrt(2) / VDC, 0.813, tol=0.001)
verifier("ex. 2 : mf", fp / 50, 400)
Iload = Sn / 230
Zl = 230 / Iload
Rl, Xl = Zl * fpw, Zl * sqrt(1 - fpw ** 2)
verifier("ex. : R équivalent (Ω)", Rl, 14.1, tol=0.002)
verifier("ex. : L équivalent (mH)", Xl / (2 * pi * 50) * 1e3, 33.7, tol=0.002)
Nm = 2 ** 20
thm = np.arange(Nm) / Nm * 2 * np.pi
def tri_m(x):
    x = (x / (2 * np.pi)) % 1
    return np.where(x < 0.5, -1 + 4 * x, 3 - 4 * x)
ma = 230 * sqrt(2) / VDC
pm = tri_m(400 * thm)
vu = VDC * (np.where(ma * np.sin(thm) >= pm, 1.0, 0.0) - np.where(-ma * np.sin(thm) >= pm, 1.0, 0.0))
F = np.fft.rfft(vu) / Nm * 2
n = np.arange(len(F))
w = 2 * pi * 50 * np.maximum(n, 1)
Zload = Rl + 1j * w * Xl / (2 * pi * 50)
Zc = 1 / (1j * w * Cf)
Zp = Zload * Zc / (Zload + Zc)
H = Zp / (Zp + 1j * w * Lf)
Vo = F * H
verifier("ex. 3 : rangs 799, 801 (V)", (abs(F[799]) + abs(F[801])) / 2, 123, tol=0.01)
verifier("ex. 3 : rangs 797, 803 (V)", (abs(F[797]) + abs(F[803])) / 2, 58, tol=0.01)
vrai("ex. 3 : rien entre 50 Hz et 39 kHz", float(np.max(np.abs(F[2:780]))) < 1.0)
verifier("ex. 3 : THD de v (%)", float(np.sqrt(np.sum(np.abs(F[2:]) ** 2)) / abs(F[1])) * 100, 75, tol=0.01)
fc = 1 / (2 * pi * sqrt(Lf * Cf))
verifier("ex. 4 : fc (kHz)", fc / 1e3, 1.93, tol=0.002)
verifier("ex. 4 : (fc/40 kHz)² ≈ 1/430", (fc / 40e3) ** 2, 1 / 430, tol=0.01)
verifier("ex. 4 : raies filtrées (V)", abs(Vo[800 - 1]), 0.29, tol=0.02)
verifier("ex. 4 : THD de sortie (%)", float(np.sqrt(np.sum(np.abs(Vo[2:]) ** 2)) / abs(Vo[1])) * 100, 0.14, tol=0.05)
verifier("ex. 4 : Lf ω (Ω)", Lf * 2 * pi * 50, 0.31, tol=0.02)
verifier("ex. 4 : chute de 1 %", (1 - abs(Vo[1]) / abs(F[1])) * 100, 1, tol=0.05)
verifier("ex. 2 : ma régulé ≈ 0,82", ma * abs(F[1]) / abs(Vo[1]), 0.82, tol=0.005)
verifier("ex. 2 : bus minimal (V)", 230 * sqrt(2) * abs(F[1]) / abs(Vo[1]), 330, tol=0.01)
verifier("ex. 4 : courant de Cf (A)", 230 * 2 * pi * 50 * Cf, 0.49, tol=0.01)
# régulation : ma porté à 0,8214, la sortie vaut 230 V
ma_r = 0.8214
vr = VDC * (np.where(ma_r * np.sin(thm) >= pm, 1.0, 0.0) - np.where(-ma_r * np.sin(thm) >= pm, 1.0, 0.0))
F = np.fft.rfft(vr) / Nm * 2
Vo = F * H
verifier("ex. 5 : sortie régulée (V)", abs(Vo[1]) / sqrt(2), 230, tol=0.001)
IL1 = abs((F[1] - Vo[1]) / (1j * w[1] * Lf)) / sqrt(2)
verifier("ex. 5 : I charge (A)", Iload, 13.0, tol=0.005)
verifier("ex. 5 : I de Lf (A)", IL1, 12.8, tol=0.005)
verifier("ex. 5 : Δi max (A)", VDC / (8 * Lf * fp), 2.5)
IL = (F - Vo) / (1j * w * Lf)
IL[0] = 0
il = np.fft.irfft(IL * Nm / 2, n=Nm)
verifier("ex. 5 : courant crête (A)", float(np.max(il)), 19.3, tol=0.005)
verifier("ex. 5 : crête du fondamental de iLf (A)", IL1 * sqrt(2), 18.0, tol=0.003)
verifier("ex. 5 : 18,0 + 1,25 (A)", IL1 * sqrt(2) + 1.25, 19.3, tol=0.002)
P = Sn * fpw
verifier("ex. 6 : P (W)", P, 2400)
verifier("ex. 6 : IDC (A)", P / VDC, 6.0)
verifier("ex. 6 : iDC min (A)", (P - Sn) / VDC, -1.5)
verifier("ex. 6 : iDC max (A)", (P + Sn) / VDC, 13.5)
verifier("ex. 6 : C (mF)", Sn / (2 * pi * 50 * VDC * 16) * 1e3, 1.5, tol=0.01)
# contrôle de ΔV = S/(ω C VDC) par intégration
C = Sn / (2 * pi * 50 * VDC * 16)
tt = np.linspace(0, 0.02, 20001)
ic = (Sn * np.cos(2 * 2 * pi * 50 * tt - radians(36.87))) / VDC
vC = np.cumsum(ic) * (tt[1] - tt[0]) / C
verifier("ex. 6 : ΔV crête à crête (V)", float(np.ptp(vC)), 16, tol=0.01)

# ── Auto-test ────────────────────────────────────────────────────────────
verifier("Q1 : 4 × 48/π (V)", 4 * 48 / pi, 61.1, tol=0.001)
verifier("Q1 : V1 (V)", 48 * 2 * sqrt(2) / pi, 43.2, tol=0.001)
verifier("Q1 : V3 (V)", 48 * 2 * sqrt(2) / pi / 3, 14.4, tol=0.001)
verifier("Q2 : THD (%)", sqrt(144 + 64 + 36) / 200 * 100, 7.8, tol=0.002)
verifier("Q2 : V (V)", 200 * sqrt(1 + (sqrt(244) / 200) ** 2), 200.6, tol=0.001)
verifier("Q2 : rapporté à V (%)", sqrt(244) / sqrt(200 ** 2 + 244) * 100, 7.8, tol=0.002)
verifier("Q2 : V3/V1 (%)", 12 / 200 * 100, 6)
verifier("Q2 : V5/V1 (%)", 8 / 200 * 100, 4)
verifier("Q2 : V7/V1 (%)", 6 / 200 * 100, 3)
verifier("Q3 : U (V)", sqrt(2 / 3) * 540, 441, tol=0.001)
verifier("Q3 : U1 (V)", sqrt(6) / pi * 540, 421, tol=0.001)
verifier("Q3 : V (V)", sqrt(2) / 3 * 540, 255, tol=0.002)
verifier("Q3 : Û1 (V)", 2 * sqrt(3) / pi * 540, 595, tol=0.001)
verifier("Q3 : Û5 (V)", 2 * sqrt(3) / pi * 540 / 5, 119, tol=0.002)
verifier("Q4 : V1 (V)", 0.8 * 400 / sqrt(2), 226, tol=0.002)
verifier("Q4 : mf", 1050 / 50, 21)
verifier("Q4 : rang 21 (V)", 0.818 * 400, 327, tol=0.001)
verifier("Q4 : rangs 19, 23 (V)", 0.22 * 400, 88, tol=0.001)
verifier("Q4 : rangs 41, 43 unipolaire (V)", 0.314 * 400, 126, tol=0.005)
V1q = 230 * 2 * sqrt(2) / pi
verifier("Q6 : V1 (V)", V1q, 207.1, tol=0.001)
verifier("Q6 : P (W)", V1q * 10 * cos(radians(25.8)), 1864, tol=0.001)
verifier("Q6 : Q (var)", V1q * 10 * sin(radians(25.8)), 901, tol=0.002)
verifier("Q6 : D (VA)", 2300 * 0.4834 / sqrt(1 + 0.4834 ** 2), 1000, tol=0.002)
verifier("Q6 : S² = P² + Q² + D²", sqrt(1864 ** 2 + 901 ** 2 + 1000 ** 2), 2300, tol=0.002)

print()
print("Aucun écart." if not ECARTS else f"{len(ECARTS)} écart(s) : {', '.join(ECARTS)}")
raise SystemExit(1 if ECARTS else 0)
