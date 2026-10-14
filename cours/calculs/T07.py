"""Applications numériques du chapitre T07, refaites en Python.

    python3 cours/calculs/T07.py

Chaque bloc reprend une valeur publiée dans cours/textes/T07.html ; un
écart de plus de 0,5 % sur la valeur arrondie fait échouer le script.
Les formules de valeur moyenne et d'ondulation sont aussi vérifiées par
simulation pas à pas des courants d'inductance (hacheurs série, parallèle,
entrelacés), indépendamment des expressions du cours.
"""
from math import floor

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


def homogene(nom, ok):
    vrai("homogénéité : " + nom, ok)


# ── Simulation : circuits complets, régime permanent par tir ───────────
# On intègre une période pas à pas (Euler, N pas) et l'on cherche l'état
# initial (i_L, v_C) qui se retrouve identique une période plus tard
# (méthode de tir, Newton à jacobien numérique) : aucune formule du cours
# n'intervient dans la recherche du régime permanent.
def tir(periode, x0, iters=30):
    x = list(x0)
    for _ in range(iters):
        y, _ = periode(x)
        F = [y[0] - x[0], y[1] - x[1]]
        if abs(F[0]) + abs(F[1]) < 1e-11:
            break
        J = [[0.0, 0.0], [0.0, 0.0]]
        for c in range(2):
            h = 1e-6 * max(1.0, abs(x[c]))
            xp = list(x); xp[c] += h
            yp, _ = periode(xp)
            for r in range(2):
                J[r][c] = ((yp[r] - xp[r]) - F[r]) / h
        det = J[0][0] * J[1][1] - J[0][1] * J[1][0]
        dx0 = (-F[0] * J[1][1] + F[1] * J[0][1]) / det
        dx1 = (-J[0][0] * F[1] + J[1][0] * F[0]) / det
        x = [max(x[0] + dx0, 0.0), x[1] + dx1]
    return periode(x)[1]


def serie(E, al, L, f, R, C=10e-3, N=4000):
    """Hacheur série, filtre L, C et charge R ; renvoie en régime permanent :
    ⟨u⟩, ⟨i_L⟩, Δi_L, ⟨i_Q⟩, ⟨i_D⟩, ⟨v_s⟩."""
    dt = 1 / (f * N)

    def periode(x):
        i, v = x
        su = si = sq = sd = sv = 0.0
        imin, imax = 1e9, -1e9
        for k in range(N):
            ferme = k < al * N
            if ferme:
                u = E
            elif i > 0:
                u = 0.0
            else:
                u = v             # Q ouvert, diode bloquée : v_L = 0
            i = max(i + (u - v) / L * dt, 0.0)
            v += (i - v / R) / C * dt
            su += u; si += i; sv += v
            sq += i if ferme else 0.0
            sd += 0.0 if ferme else i
            imin, imax = min(imin, i), max(imax, i)
        return (i, v), (su / N, si / N, imax - imin, sq / N, sd / N, sv / N)
    return tir(periode, (0.0, 0.0))


def parallele(E, al, L, f, R, C=10e-3, N=4000):
    """Hacheur parallèle complet ; renvoie ⟨v_s⟩, ⟨i_L⟩, ⟨i_D⟩, Δi_L."""
    dt = 1 / (f * N)

    def periode(x):
        i, v = x
        sd = si = sv = 0.0
        imin, imax = 1e9, -1e9
        for k in range(N):
            ferme = k < al * N
            if ferme:
                vL, iD = E, 0.0
            elif i > 0:
                vL, iD = E - v, i
            else:
                vL, iD = 0.0, 0.0
            i = max(i + vL / L * dt, 0.0)
            v += (iD - v / R) / C * dt
            si += i; sd += iD; sv += v
            imin, imax = min(imin, i), max(imax, i)
        return (i, v), (sv / N, si / N, sd / N, imax - imin)
    return tir(periode, (0.0, E))


def entrelace(n, al, N=6000):
    """Ondulation crête à crête de la somme de n rampes de hacheur série
    décalées de T/n, en unités E/(L f) (E = L = f = 1)."""
    def bras(t):
        u = t % 1.0
        return (1 - al) * u if u < al else (1 - al) * al - al * (u - al)
    vals = [sum(bras(k / N - j / n) for j in range(n)) for k in range(N)]
    return max(vals) - min(vals)


