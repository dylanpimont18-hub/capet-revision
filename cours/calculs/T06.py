"""Applications numériques du chapitre T06, refaites en Python.

    python3 cours/calculs/T06.py

Chaque bloc reprend une valeur publiée dans cours/textes/T06.html ; un
écart de plus de 0,5 % sur la valeur arrondie fait échouer le script.
La chute de tension exacte est recalculée sur le diagramme de Fresnel,
en nombres complexes.
"""
from math import sqrt, pi, sin, cos, acos, radians
from cmath import rect

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


# ── §1 : transformateur parfait, formule de Boucherot ──────────────────
verifier("Boucherot : 2π/√2", 2 * pi / sqrt(2), 4.44)
# Puissance conservée : V2 I2 = (m V1)(I1/m)
m, V1, I1 = 0.1, 230.0, 2.0
verifier("Parfait : V2 I2 = V1 I1", (m * V1) * (I1 / m), V1 * I1)

# ── §4 : courant de court-circuit ──────────────────────────────────────
verifier("Icc / In pour εcc = 4 %", 1 / 0.04, 25)

# ── §7 : redresseur ────────────────────────────────────────────────────
kPD2, kPD3 = 2 * sqrt(2) / pi, 3 * sqrt(2) / pi
verifier("PD2 : 2√2/π", kPD2, 0.90)
verifier("PD3 : 3√2/π", kPD3, 1.35)
V2 = 48 / kPD2
verifier("§7 : V2 pour 48 V continus (PD2)", V2, 53.3)
verifier("§7 : m = V2/230", V2 / 230, 0.232)

# ── Exemple chiffré : 250 kVA, 20 kV / 410 V, Dyn11 ────────────────────
Sn, U1n, U20, f = 250e3, 20e3, 410.0, 50
P0, I0 = 650.0, 6.0
Pcc, U1cc = 3250.0, 800.0
cphi = 0.85
sphi = sqrt(1 - cphi ** 2)
V20 = U20 / sqrt(3)
verifier("Ex : V20 = 410/√3", V20, 236.7)
I1n = Sn / (sqrt(3) * U1n)
I2n = Sn / (sqrt(3) * U20)
verifier("Ex 1 : I1n", I1n, 7.22)
verifier("Ex 1 : I2n", I2n, 352)
m = U20 / U1n
verifier("Ex 1 : m", m, 0.0205)
verifier("Ex 1 : N2/N1 = m/√3 (Dyn)", m / sqrt(3), 0.0118)
verifier("Ex 1 : spires HT par spire BT", sqrt(3) / m, 84.5)
verifier("Ex 1 : I0/I2n (%)", 100 * I0 / I2n, 1.7, tol=0.02)

S0 = sqrt(3) * U20 * I0
Q0 = sqrt(S0 ** 2 - P0 ** 2)
verifier("Ex 2 : S0 (kVA)", S0 / 1e3, 4.26)
verifier("Ex 2 : Q0 (kvar)", Q0 / 1e3, 4.21)
verifier("Ex 2 : FP à vide", P0 / S0, 0.15, tol=0.02)
verifier("Ex 2 : P0/3", P0 / 3, 217)
verifier("Ex 2 : Q0/3", Q0 / 3, 1404)
Rf = V20 ** 2 / (P0 / 3)
Xm = V20 ** 2 / (Q0 / 3)
verifier("Ex 2 : Rf (Ω)", Rf, 259)
verifier("Ex 2 : Rf = U²/P0 (même valeur)", U20 ** 2 / P0, 259)
verifier("Ex 2 : Xm (Ω)", Xm, 39.9)

Rs = Pcc / (3 * I2n ** 2)
verifier("Ex 3 : Rs (mΩ)", Rs * 1e3, 8.74)
Vcc2 = m * U1cc / sqrt(3)
verifier("Ex 3 : m U1cc/√3 (V)", Vcc2, 9.47)
Zs = Vcc2 / I2n
Xs = sqrt(Zs ** 2 - Rs ** 2)
verifier("Ex 3 : Zs (mΩ)", Zs * 1e3, 26.9)
verifier("Ex 3 : Xs (mΩ)", Xs * 1e3, 25.4)
ecc, eR = U1cc / U1n, Pcc / Sn
eX = sqrt(ecc ** 2 - eR ** 2)
verifier("Ex 3 : εcc (%)", 100 * ecc, 4)
verifier("Ex 3 : εR = Pcc/Sn (%)", 100 * eR, 1.3)
verifier("Ex 3 : εR = Rs I2n / V20 (%)", 100 * Rs * I2n / V20, 1.3)
verifier("Ex 3 : εX (%)", 100 * eX, 3.78)
verifier("Ex 3 : εX = Xs I2n / V20 (%)", 100 * Xs * I2n / V20, 3.78)

