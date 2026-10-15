"""Applications numériques du chapitre T19, refaites en Python.

    python3 cours/calculs/T19.py

Chaque bloc reprend une valeur publiée dans cours/textes/T19.html ; un
écart de plus de 0,5 % sur la valeur arrondie fait échouer le script.
Les montages linéaires sont résolus par analyse nodale avec un AOP de gain
fini A_d (sortie = A_d·ε), puis A_d → 10⁹ : les formules du cours en sont
la limite, indépendamment de leur démonstration. Les comparateurs sont
simulés pas à pas, sortie saturée.
"""
from math import sqrt, pi, log10, exp, asin, degrees

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


def resoudre(noeuds, branches, sources, aop, Ad=1e9):
    """Analyse nodale. noeuds : liste des nœuds inconnus. branches : (a, b, Y) admittance entre a et b
    ('0' = masse). sources : {nœud: potentiel imposé}. aop : liste de (plus, moins, sortie) ; la sortie
    est une source commandée v_s = Ad·(v+ − v−). Renvoie le dict des potentiels."""
    idx = {n: k for k, n in enumerate(noeuds)}
    N = len(noeuds)
    M = np.zeros((N, N), dtype=complex)
    b = np.zeros(N, dtype=complex)
    sorties = {s for _, _, s in aop}

    def pot(n):
        return ('src', sources[n]) if n in sources else (('masse', 0) if n == '0' else ('inc', idx[n]))
    for a, c, Y in branches:
        for x, y in ((a, c), (c, a)):
            if x in sources or x == '0' or x in sorties:
                continue
            i = idx[x]
            M[i, i] += Y
            t, v = pot(y)
            if t == 'inc':
                M[i, v] -= Y
            elif t == 'src':
                b[i] += Y * v
    for p, m, s in aop:
        i = idx[s]
        M[i, i] = 1
        for n, sg in ((p, -Ad), (m, Ad)):
            t, v = pot(n)
            if t == 'inc':
                M[i, v] += sg
            elif t == 'src':
                b[i] -= sg * v
    sol = np.linalg.solve(M, b)
    out = {n: sol[idx[n]] for n in noeuds}
    out.update(sources)
    return out


print("— §1, §2 Ordres de grandeur et contre-réaction")
Ad, Vsat = 2e5, 13.5
verifier("zone linéaire ≈ 70 µV (13,5 V / 2·10⁵)", Vsat / Ad, 70e-6, tol=0.04)
beta = 0.1
verifier("gain en boucle fermée ≈ 9,9995", Ad / (1 + beta * Ad), 9.9995, tol=1e-6)
verifier("ε = 50 µV pour 10 V en sortie", 10 / Ad, 50e-6)
verifier("bande passante gain 10 : 300 kHz", 3e6 / 10, 300e3)
verifier("bande passante gain 100 : 30 kHz", 3e6 / 100, 30e3)
verifier("inverseur −10 : gain de bruit 11, ≈ 270 kHz", 3e6 / 11, 270e3, tol=0.011)
verifier("vitesse de balayage : f max à 10 V ≈ 207 kHz", 13e6 / (2 * pi * 10), 207e3)

print("— §3 Inverseur, non inverseur, suiveur")
R1, R2 = 10e3, 47e3
v = resoudre(['m', 's'], [('e', 'm', 1 / R1), ('m', 's', 1 / R2)], {'e': 1.0}, [('0', 'm', 's')])
verifier("inverseur : vs/ve = −R2/R1", v['s'].real, -R2 / R1, tol=1e-6)
verifier("inverseur : v− ≈ 0 (masse virtuelle)", abs(v['m']) + 1, 1, tol=1e-6)
R1, R2 = 10e3, 100e3
v = resoudre(['m', 's'], [('m', '0', 1 / R1), ('m', 's', 1 / R2)], {'e': 1.0}, [('e', 'm', 's')])
verifier("non inverseur : vs/ve = 1 + R2/R1 = 11", v['s'].real, 11, tol=1e-6)
v = resoudre(['s'], [], {'e': 0.7}, [('e', 's', 's')])
verifier("suiveur : vs = ve", v['s'].real, 0.7, tol=1e-6)
verifier("capteur 1 V, 10 kΩ, sur 1 kΩ : 0,091 V", 1 * 1e3 / 11e3, 0.091, tol=0.005)

