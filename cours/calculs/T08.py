"""Applications numériques du chapitre T08, refaites en Python.

    python3 cours/calculs/T08.py

Chaque bloc reprend une valeur publiée dans cours/textes/T08.html ; un
écart de plus de 0,5 % sur la valeur arrondie fait échouer le script.
Les valeurs moyennes, efficaces, taux d'ondulation, facteurs de puissance
et taux de distorsion sont recalculés par intégration numérique des formes
d'onde (règle « max − min » des groupes de diodes), indépendamment des
expressions du cours.
"""
from math import sqrt, pi, sin, cos, radians, degrees, acos, tan, atan2, exp

ECARTS = []
N = 36000


def verifier(nom, calcule, publie, tol=0.005):
    ok = abs(calcule - publie) <= tol * max(abs(publie), 1e-12)
    print(f"{'ok ' if ok else 'ÉCART'} {nom:62s} calculé {calcule:.6g} · publié {publie:g}")
    if not ok:
        ECARTS.append(nom)


def vrai(nom, ok):
    print(f"{'ok ' if ok else 'ÉCART'} {nom}")
    if not ok:
        ECARTS.append(nom)


def moy(fn):
    return sum(fn(360 * k / N) for k in range(N)) / N


def eff(fn):
    return sqrt(sum(fn(360 * k / N) ** 2 for k in range(N)) / N)


def fondamental(fn):
    """Amplitude et phase (degrés) du fondamental de fn(θ), θ en degrés, par rapport à sin θ."""
    a = sum(fn(360 * k / N) * cos(radians(360 * k / N)) for k in range(N)) * 2 / N
    b = sum(fn(360 * k / N) * sin(radians(360 * k / N)) for k in range(N)) * 2 / N
    return sqrt(a * a + b * b), degrees(atan2(a, b))


S = lambda t: sin(radians(t))
V3 = (lambda t: S(t), lambda t: S(t - 120), lambda t: S(t - 240))

# ── PD2 : u_d = max − min des deux bornes (v_A = v/2, v_B = −v/2) ──────
ud2 = lambda t: max(S(t) / 2, -S(t) / 2) - min(S(t) / 2, -S(t) / 2)
verifier("PD2 : ⟨u_d⟩/V̂ = 2/π", moy(ud2), 2 / pi)
verifier("PD2 : ⟨u_d⟩/V ≈ 0,90", moy(ud2) * sqrt(2), 0.90)
verifier("PD2 : 0,90 × 230 (V)", moy(ud2) * sqrt(2) * 230, 207, tol=0.003)
verifier("PD2 : valeur efficace de u_d = V", eff(ud2) * sqrt(2), 1.0)
ond2 = sqrt(eff(ud2) ** 2 - moy(ud2) ** 2) / moy(ud2)
verifier("PD2 : taux d'ondulation (%)", ond2 * 100, 48, tol=0.01)
# courant de ligne en créneaux ±I_d
cr = lambda t: 1.0 if (t % 360) < 180 else -1.0
I1, phi = fondamental(cr)
verifier("PD2 : fondamental du créneau 4/π", I1, 4 / pi)
vrai(f"PD2 : fondamental en phase avec v ({phi:.3f}°)", abs(phi) < 0.05)
verifier("PD2 : FP = I1/√2 / I_d", I1 / sqrt(2) / eff(cr), 0.90, tol=0.002)
verifier("PD2 : FP = 2√2/π", 2 * sqrt(2) / pi, 0.90, tol=0.002)
thd2 = sqrt((eff(cr) / (I1 / sqrt(2))) ** 2 - 1)
verifier("PD2 : THD_i (%)", thd2 * 100, 48, tol=0.01)
iD1 = lambda t: 1.0 if (t % 360) < 180 else 0.0
verifier("PD2 : diode, courant moyen I_d/2", moy(iD1), 0.5)
verifier("PD2 : diode, courant efficace I_d/√2", eff(iD1), 1 / sqrt(2))
verifier("PD2 : crête de 230 V (V)", 230 * sqrt(2), 325, tol=0.002)

# ── Filtrage capacitif (figure 4 et exemple) ───────────────────────────
tau = 2 * pi * 3.3
u, hist = 0.0, []
M = 1440
for kk in range(M * 6):
    t = kk * 360 / M
    va = abs(S(t))
    dec = u * exp(-radians(360 / M) / tau)
    un = max(va, dec)
    hist.append(un)
    u = un
dern = hist[4 * M:]
umin = min(dern)
verifier("figure 4 : ondulation relative (%)", (1 - umin) * 100, 12, tol=0.02)
majorant = 1 / (2 * 3.3)          # I/(2fC) rapporté à V̂, avec RC = 3,3 T et I ≈ V̂/R
vrai(f"figure 4 : I/(2fC) = {majorant:.3f} majore l'ondulation simulée {1 - umin:.3f}", majorant > 1 - umin)
verifier("ΔU = 2/(2·50·10⁻³) (V)", 2 / (2 * 50 * 1e-3), 20)
verifier("autotest 5 : 325 − 20 (V)", 325 - 20, 305)