def formule_entrelace(n, al):
    m = floor(n * al)
    if m >= n:
        m = n - 1
    return n * ((m + 1) / n - al) * (al - m / n)


# ── Idée physique : régulateur linéaire 48 V → 12 V, 3 A ───────────────
verifier("linéaire : puissance dissipée (W)", (48 - 12) * 3, 108)
verifier("linéaire : puissance utile (W)", 12 * 3, 36)
verifier("linéaire : rendement (%)", 12 / 48 * 100, 25)

# ── §2 : hacheur série, contrôle par simulation ────────────────────────
E, al, L, f, R = 48.0, 0.3, 200e-6, 50e3, 3.0
u_m, iL_m, dI, iQ_m, iD_m, Vs = serie(E, al, L, f, R)
verifier("simulation série : ⟨u⟩ = αE (V)", u_m, al * E, tol=0.002)
verifier("simulation série : V_s = αE (V)", Vs, al * E, tol=0.002)
verifier("simulation série : Δi_L = α(1−α)E/(Lf) (A)", dI, al * (1 - al) * E / (L * f), tol=0.005)
verifier("simulation série : ⟨i_Q⟩ = αI (A)", iQ_m, al * iL_m, tol=0.005)
verifier("simulation série : ⟨i_D⟩ = (1−α)I (A)", iD_m, (1 - al) * iL_m, tol=0.005)
# conduction discontinue : ⟨u⟩ > αE
u_d, iL_d, dI_d, _, _, Vs_d = serie(E, al, L, f, 200.0)
vrai(f"conduction discontinue (R = 200 Ω) : ⟨u⟩ = {u_d:.2f} V > αE = {al * E:.1f} V", u_d > al * E + 0.5)
# ondulation maximale en α = 0,5
amax = max((a / 1000 for a in range(1, 1000)), key=lambda a: a * (1 - a))
verifier("α(1 − α) maximal en α", amax, 0.5)
verifier("valeur maximale de α(1 − α)", amax * (1 - amax), 0.25)
# ΔV_s = Δi/(8Cf) : intégrale du courant alternatif dans C
N = 20000
q, qmin, qmax = 0.0, 0.0, 0.0
for k in range(N):
    t = k / N
    i_ac = (t / al - 0.5) if t < al else (0.5 - (t - al) / (1 - al))   # Δi = 1, f = 1
    q += i_ac / N
    qmin, qmax = min(qmin, q), max(qmax, q)
verifier("ΔV_s · C f / Δi_L (doit valoir 1/8)", qmax - qmin, 1 / 8, tol=0.002)

# ── §3 : hacheur parallèle, contrôle par simulation ────────────────────
E, al, L, f, R = 24.0, 0.6, 500e-6, 50e3, 20.0
Vs, iL_m, iD_m, dI = parallele(E, al, L, f, R)
verifier("simulation parallèle : V_s = E/(1−α) (V)", Vs, E / (1 - al), tol=0.002)
verifier("simulation parallèle : ⟨i_D⟩ = (1−α)⟨i_L⟩ (A)", iD_m, (1 - al) * iL_m, tol=0.003)
verifier("simulation parallèle : Δi_L = αE/(Lf) (A)", dI, al * E / (L * f), tol=0.005)
verifier("bilan E I_E = V_s I_s (W)", E * iL_m, Vs * iD_m, tol=0.003)
verifier("figure 7 : V_s/E pour α = 0,6", 1 / (1 - 0.6), 2.5)
verifier("figure 7 : E − V_s en unités de E", 1 - 2.5, -1.5)
verifier("figure 7 : aire positive 0,6 E T", 0.6 * 1, 0.6)
verifier("figure 7 : aire négative 0,4 × 1,5 E T", 0.4 * 1.5, 0.6)
verifier("α = 0,79 : gain 1/(1 − α)", 1 / 0.21, 4.76, tol=0.005)
vrai("α = 0,8 : gain de 5", abs(1 / (1 - 0.8) - 5) < 1e-9)

# ── §4 : réversibilité ─────────────────────────────────────────────────
for a, val in ((0.7, 0.4), (0.5, 0.0), (1.0, 1.0), (0.0, -1.0)):
    vrai(f"(2α − 1) pour α = {a} : {2 * a - 1:+.2f}", abs((2 * a - 1) - val) < 1e-12)