print("— §4 Millman, sommateur, soustracteur")
R = 1e3
v = resoudre(['p', 'm', 's'], [('v1', 'p', 1 / R), ('v2', 'p', 1 / R), ('m', '0', 1 / R), ('m', 's', 1 / R)],
             {'v1': 0.83, 'v2': 1.34}, [('p', 'm', 's')])
verifier("sommateur de décalage : vs = v1 + v2", v['s'].real, 0.83 + 1.34, tol=1e-6)
verifier("… v+ = (v1 + v2)/2", v['p'].real, (0.83 + 1.34) / 2, tol=1e-6)
R1, R2 = 1e3, 10e3


def soustracteur(v1, v2, R3=R1, R4=R2):
    v = resoudre(['m', 'p', 's'], [('v1', 'm', 1 / R1), ('m', 's', 1 / R2), ('v2', 'p', 1 / R3), ('p', '0', 1 / R4)],
                 {'v1': v1, 'v2': v2}, [('p', 'm', 's')])
    return v['s'].real


verifier("soustracteur : 10 × (2,05 − 2,00) = 0,50 V", soustracteur(2.00, 2.05), 0.50, tol=1e-6)
verifier("R4 à +1 % : mode commun de 2 V → +18 mV", soustracteur(2.0, 2.0, R4=1.01 * R2), 0.018, tol=0.02)
verifier("R4 à +1 % : vs ≈ 0,518 V", soustracteur(2.00, 2.05, R4=1.01 * R2), 0.518, tol=0.002)
verifier("… erreur ≈ 3,7 %", (soustracteur(2.00, 2.05, R4=1.01 * R2) - 0.5) / 0.5, 0.037, tol=0.01)

print("— §5 Amplificateur d'instrumentation (2024-E2)")
# 2025-E1 Q59, notre lecture de sa figure 31 : 120 Ω à 0 N, 120,0172 Ω à 15 000 N
R0, KR = 120.0, 0.0172 / 15000
verifier("2025-E1 : K_R ≈ 1,147·10⁻⁶ Ω/N", KR, 1.147e-6, tol=0.0005)
F = 1380 * 9.81
verifier("2025-E1 : F ≈ 13 540 N", F, 13540, tol=0.001)
dR = KR * F
verifier("2025-E1 : ΔR ≈ 0,0155 Ω", dR, 0.0155, tol=0.005)
vab = 1 / 2 * dR / (2 * R0 + dR)
verifier("2025-E1 : V_A − V_B ≈ 32 µV (expression exacte de Q57)", vab, 32e-6, tol=0.012)
verifier("2025-E1 : K_A ≈ 1,55·10⁵", 5 / vab, 1.55e5, tol=0.005)
R1, R2 = 1e3, 834.4


def instru(vA, vB, R1a=R1, R1b=R1):
    v = resoudre(['x', 'y', 'o1', 'o2'], [('o1', 'x', 1 / R1a), ('x', 'y', 1 / R2), ('y', 'o2', 1 / R1b)],
                 {'A': vA, 'B': vB}, [('A', 'x', 'o1'), ('B', 'y', 'o2')])
    return v


v = instru(1.010, 1.000)
verifier("V_R2 = e_AB", (v['x'] - v['y']).real, 0.010, tol=1e-6)
G1 = 1 + 2 * R1 / R2
verifier("G1 = 1 + 2R1/R2 ≈ 3,397", G1, 3.397, tol=0.0005)
verifier("circuit : V1/e_AB = G1", ((v['o1'] - v['o2']) / 0.010).real, G1, tol=1e-6)
v2 = instru(3.010, 3.000, R1a=1.02e3, R1b=0.98e3)
v3 = instru(1.010, 1.000, R1a=1.02e3, R1b=0.98e3)
vrai("mode commun sans effet sur V1, même R1 inégales",
     abs((v2['o1'] - v2['o2']) - (v3['o1'] - v3['o2'])) < 1e-6)