verifier("Ex 4 : sin φ2", sphi, 0.527)
verifier("Ex 4 : εR cos φ2 (%)", 100 * eR * cphi, 1.10, tol=0.01)
verifier("Ex 4 : εX sin φ2 (%)", 100 * eX * sphi, 1.99)
dv = eR * cphi + eX * sphi
verifier("Ex 4 : ΔV2/V20 (%)", 100 * dv, 3.1, tol=0.01)
verifier("Ex 4 : ΔV2 par phase (V)", dv * V20, 7.33)
verifier("Ex 4 : U2 approché (V)", U20 * (1 - 0.031), 397)
# Exact : |V2 + (Rs + jXs) I2 e^{-jφ}| = V20, V2 réel
Z = complex(Rs, Xs) * rect(I2n, -acos(cphi))
V2x = sqrt(V20 ** 2 - Z.imag ** 2) - Z.real
verifier("Ex 4 : U2 exact, Fresnel (V)", sqrt(3) * V2x, 397.2, tol=0.0005)

P2 = sqrt(3) * 397 * 352 * cphi
verifier("Ex 5 : P2 (kW)", P2 / 1e3, 205.7, tol=0.001)
verifier("Ex 5 : pertes (W)", P0 + Pcc, 3900)
verifier("Ex 5 : η (%)", 100 * 205.7 / (205.7 + 3.9), 98.1, tol=0.001)
xo = sqrt(P0 / Pcc)
verifier("Ex 5 : x_opt", xo, 0.447)
verifier("Ex 5 : I2 à x_opt (A)", xo * I2n, 157)
verifier("Ex 5 : P2 à x_opt (kW)", 0.447 * 205.7, 92.0, tol=0.001)
verifier("Ex 5 : pertes à x_opt (W)", P0 + xo ** 2 * Pcc, 1300)
verifier("Ex 5 : η max (%)", 100 * 92.0 / (92.0 + 1.3), 98.6, tol=0.001)
verifier("Fig 8 : x_opt ≈ 0,45", xo, 0.45, tol=0.01)

verifier("Ex 6 : Icc = I2n/εcc (kA)", I2n / ecc / 1e3, 8.8)
verifier("Méthode plaque : chute ≈ 3 % à pleine charge", 100 * dv, 3, tol=0.04)

# Méthode conformité : chute du transformateur sous le FP de 2024-E2
fp = 181.7 / 192.6
verifier("2024-E2 : FP vu du transformateur", fp, 0.94, tol=0.01)
verifier("2024-E2 : chute à pleine charge (%)", 100 * (eR * fp + eX * sqrt(1 - fp ** 2)), 2.5, tol=0.02)
verifier("2024-E2 : U_D = S_T/(√3 I_tot)", 192600 / (sqrt(3) * 258), 431)
verifier("2024-E2 : chute de la ligne (%)", 100 * (1 - 400 / (192600 / (sqrt(3) * 258))), 7.2, tol=0.01)
# Ex 6 : réseau amont de 500 MVA
Zr = U20 ** 2 / 500e6
verifier("Ex 6 : U²/Scc vu de la BT (mΩ)", Zr * 1e3, 0.34, tol=0.02)
Zt = abs(complex(Rs, Xs) + complex(0, Zr))
verifier("Ex 6 : baisse relative de Icc (%)", 100 * (1 - Zs / Zt), 1, tol=0.3)
# §7 : 12 pulsations, Dd0 et Dy11 sur un même primaire
verifier("§7 : rapport des spires Dd/Dy", (U20 / U1n) / (U20 / U1n / sqrt(3)), sqrt(3))