# ── P3 ──────────────────────────────────────────────────────────────────
ud3 = lambda t: max(fn(t) for fn in V3)
verifier("P3 : ⟨u_d⟩/V̂ = 3√3/(2π)", moy(ud3), 3 * sqrt(3) / (2 * pi))
verifier("P3 : ⟨u_d⟩/V ≈ 1,17", moy(ud3) * sqrt(2), 1.17, tol=0.002)
verifier("P3 : 1,17 × 230 (V)", moy(ud3) * sqrt(2) * 230, 269, tol=0.003)
ond3 = sqrt(eff(ud3) ** 2 - moy(ud3) ** 2) / moy(ud3)
verifier("P3 : taux d'ondulation (%)", ond3 * 100, 18, tol=0.03)
i1p3 = lambda t: 1.0 if max(range(3), key=lambda j: V3[j](t)) == 0 else 0.0
verifier("P3 : diode, courant moyen I_d/3", moy(i1p3), 1 / 3, tol=0.002)
verifier("P3 : diode, courant efficace I_d/√3", eff(i1p3), 1 / sqrt(3), tol=0.002)
vinv = max(V3[0](t) - V3[1](t) for t in range(360))   # D2 bloquée : −u12
verifier("P3 : tension inverse max / V = √6", vinv * sqrt(2), sqrt(6), tol=0.002)
verifier("P3 : √6 × 230 (V)", sqrt(6) * 230, 563, tol=0.002)
verifier("P3 : FP = (1,17 V I_d)/(3 V I_d/√3)", moy(ud3) * sqrt(2) / (3 * eff(i1p3)), 0.675, tol=0.003)
verifier("P3 : 3√2/(2π)", 3 * sqrt(2) / (2 * pi), 0.675, tol=0.002)
I1p3, phip3 = fondamental(i1p3)
vrai(f"P3 : fondamental en phase avec v1 ({phip3:.3f}°)", abs(phip3) < 0.05)
verifier("P3 : composante continue du courant de ligne", moy(i1p3), 1 / 3, tol=0.002)

# ── PD3 ─────────────────────────────────────────────────────────────────
ud6 = lambda t: max(fn(t) for fn in V3) - min(fn(t) for fn in V3)
Uc = sqrt(3)     # amplitude des composées pour V̂ = 1
verifier("PD3 : ⟨u_d⟩/Û = 3/π", moy(ud6) / Uc, 3 / pi)
verifier("PD3 : ⟨u_d⟩/Û ≈ 0,955", moy(ud6) / Uc, 0.955, tol=0.002)
verifier("PD3 : ⟨u_d⟩/U ≈ 1,35", moy(ud6) / Uc * sqrt(2), 1.35, tol=0.002)
verifier("PD3 : ⟨u_d⟩/V ≈ 2,34", moy(ud6) * sqrt(2), 2.34, tol=0.002)
verifier("PD3 : 1,35 × 400 (V)", 3 * sqrt(2) / pi * 400, 540, tol=0.002)
verifier("PD3 : 3√2/π × 400 (V)", 3 * sqrt(2) / pi * 400, 540.2, tol=0.0005)
verifier("PD3 : min/max de u_d = cos 30°", min(ud6(360 * k / N) for k in range(N)) / Uc, 0.866, tol=0.001)
verifier("PD3 : crête à crête / Û", 1 - cos(radians(30)), 0.134, tol=0.003)
verifier("PD3 : crête à crête / moyenne (%)", (1 - cos(radians(30))) / (3 / pi) * 100, 14, tol=0.01)
ond6 = sqrt(eff(ud6) ** 2 - moy(ud6) ** 2) / moy(ud6)
verifier("PD3 : taux d'ondulation (%)", ond6 * 100, 4.2, tol=0.01)
verifier("PD3 : √2 × 400 (V)", sqrt(2) * 400, 566, tol=0.002)
verifier("2023-E1 : 565 × cos 30° (V)", 565 * cos(radians(30)), 490, tol=0.002)
def i1pd3(t):
    j_max = max(range(3), key=lambda j: V3[j](t))
    j_min = min(range(3), key=lambda j: V3[j](t))
    return (1.0 if j_max == 0 else 0.0) - (1.0 if j_min == 0 else 0.0)