verifier("V3 = G1·G2·G3·e_AB ≈ 339,7 e_AB", G1 * (-100) * (-1), 339.7, tol=0.0005)
verifier("écart au 337,7 du sujet ≈ 0,6 %", (G1 * 100 - 337.7) / 337.7, 0.006, tol=0.1)
verifier("droite idéale 1–5 V : pente 4/11,8 mV ≈ 339", 4 / 11.8e-3, 339, tol=0.002)
verifier("… décalage ≈ 1,34 V", 1 + 4 / 11.8e-3 * 1e-3, 1.34, tol=0.002)
verifier("E5 : V4(−1 mV) ≈ 1,00 V", 337.7 * -1e-3 + 1.34, 1.00, tol=0.005)
verifier("E5 : V4(10,8 mV) ≈ 4,99 V", 337.7 * 10.8e-3 + 1.34, 4.99, tol=0.002)

print("— §6 Intégrateur et dérivateur")
R, C = 10e3, 100e-9
for w in (100.0, 1 / (R * C), 1e5):
    Y = 1j * w * C
    v = resoudre(['m', 's'], [('e', 'm', 1 / R), ('m', 's', Y)], {'e': 1.0}, [('0', 'm', 's')])
    vrai(f"intégrateur : H = −1/(jRCω), ω = {w:g}", abs(v['s'] - (-1 / (1j * R * C * w))) < 1e-5 * abs(v['s']))
    v = resoudre(['m', 's'], [('e', 'm', Y), ('m', 's', 1 / R)], {'e': 1.0}, [('0', 'm', 's')])
    vrai(f"dérivateur : H = −jRCω, ω = {w:g}", abs(v['s'] - (-1j * R * C * w)) < 1e-5 * abs(v['s']))
verifier("intégrateur : phase +90°", degrees(np.angle(-1 / (1j * R * C * 500))), 90)
verifier("dérivateur : phase −90°", degrees(np.angle(-1j * R * C * 500)), -90)
verifier("intégrateur : |H(1/RC)| = 1, 0 dB", abs(-1 / (1j * R * C * (1 / (R * C)))), 1.0, tol=1e-9)
E, Tp = 1.0, 2e-3
verifier("triangle : amplitude crête à crête E·T/(2RC)", E * Tp / (2 * R * C), 1.0, tol=1e-9)
# Créneau → triangle, par intégration numérique
t = np.linspace(0, 3 * Tp, 30001)
ve = np.where((t % Tp) < Tp / 2, E, -E)
vs = -np.cumsum(ve) * (t[1] - t[0]) / (R * C)
verifier("simulation : crête à crête du triangle", vs.max() - vs.min(), E * Tp / (2 * R * C), tol=0.002)
Rp = 1e6
w = 2 * pi * 10
H = -(Rp / R) / (1 + 1j * Rp * C * w)
v = resoudre(['m', 's'], [('e', 'm', 1 / R), ('m', 's', 1 / Rp + 1j * w * C)], {'e': 1.0}, [('0', 'm', 's')])
vrai("pseudo-intégrateur : H = −(Rp/R)/(1 + jRpCω)", abs(v['s'] - H) < 1e-5 * abs(H))

print("— §7 Filtres actifs")
R1, R2, Cf = 1e3, 10e3, 10e-9
for w in (1e3, 1 / (R2 * Cf), 1e6):
    v = resoudre(['m', 's'], [('e', 'm', 1 / R1), ('m', 's', 1 / R2 + 1j * w * Cf)], {'e': 1.0}, [('0', 'm', 's')])
    vrai(f"premier ordre actif, ω = {w:g}", abs(v['s'] - (-(R2 / R1) / (1 + 1j * R2 * Cf * w))) < 1e-5 * abs(v['s']))