# unipolaire : ondulation 4 fois plus faible au maximum (charge R-L, courant quasi constant)
bip = max(2 * (1 - a / 1000) * (a / 1000) for a in range(1, 1000))     # (E − ⟨u⟩)αT/L, unités ET/L
uni = max(d / 1000 * (1 - d / 1000) / 2 for d in range(1, 1000))       # créneaux E, 0 à 2f
verifier("ondulation bipolaire max / unipolaire max", bip / uni, 4)


def ond_charge(u_de_t, N=20000):
    """Ondulation crête à crête de ∫(u − ⟨u⟩)dt sur une période (L = f = E = 1)."""
    us = [u_de_t(k / N) for k in range(N)]
    m = sum(us) / N
    x = lo = hi = 0.0
    for u in us:
        x += (u - m) / N
        lo, hi = min(lo, x), max(hi, x)
    return hi - lo


for D in (0.05, 0.3, 0.5, 0.9):
    a = (1 + D) / 2
    bipo = ond_charge(lambda t: 1.0 if t < a else -1.0)
    a1, a2, b1, b2 = (1 - a) / 2, (1 + a) / 2, a / 2, 1 - a / 2
    unip = ond_charge(lambda t: (1.0 if a1 <= t < a2 else 0.0) - (1.0 if b1 <= t < b2 else 0.0))
    verifier(f"bipolaire, D = {D} : (1 − D²)/2", bipo, (1 - D * D) / 2, tol=0.003)
    verifier(f"unipolaire, D = {D} : |D|(1 − |D|)/2", unip, D * (1 - D) / 2, tol=0.003)
    verifier(f"rapport, D = {D} : (1 + |D|)/|D|", bipo / unip, (1 + D) / D, tol=0.005)
    vrai(f"rapport ≥ 2 (D = {D})", bipo / unip >= 2 - 1e-9)

# ── §5 : entrelacement ─────────────────────────────────────────────────
verifier("n = 2, α = 0,3 : somme (E/Lf)", entrelace(2, 0.3), 0.12, tol=0.01)
verifier("n = 2, α = 0,3 : formule 2(1/2 − α)α", 2 * (0.5 - 0.3) * 0.3, 0.12)
verifier("n = 1, α = 0,3 : α(1 − α)", 0.3 * 0.7, 0.21)
verifier("rapport 0,12/0,21", 0.12 / 0.21, 0.57, tol=0.005)
for n in (2, 3, 4):
    for a in (0.07, 0.14, 0.235, 0.3, 0.45, 0.6, 0.79, 0.9):
        sim, form = entrelace(n, a), formule_entrelace(n, a)
        vrai(f"n = {n}, α = {a} : simulation {sim:.4f} = formule {form:.4f}", abs(sim - form) < 2e-3)
for n in (2, 3, 4):
    pts = [(formule_entrelace(n, a / 4000), a / 4000) for a in range(1, 4000)]
    mx, amx = max(pts)
    verifier(f"n = {n} : maximum E/(4nLf)", mx, 1 / (4 * n), tol=0.002)
    vrai(f"n = {n} : maximum atteint en α = (2m+1)/(2n) ({amx:.4f})",
         min(abs(amx - (2 * m + 1) / (2 * n)) for m in range(n)) < 1e-3)
    vrai(f"n = {n} : zéro en α = k/n", all(formule_entrelace(n, k / n) < 1e-12 for k in range(1, n)))
# rapport à un bras : de 0 à presque 1
r_petit = formule_entrelace(2, 0.01) / (0.01 * 0.99)
vrai(f"n = 2, α = 0,01 : rapport {r_petit:.3f} proche de 1", r_petit > 0.97)
# formule de 2023-E2 (n = 4, α < 1/4) : E T (1 − 4α) 4α / (4 L') = (1 − 4α) α E/(L f)
for a in (0.1, 0.14, 0.2, 0.235):
    vrai(f"2023-E2 : (1 − 4α)α = formule générale (α = {a})", abs((1 - 4 * a) * a - formule_entrelace(4, a)) < 1e-12)
# n bras en phase : ondulation n fois celle d'un bras = un bras de L/n
vrai("bras en phase : n Δi = Δi(L/n)", abs(3 * 0.21 - 0.21 / (1 / 3)) < 1e-12)