verifier("PD3 : courant de ligne efficace √(2/3)", eff(i1pd3), sqrt(2 / 3), tol=0.002)
verifier("PD3 : √(2/3)", sqrt(2 / 3), 0.816, tol=0.002)
I1p6, phip6 = fondamental(i1pd3)
verifier("PD3 : fondamental efficace √6/π", I1p6 / sqrt(2), sqrt(6) / pi, tol=0.002)
vrai(f"PD3 : fondamental en phase avec v1 ({phip6:.3f}°)", abs(phip6) < 0.05)
verifier("PD3 : FP = P/S", moy(ud6) * sqrt(2) / (3 * eff(i1pd3)), 0.955, tol=0.002)
verifier("PD3 : FP = 3/π", 3 / pi, 0.955, tol=0.002)
thd6 = sqrt((eff(i1pd3) / (I1p6 / sqrt(2))) ** 2 - 1)
verifier("PD3 : THD_i (%)", thd6 * 100, 31, tol=0.01)
verifier("PD3 : diode, courant moyen", moy(lambda t: max(i1pd3(t), 0)), 1 / 3, tol=0.002)
verifier("PD3 : diode, courant efficace", eff(lambda t: max(i1pd3(t), 0)), 1 / sqrt(3), tol=0.002)
verifier("méthode : I_d/3 pour 20 A", 20 / 3, 6.7, tol=0.005)
verifier("méthode : I_d/√3 pour 20 A", 20 / sqrt(3), 11.5, tol=0.005)
verifier("méthode : marge 1 200/566", 1200 / 566, 2.1, tol=0.01)

# ── Empiètement : aire L ω I_d par commutation (simulation) ────────────
# Commutation de la phase 1 vers la phase 2 (groupe du haut) : L di2/dt = (v2 − v1)/2 ·… on intègre
# v2 − v1 = 2 L ω di2/dθ jusqu'à i2 = I_d ; l'aire perdue vaut ∫ (v2 − v1)/2 dθ.
L, w, Id, Vh = 0.4e-3, 2 * pi * 50, 50.0, sqrt(2) * 400 / sqrt(3)
th0 = 150.0          # croisement de v1 et v2, θ en degrés
i2, aire, th, dth = 0.0, 0.0, th0, 1e-4
while i2 < Id:
    d = Vh * (S(th - 120) - S(th))     # v2 − v1
    i2 += d / (2 * L * w) * radians(dth)
    aire += d / 2 * radians(dth)
    th += dth
verifier("empiètement : aire perdue / (L ω I_d)", aire / (L * w * Id), 1.0, tol=0.003)
dU = 3 * L * w / pi * Id
verifier("empiètement : ΔU = 3 L ω I_d/π (V)", dU, 6.0, tol=0.005)
print(f"    empiètement : angle μ ≈ {th - th0:.2f}° (non publié)")

# ── Redresseurs commandés ──────────────────────────────────────────────
for al in (45, 60, 120):
    def udc(t, al=al):
        ph = (t - al) % 360
        return S(t) if ph < 180 else -S(t)
    verifier(f"PD2 tout thyristors : ⟨u_d⟩/U_d0 pour α = {al}°", moy(udc) / (2 / pi), cos(radians(al)), tol=0.002)
    i_al = lambda t, al=al: 1.0 if ((t - al) % 360) < 180 else -1.0
    _, ph1 = fondamental(i_al)
    verifier(f"PD2 tout thyristors : retard du fondamental pour α = {al}° (°)", -ph1, al, tol=0.002)
for al in (60, 120):
    def udm(t, al=al):
        ph = t % 180
        return abs(S(t)) if ph >= al else 0.0
    verifier(f"pont mixte : ⟨u_d⟩/U_d0 pour α = {al}°", moy(udm) / (2 / pi), (1 + cos(radians(al))) / 2, tol=0.002)
Um = 2 * sqrt(2) / pi * 230 * cos(radians(45))
verifier("méthode : 0,90 × 230 × cos 45° (V)", Um, 146.4, tol=0.002)
verifier("méthode : I_d (A)", Um / 10, 14.6, tol=0.003)
verifier("méthode : R I_d² (kW)", 10 * (Um / 10) ** 2 / 1e3, 2.14, tol=0.003)