def sallen_key(Ra, Rb, C1, C2, w):
    v = resoudre(['M', 'P', 's'], [('e', 'M', 1 / Ra), ('M', 'P', 1 / Rb), ('M', 's', 1j * w * C1), ('P', '0', 1j * w * C2)],
                 {'e': 1.0}, [('P', 's', 's')])
    return v['s']


R, C1, C2 = 3.75e3, 20e-9, 10e-9
for w in (2e3, 2e4, 2e5):
    canon = 1 / (1 + (2 * R) * C2 * 1j * w + R * R * C1 * C2 * (1j * w) ** 2)
    vrai(f"Sallen et Key : forme canonique, ω = {w:g}", abs(sallen_key(R, R, C1, C2, w) - canon) < 1e-5)
verifier("Sallen et Key : m = √(C2/C1) = 0,707", sqrt(C2 / C1), 0.7071, tol=0.0005)
Rsk = 1 / (2 * pi * 3000 * sqrt(C1 * C2))
verifier("R pour f0 = 3 kHz ≈ 3,75 kΩ", Rsk, 3.75e3, tol=0.002)
w0 = 1 / (Rsk * sqrt(C1 * C2))
verifier("Sallen et Key : |H(ω0)| = 1/(2m) ≈ 0,707", abs(sallen_key(Rsk, Rsk, C1, C2, w0)), 0.7071, tol=0.001)
ws = np.logspace(2, 6, 4000)
gmax = max(abs(sallen_key(Rsk, Rsk, C1, C2, w)) for w in ws[::40])
vrai("Butterworth : pas de bosse (gain ≤ 1)", gmax <= 1 + 1e-6)

print("— §8 Comparateurs")


def trigger_inverseur(ve, R1, R2, Vref, Vsat):
    """Simulation pas à pas : renvoie la sortie et les deux abscisses de bascule."""
    vs, sorties, bascules = Vsat, [], []
    for x in ve:
        vp = (R2 * Vref + R1 * vs) / (R1 + R2)
        nouveau = Vsat if vp - x > 0 else -Vsat
        if nouveau != vs:
            bascules.append((x, nouveau))
        vs = nouveau
        sorties.append(vs)
    return np.array(sorties), bascules


R1, R2, Vref, Vsat = 1e3, 150e3, 2.42, 15
VH = (R2 * Vref + R1 * Vsat) / (R1 + R2)
VB = (R2 * Vref - R1 * Vsat) / (R1 + R2)
verifier("2023-E2 : V_H = 378/151 ≈ 2,503 V", VH, 2.503, tol=0.0005)
verifier("2023-E2 : V_B = 348/151 ≈ 2,305 V", VB, 2.305, tol=0.0005)
ve = np.concatenate([np.linspace(0, 5, 50001), np.linspace(5, 0, 50001)])
s, b = trigger_inverseur(ve, R1, R2, Vref, Vsat)
verifier("simulation : bascule vers −Vsat à V_H", b[0][0], VH, tol=0.0005)
vrai("… vers −Vsat en montant", b[0][1] == -Vsat)
verifier("simulation : retour vers +Vsat à V_B", b[1][0], VB, tol=0.0005)
verifier("seuils en pente : 25,0 %", VH / 0.1, 25.0, tol=0.002)
verifier("… 23,0 %", VB / 0.1, 23.0, tol=0.003)
verifier("largeur 2R1Vsat/(R1 + R2)", VH - VB, 2 * R1 * Vsat / (R1 + R2), tol=1e-9)
verifier("F10 : basculement à 25,03 %", VH / 0.1, 25.03, tol=0.0002)
verifier("F10 : retour à 23,05 %", VB / 0.1, 23.05, tol=0.0002)
verifier("F10 : ±0,005 V sur Vref2 → ±0,05 point", 0.005 * R2 / (R1 + R2) / 0.1, 0.05, tol=0.01)
verifier("F10 : Vref2 = 2,415 V → 24,98 %", (R2 * 2.415 + R1 * Vsat) / (R1 + R2) / 0.1, 24.98, tol=0.0002)
verifier("F10 : Vref2 = 2,415 V → 23,00 %", (R2 * 2.415 - R1 * Vsat) / (R1 + R2) / 0.1, 23.00, tol=0.0002)