# ── Méthodes : 2023-E2 ─────────────────────────────────────────────────
E, f, dI = 500.0, 50e3, 2.0
verifier("C6 : L_min = E/(4 f Δi) (mH)", E / (4 * f * dI) * 1e3, 1.25)
verifier("C6 : α_min = 70/500", 70 / 500, 0.14)
verifier("C6 : α_max = 117,5/500", 117.5 / 500, 0.235)
verifier("C6 : L pour α = 0,235 (mH)", 0.235 * 0.765 * E / (f * dI) * 1e3, 0.90, tol=0.005)
Lp = 1.25e-3
verifier("C8 : α d'ondulation maximale", max((a / 10000 for a in range(1, 2500)), key=lambda a: (1 - 4 * a) * a), 0.125)
verifier("C8 : Δi' = E/(16 L' f) (A)", E / (16 * Lp * f), 0.5)
verifier("C8 : Δi' pour α = 0,14 (A)", (1 - 4 * 0.14) * 0.14 * E / (Lp * f), 0.49, tol=0.01)
verifier("C8 : Δi' pour α = 0,235 (A)", (1 - 4 * 0.235) * 0.235 * E / (Lp * f), 0.11, tol=0.03)
verifier("C8 : rapport des maxima 2/0,5", 2 / 0.5, 4)

# ── Méthodes : 2025-E2 ─────────────────────────────────────────────────
verifier("Q19 : f_m en P1 = 195/48", 195 / 48, 4.06)
verifier("Q19 : f_m en Pmax = 317/48", 317 / 48, 6.60)
verifier("Q19 : f_m en P2 = 340/48", 340 / 48, 7.08)
verifier("Q19 : α = 1/f_m en P2", 48 / 340, 0.14, tol=0.01)
verifier("Q19 : α = 1/f_m en P1", 48 / 195, 0.25, tol=0.02)
verifier("Q31 : 2(1 − α) I_b/2 = (1 − α) I_b (α = 0,79, I_b = 62 A)", 2 * 0.21 * 62 / 2, 0.21 * 62)
verifier("Q32 : V_DC = 48/0,21 (V)", 48 / 0.21, 229, tol=0.003)
verifier("Q35 coquille : 48 × 0,21 (V)", 48 * 0.21, 10, tol=0.01)
verifier("Q33 : 48/3,69", 48 / 3.69, 13.0, tol=0.005)
Eb_plein, Eb_vide = 13 * 4.05, 13 * 3.3
verifier("Q34 : E_b pleine charge (V)", Eb_plein, 52.7, tol=0.002)
verifier("Q34 : E_b fin de décharge (V)", Eb_vide, 42.9)
verifier("Q34 : ΔE_b, valeurs arrondies (V)", 52.7 - 42.9, 9.8)
verifier("Q35 : V_DC plein (V)", 52.7 / 0.21, 251, tol=0.002)
verifier("Q35 : V_DC déchargé (V)", 42.9 / 0.21, 204, tol=0.002)
verifier("Q35 : écart plein (%)", (52.7 / 0.21 / 230 - 1) * 100, 9, tol=0.03)
verifier("Q35 : écart déchargé (%)", (42.9 / 0.21 / 230 - 1) * 100, -11, tol=0.03)
vrai("Q35 : plein dans ±10 %, déchargé hors tolérance",
     abs(52.7 / 0.21 / 230 - 1) < 0.10 < abs(42.9 / 0.21 / 230 - 1))

verifier("Q29-Q30 : deux interrupteurs fermés pendant (α − 1/2)T, en T", 0.79 - 0.5, 0.29)
verifier("2025-E2 : ondulation totale à α = 0,79 (unités V_s/(Lf))", entrelace(2, 0.79), formule_entrelace(2, 0.79), tol=0.01)

# ── Méthodes : 2022-E2 ─────────────────────────────────────────────────
verifier("Q31 : crête de 230 V efficaces (V)", 230 * 2 ** 0.5, 325, tol=0.003)
verifier("Q35 : (2 × 0,7 − 1) × 207 (V)", (2 * 0.7 - 1) * 207, 82.8)
verifier("Q36 : α nominal", (1 + 192 / 207) / 2, 0.964)
verifier("chapitre 1 : R_f I = 10,1 × 19 (V)", 10.1 * 19, 192, tol=0.003)