# ── Exemple chiffré ────────────────────────────────────────────────────
Ud0 = 3 * sqrt(2) / pi * 400
verifier("ex. 1 : U_d0 (V)", Ud0, 540.2, tol=0.0005)
verifier("ex. 2 : cos α", 440 / Ud0, 0.815, tol=0.002)
al_n = degrees(acos(440 / Ud0))
verifier("ex. 2 : α (°)", al_n, 35.5, tol=0.003)
verifier("ex. 2 : E′ (V)", 440 - 0.4 * 50, 420)
verifier("ex. 3 : α avec empiètement (°)", degrees(acos(446 / Ud0)), 34.4, tol=0.003)
verifier("ex. 4 : courant moyen (A)", 50 / 3, 16.7, tol=0.003)
verifier("ex. 4 : courant efficace (A)", 50 / sqrt(3), 28.9, tol=0.003)
I = 50 * sqrt(2 / 3)
I1 = sqrt(6) / pi * 50
verifier("ex. 5 : I (A)", I, 40.8, tol=0.002)
verifier("ex. 5 : I1 (A)", I1, 39.0, tol=0.002)
P, Sv = 440 * 50, sqrt(3) * 400 * I
verifier("ex. 5 : S (kVA)", Sv / 1e3, 28.3, tol=0.002)
verifier("ex. 5 : FP", P / Sv, 0.778, tol=0.002)
verifier("ex. 5 : 0,955 cos α", 3 / pi * 440 / Ud0, 0.778, tol=0.002)
Q1 = P * tan(radians(al_n))
verifier("ex. 5 : tan α", tan(radians(al_n)), 0.713, tol=0.003)
verifier("ex. 5 : Q1 (kvar)", Q1 / 1e3, 15.7, tol=0.003)
D = sqrt(Sv ** 2 - P ** 2 - Q1 ** 2)
verifier("ex. 5 : D (kVA)", D / 1e3, 8.4, tol=0.01)
verifier("ex. 5 : D par √3 U I_H (kVA)", sqrt(3) * 400 * sqrt(I ** 2 - I1 ** 2) / 1e3, 8.4, tol=0.01)
verifier("ex. 6 : ⟨u_d⟩ (V)", -400 + 0.4 * 50, -380)
verifier("ex. 6 : cos α", -380 / Ud0, -0.703, tol=0.003)
verifier("ex. 6 : α (°)", degrees(acos(-380 / Ud0)), 134.7, tol=0.003)
verifier("ex. 6 : puissance renvoyée (kW)", 380 * 50 / 1e3, 19.0)
verifier("ex. 6 : puissance de la machine (kW)", 400 * 50 / 1e3, 20.0)
verifier("ex. 6 : pertes d'induit (kW)", 0.4 * 50 ** 2 / 1e3, 1.0)

# ── Corrections du tour 1 ──────────────────────────────────────────────
verifier("P3 : I1 efficace / I_d", I1p3 / sqrt(2), 0.390, tol=0.003)
verifier("P3 : I / I_d", eff(i1p3), 0.577, tol=0.002)
verifier("P3 : FP = I1/I", (I1p3 / sqrt(2)) / eff(i1p3), 0.675, tol=0.003)
vrai("P3 : la formule cos φ1/√(1 + THD²) sans I0 serait fausse",
     abs(1 / sqrt(1 + (sqrt(eff(i1p3) ** 2 - moy(i1p3) ** 2 - (I1p3 / sqrt(2)) ** 2) / (I1p3 / sqrt(2))) ** 2) - 0.675) > 0.05)
verifier("pont mixte à 60° : moyenne / U_d0", (1 + cos(radians(60))) / 2, 0.75)
verifier("ex. 6 : cos α avec empiètement", (-380 + 6.0) / Ud0, -0.692, tol=0.003)
verifier("ex. 6 : α avec empiètement (°)", degrees(acos((-380 + 6.0) / Ud0)), 133.8, tol=0.003)
verifier("ex. 6 : U_d0 cos α (V)", -380 + 6.0, -374)
verifier("Q1 = U_d0 I_d sin α = P tan α (ex. 5)", Ud0 * 50 * sin(radians(al_n)), P * tan(radians(al_n)), tol=0.003)

# ── Auto-test ──────────────────────────────────────────────────────────
verifier("Q2 : P3 sous 230 V (V)", 3 * sqrt(6) / (2 * pi) * 230, 269, tol=0.003)
verifier("Q3 : moyen (A)", 30 / 3, 10)
verifier("Q3 : efficace (A)", 30 / sqrt(3), 17.3, tol=0.003)
verifier("Q4 : P (W)", 207 * 10, 2070)
verifier("Q4 : I1 (A)", 4 / pi * 10 / sqrt(2), 9.0, tol=0.003)
verifier("Q4 : THD (%)", sqrt(1 / 0.81 - 1) * 100, 48, tol=0.01)
verifier("Q4 : contrôle FP", 1 / sqrt(1 + 0.483 ** 2), 0.90, tol=0.002)
verifier("Q6 : 207 cos 120° (V)", 207 * cos(radians(120)), -103.5)
verifier("Q6 : P (W)", 207 * cos(radians(120)) * 10, -1035)
verifier("Q6 : pont mixte (V)", 207 * (1 + cos(radians(120))) / 2, 52, tol=0.01)

print()
print("Aucun écart." if not ECARTS else f"{len(ECARTS)} écart(s) : {', '.join(ECARTS)}")
raise SystemExit(1 if ECARTS else 0)