def trigger_non_inverseur(ve, R1, R2, Vref, Vsat):
    vs, bascules = -Vsat, []
    for x in ve:
        vp = (R2 * x + R1 * vs) / (R1 + R2)
        nouveau = Vsat if vp - Vref > 0 else -Vsat
        if nouveau != vs:
            bascules.append((x, nouveau))
        vs = nouveau
    return bascules


b = trigger_non_inverseur(np.concatenate([np.linspace(-3, 3, 60001), np.linspace(3, -3, 60001)]), 1e3, 10e3, 0, 12)
verifier("non inverseur, Vref = 0 : seuil haut +(R1/R2)Vsat", b[0][0], 1.2, tol=0.001)
vrai("… sortie à +Vsat au-dessus du seuil haut", b[0][1] == 12)
verifier("non inverseur : seuil bas −(R1/R2)Vsat", b[1][0], -1.2, tol=0.001)

print("— §9 Conversion tension-courant")
Rref, Rch, Ve = 250, 300, 3.0
v = resoudre(['m', 's'], [('m', '0', 1 / Rref), ('m', 's', 1 / Rch)], {'e': Ve}, [('e', 'm', 's')])
Is = ((v['s'] - v['m']) / Rch).real
verifier("charge flottante : Is = Ve/Rref", Is, Ve / Rref, tol=1e-6)
verifier("… vs = (Rref + Rch)·Is", v['s'].real, (Rref + Rch) * Is, tol=1e-6)


def howland(V4, Rana, R=250.0, Ad=1e9):
    v = resoudre(['m', 'A', 's'], [('m', '0', 1 / R), ('m', 's', 1 / R), ('V4', 'A', 1 / R), ('A', 's', 1 / R), ('A', '0', 1 / Rana)],
                 {'V4': V4}, [('A', 'm', 's')], Ad=Ad)
    return v


for Rana in (100, 250, 500):
    v = howland(5.0, Rana)
    verifier(f"Howland : Is = V4/R, R_ana = {Rana} Ω", (v['A'] / Rana).real, 0.020, tol=1e-6)
    verifier(f"… vs = 2·R_ana·Is, R_ana = {Rana} Ω", v['s'].real, 2 * Rana * 0.020, tol=1e-6)
verifier("E10 : 1 V → 4 mA", (howland(1.0, 250)['A'] / 250).real, 4e-3, tol=1e-6)
verifier("E10 : 5 V → 20 mA", (howland(5.0, 250)['A'] / 250).real, 20e-3, tol=1e-6)
verifier("500 Ω à 20 mA : sortie à 20 V", 2 * 500 * 0.02, 20)
# Résistances inégales : le courant dépend alors de la charge
v1 = resoudre(['m', 'A', 's'], [('m', '0', 1 / 250), ('m', 's', 1 / 252.5), ('V4', 'A', 1 / 250), ('A', 's', 1 / 250), ('A', '0', 1 / 100)],
              {'V4': 5.0}, [('A', 'm', 's')])
v2 = resoudre(['m', 'A', 's'], [('m', '0', 1 / 250), ('m', 's', 1 / 252.5), ('V4', 'A', 1 / 250), ('A', 's', 1 / 250), ('A', '0', 1 / 500)],
              {'V4': 5.0}, [('A', 'm', 's')])
vrai("Howland à résistances inégales : Is dépend de la charge", abs(v1['A'] / 100 - v2['A'] / 500) > 1e-5)

# Régime du Howland : fractions de retour vers chaque entrée
for Rana in (100, 500, 1e9):
    par = 250 * Rana / (250 + Rana)
    bp, bm = par / (250 + par), 0.5
    vrai(f"Howland : retour sur + ({bp:.3f}) < retour sur − (0,5), R_ana = {Rana:g} Ω", bp < bm or Rana > 1e8)