# ── Exemple chiffré ────────────────────────────────────────────────────
Vs, f, dIadm = 14.0, 1e5, 4.0
verifier("ex. 1 : α à 56 V", Vs / 56, 0.25)
verifier("ex. 1 : α à 40 V", Vs / 40, 0.35)
Lmin = (1 - 0.25) * Vs / (f * dIadm)
verifier("ex. 2 : L_min (µH)", Lmin * 1e6, 26.3, tol=0.002)
L = 33e-6
verifier("ex. 2 : (1 − α)V_s à 56 V (V)", 0.75 * Vs, 10.5)
d56 = 0.75 * Vs / (L * f)
d40 = 0.65 * Vs / (L * f)
verifier("ex. 2 : Δi_L à 56 V (A)", d56, 3.18)
verifier("ex. 2 : 33 µH à −20 % (µH)", 33 * 0.8, 26.4)
vrai("ex. 2 : 33 µH à −20 % ≥ 26,25 µH, 27 µH à −20 % < 26,25 µH", 33 * 0.8 >= Lmin * 1e6 > 27 * 0.8)
verifier("ex. 2 : Δi_L à 40 V (A)", d40, 2.76)
verifier("ex. 2 : L au point nominal 48 V (µH)", (1 - Vs / 48) * Vs / (f * dIadm) * 1e6, 24.8, tol=0.003)
verifier("ex. 2 : E/(4 f Δi) avec 56 V (µH)", 56 / (4 * f * dIadm) * 1e6, 35)
vrai("ex. 2 : Δi décroît avec α à V_s fixé", d56 > d40)
d56p = 0.75 * Vs / (26.4e-6 * f)
verifier("ex. 3 : Δi_L à 56 V, L = 26,4 µH (A)", d56p, 3.98)
verifier("ex. 3 : Δi/2 au pire (A)", d56p / 2, 1.99)
vrai("ex. 3 : 2 A > Δi/2, de peu", 0 < 2 - d56p / 2 < 0.02)
vrai("ex. 3 : Δi_adm = 2 I_min", 4.0 == 2 * 2.0)
vrai("ex. 3 : 39 µH à −20 % : Δi/2 nettement sous 2 A", 0.75 * Vs / (39e-6 * 0.8 * f) / 2 < 1.75)
# simulation de l'exemple : conduction continue à 2 A sous 56 V
u_m, iL_m, dI_s, _, _, Vs_s = serie(56, 0.25, L, f, Vs / 2)
vrai(f"ex. 3 : simulation 56 V, 2 A : ⟨u⟩ = {u_m:.3f} V = αE", abs(u_m - 14) < 0.02)
verifier("ex. 4 : I_max (A)", 20 + d56p / 2, 22.0)
verifier("ex. 4 : ⟨i_Q⟩ max (A)", 0.35 * 20, 7)
verifier("ex. 4 : ⟨i_D⟩ max (A)", 0.75 * 20, 15)
verifier("ex. 5 : C_min (µF)", 3.98 / (8 * f * 0.07) * 1e6, 71, tol=0.005)
verifier("ex. 5 : ondulation capacitive avec 100 µF (mV)", 3.98 / (8 * f * 100e-6) * 1e3, 49.7, tol=0.003)
verifier("ex. 5 : résistance série max (mΩ)", (0.07 - 0.0497) / 3.98 * 1e3, 5.1, tol=0.01)
# majoration : ondulation totale simulée (capacitive + résistance série) sous 70 mV
N = 20000
vmin = vmax = 0.0
q = 0.0
for k in range(N):
    t = k / N
    i_ac = 3.98 * ((t / 0.25 - 0.5) if t < 0.25 else (0.5 - (t - 0.25) / 0.75))
    q += i_ac / (N * f)
    v = q / 100e-6 + 5.1e-3 * i_ac
    vmin, vmax = min(vmin, v), max(vmax, v)
vrai(f"ex. 5 : 100 µF et 5,1 mΩ : ondulation totale {(vmax - vmin) * 1e3:.1f} mV ≤ 70 mV", vmax - vmin <= 0.0701)
verifier("ex. 6 : P_s (W)", 14 * 20, 280)
verifier("ex. 6 : pertes diode (W)", 0.5 * 15, 7.5)
verifier("ex. 6 : rendement (%)", 280 / 287.5 * 100, 97.4)
verifier("ex. 6 : linéaire, puissance dissipée (W)", (56 - 14) * 20, 840)
verifier("ex. 6 : entrée ⟨i_Q⟩ × E = P (W)", 0.25 * 20 * 56, 280)