# ── Auto-test ──────────────────────────────────────────────────────────
# Q1
m1 = 24 / 230
verifier("Q1 : m", m1, 0.104)
verifier("Q1 : I2n", 100 / 24, 4.17)
verifier("Q1 : I1n", 100 / 230, 0.435)
verifier("Q1 : R vue du primaire", 5.76 / m1 ** 2, 529)
verifier("Q1 : 230²/100", 230 ** 2 / 100, 529)
verifier("Q1 : P dans 5,76 Ω sous 24 V", 24 ** 2 / 5.76, 100)
# Q2
S0q, P0q = 230 * 0.25, 15.0
Q0q = sqrt(S0q ** 2 - P0q ** 2)
verifier("Q2 : S0", S0q, 57.5)
verifier("Q2 : Q0", Q0q, 55.5)
verifier("Q2 : Rf (kΩ)", 230 ** 2 / P0q / 1e3, 3.53)
verifier("Q2 : Xm (Ω)", 230 ** 2 / Q0q, 953)
verifier("Q2 : IRf (mA)", 1e3 * P0q / 230, 65, tol=0.01)
verifier("Q2 : Im (mA)", 1e3 * Q0q / 230, 241)
verifier("Q2 : √(IRf² + Im²) = I0", sqrt((P0q / 230) ** 2 + (Q0q / 230) ** 2), 0.25)
# Q3
I2q = 2000 / 115
Rsq = 60 / I2q ** 2
Zsq = 0.5 * 12 / I2q
Xsq = sqrt(Zsq ** 2 - Rsq ** 2)
verifier("Q3 : εcc (%)", 100 * 12 / 230, 5.2, tol=0.01)
verifier("Q3 : I2n", I2q, 17.4)
verifier("Q3 : Rs", Rsq, 0.198)
verifier("Q3 : Zs", Zsq, 0.345)
verifier("Q3 : Xs", Xsq, 0.282)
# Q4
dvi = 17.4 * (0.198 * 0.6 + 0.282 * 0.8)
dvc = 17.4 * (0.198 * 0.6 - 0.282 * 0.8)
verifier("Q4 : ΔV2 inductif", dvi, 6.0, tol=0.01)
verifier("Q4 : V2 inductif", 115 - dvi, 109)
verifier("Q4 : Rs cos φ", 0.198 * 0.6, 0.119)
verifier("Q4 : Xs |sin φ|", 0.282 * 0.8, 0.226)
verifier("Q4 : ΔV2 capacitif (arrondi à 0,1 V)", round(dvc, 1), -1.9)
verifier("Q4 : V2 capacitif", 115 - dvc, 117)
# Q5
verifier("Q5 : N2/N1 Dyn", (410 / sqrt(3)) / 20e3, 0.0118)
verifier("Q5 : |1 − e^{j30°}| (%)", 100 * abs(1 - rect(1, radians(30))), 52, tol=0.01)
# Q6
V2q = 24 / kPD2
verifier("Q6 : V2", V2q, 26.7)
verifier("Q6 : m", V2q / 230, 0.116)
verifier("Q6 : défaut avec m = 24/230 (%)", 100 * (1 - kPD2), 10, tol=0.01)

# Q6 : rendement
P2q = 109 * 17.4 * 0.6
verifier("Q6 : P2 (W)", P2q, 1138)
verifier("Q6 : η (%)", 100 * P2q / (P2q + 15 + 60), 93.8, tol=0.001)
verifier("Q6 : x_opt", sqrt(15 / 60), 0.5)
verifier("Q6 : I2 à x_opt (A)", 0.5 * I2q, 8.7)
verifier("Q6 : P2 à x_opt (W)", 0.5 * P2q, 569)
verifier("Q6 : η max (%)", 100 * 569 / (569 + 30), 95.0, tol=0.001)
verifier("Q3 : I0 / I1n (%)", 100 * 0.25 / (2000 / 230), 2.9, tol=0.02)

# ── Homogénéité ────────────────────────────────────────────────────────
# Dimensions [M, L, T, I] ; tension = M L² T⁻³ I⁻¹
V_, A_ = (1, 2, -3, -1), (0, 0, 0, 1)
W_ = (1, 2, -3, 0)
OHM = tuple(a - b for a, b in zip(V_, A_))


def mul(*ds):
    return tuple(sum(c) for c in zip(*ds))


def puis(d, k):
    return tuple(k * c for c in d)


homogene("Rf = V1²/P0 en Ω", mul(puis(V_, 2), puis(W_, -1)) == OHM)
homogene("P0 = Rf IRf² en W", mul(OHM, puis(A_, 2)) == W_)
homogene("Pcc = Rs I2cc² en W", mul(OHM, puis(A_, 2)) == W_)
homogene("Zs = m V1cc / I2cc en Ω", mul(V_, puis(A_, -1)) == OHM)
homogene("ΔV2 = Rs I2 cos φ + Xs I2 sin φ en V", mul(OHM, A_) == V_)
homogene("εR = Pcc/Sn sans dimension", mul(W_, puis(W_, -1)) == (0, 0, 0, 0))
# V1 = 4,44 N f B S : B en T = V s m⁻², f en s⁻¹, S en m²
T_ = mul(V_, (0, 0, 1, 0), (0, -2, 0, 0))
homogene("V1 = 4,44 N f B S en V", mul((0, 0, -1, 0), T_, (0, 2, 0, 0)) == V_)

print()
print("Aucun écart." if not ECARTS else f"{len(ECARTS)} écart(s) : {', '.join(ECARTS)}")
raise SystemExit(1 if ECARTS else 0)