# Courant fourni par la sortie de l'AOP et courant de la source V4
for Rana, i_attendu, i2_attendu in ((250, 0.040, 0.0), (500, 0.080, -0.020)):
    v = howland(5.0, Rana)
    i_s = ((v['s'] - v['A']) / 250 + (v['s'] - v['m']) / 250).real
    verifier(f"Howland : courant de sortie de l'AOP = 2·vA/R, R_ana = {Rana} Ω", i_s, i_attendu, tol=1e-6)
    vrai(f"… I2 = (V4 − vA)/R = {i2_attendu * 1e3:g} mA, R_ana = {Rana} Ω", abs(((5.0 - v['A']) / 250).real - i2_attendu) < 1e-6)

print("— Exemple : alarme de température")
verifier("gain 0,1/0,01 = 10", 0.1 / 0.01, 10)
verifier("R1 = 2,0 kΩ, R2 = 18 kΩ : gain 10", 1 + 18 / 2.0, 10)
verifier("seuils voulus : largeur 0,30 V", 3.50 - 3.20, 0.30)
verifier("R3/R4 = 0,30/22 ≈ 0,0136", 0.30 / 22, 0.0136, tol=0.003)
verifier("R4 ≈ 73,3 R3", 22 / 0.30, 73.3, tol=0.001)
verifier("largeur avec 1,0 et 75 kΩ ≈ 0,293 V", 2 * 11 / 75, 0.293, tol=0.002)
verifier("Vref voulue ≈ 3,306 V", 3.35 / (1 + 1 / 75), 3.306, tol=0.0005)
Vref = 5 * 10 / 15.1
verifier("diviseur 5,1 et 10 kΩ : 3,311 V", Vref, 3.311, tol=0.0005)
verifier("centre ≈ 3,355 V", Vref * (1 + 1 / 75), 3.355, tol=0.0005)
verifier("demi-largeur ≈ 0,147 V", 11 / 75, 0.147, tol=0.003)
b = trigger_non_inverseur(np.concatenate([np.linspace(3.0, 3.8, 80001), np.linspace(3.8, 3.0, 80001)]), 1e3, 75e3, Vref, 11)
verifier("simulation : V_H ≈ 3,502 V", b[0][0], 3.502, tol=0.0005)
verifier("simulation : V_B ≈ 3,209 V", b[1][0], 3.209, tol=0.0005)
verifier("… soit 35,0 °C", b[0][0] / 0.1, 35.0, tol=0.002)
verifier("… et 32,1 °C", b[1][0] / 0.1, 32.1, tol=0.002)
verifier("courant tiré par le trigger ≈ 0,19 mA", (11 + 3.5) / 76e3, 0.19e-3, tol=0.01)
verifier("bande passante du gain 10 : 300 kHz", 3e6 / 10, 300e3)

print("— Auto-test")
verifier("Q1 : amplitude 2,35 V", 4.7 * 0.5, 2.35)
verifier("Q1 : entrée max 2,87 V", 13.5 / 4.7, 2.87, tol=0.002)
verifier("Q2 : gain 11", 1 + 100 / 10, 11)
verifier("Q2 : bande 0,27 MHz", 3e6 / 11, 0.27e6, tol=0.012)
verifier("Q2 : 207 kHz", 13e6 / (2 * pi * 10), 207e3, tol=0.002)
verifier("Q4 : pente −1 000 V/s", -1 / (10e3 * 100e-9), -1000)
verifier("Q4 : saturation à 13,5 ms", 13.5 / 1000, 13.5e-3)
verifier("Q5 : seuils ±1,09 V", 12 / 11, 1.09, tol=0.002)
verifier("Q5 : bascule à 33° après le zéro", degrees(asin((12 / 11) / 2)), 33, tol=0.01)
verifier("Q6 : charge max 425 Ω", 13.5 / 0.02 - 250, 425)

print()
print("Aucun écart." if not ECARTS else f"{len(ECARTS)} écart(s) : " + " ; ".join(ECARTS))
raise SystemExit(1 if ECARTS else 0)