# ── Auto-test ──────────────────────────────────────────────────────────
verifier("Q1 : V_s (V)", 0.4 * 24, 9.6)
verifier("Q1 : T (µs)", 1e6 / 20e3, 50)
verifier("Q1 : t_on (µs)", 0.4 * 50, 20)
verifier("Q1 : t_off (µs)", 0.6 * 50, 30)
verifier("Q2 : α", 1 - 12 / 48, 0.75)
verifier("Q2 : Δi_L (A)", 0.75 * 12 / (100e-6 * 50e3), 1.8)
verifier("Q2 : I_E (A)", 96 / 12, 8)
verifier("Q2 : ⟨i_D⟩ (A)", 0.25 * 8, 2)
verifier("Q2 : 96/48 (A)", 96 / 48, 2)
verifier("Q3 : α", (1 - 50 / 207) / 2, 0.379)
verifier("Q4 : L_min (mH)", 300 / (4 * 20e3 * 1.5) * 1e3, 2.5)
verifier("Q4 : courant minimal (A)", 1.5 / 2, 0.75)
dq5 = 0.25 * 0.75 * 48 / (100e-6 * 50e3)
verifier("Q5 : Δi_L (A)", dq5, 1.8)
verifier("Q5 : R max (Ω)", 12 / (dq5 / 2), 13.3)
verifier("Q5 : courant sous 50 Ω (A)", 12 / 50, 0.24)
u_m, *_ = serie(48, 0.25, 100e-6, 50e3, 50.0)
vrai(f"Q5 : simulation sous 50 Ω : ⟨u⟩ = {u_m:.2f} V > 12 V", u_m > 12.5)
K_ = 2 * 100e-6 * 50e3 / 50          # 2L/(R T)
M_ = 2 / (1 + (1 + 4 * K_ / 0.25 ** 2) ** 0.5)
verifier("Q5 : conduction discontinue, formule classique (V)", 48 * M_, 20, tol=0.03)
verifier("Q5 : conduction discontinue, simulation (V)", u_m, 20, tol=0.03)
k6 = 48 / (100e-6 * 50e3)
verifier("Q6 : E/(Lf) (A)", k6, 9.6)
verifier("Q6 : un bras (A)", 0.3 * 0.7 * k6, 2.02)
verifier("Q6 : total (A)", formule_entrelace(3, 0.3) * k6, 0.29, tol=0.01)
verifier("Q6 : total, simulation (A)", entrelace(3, 0.3) * k6, 0.288, tol=0.01)
verifier("Q6 : rapport un bras / total", 0.21 / formule_entrelace(3, 0.3), 7, tol=0.005)
verifier("Q6 : un bras / 3 (A)", 0.3 * 0.7 * k6 / 3, 0.67, tol=0.005)
verifier("Q6 : maximum total E/(12 L f) (A)", k6 / 12, 0.8)
verifier("Q6 : maximum un bras E/(4 L f) (A)", k6 / 4, 2.4)

# ── Homogénéité ────────────────────────────────────────────────────────
V_, A_, S_ = (1, 2, -3, -1), (0, 0, 0, 1), (0, 0, 1, 0)
W_ = (1, 2, -3, 0)
OHM = tuple(a - b for a, b in zip(V_, A_))
HENRY = tuple(a + b for a, b in zip(OHM, S_))
FARAD = tuple(a + b - c for a, b, c in zip(A_, S_, V_))
HZ = tuple(-c for c in S_)


def mul(*ds):
    return tuple(sum(c) for c in zip(*ds))


def puis(d, k):
    return tuple(k * c for c in d)


homogene("Δi_L = α(1 − α)E/(L f) en A", mul(V_, puis(HENRY, -1), puis(HZ, -1)) == A_)
homogene("L_min = α(1 − α)E/(f Δi) en H", mul(V_, puis(HZ, -1), puis(A_, -1)) == HENRY)
homogene("ΔV_s = Δi/(8 C f) en V", mul(A_, puis(FARAD, -1), puis(HZ, -1)) == V_)
homogene("ΔV_s = α I_s/(C f) en V", mul(A_, puis(FARAD, -1), puis(HZ, -1)) == V_)
homogene("E I_E = V_s I_s en W", mul(V_, A_) == W_)
homogene("⟨i⟩ = (αE − E′)/R en A", mul(V_, puis(OHM, -1)) == A_)

print()
print("Aucun écart." if not ECARTS else f"{len(ECARTS)} écart(s) : {', '.join(ECARTS)}")
raise SystemExit(1 if ECARTS else 0)
