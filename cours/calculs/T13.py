"""Applications numériques du chapitre T13, refaites en Python.

    python3 cours/calculs/T13.py

Chaque bloc reprend une valeur publiée dans cours/textes/T13.html ; un
écart de plus de 0,5 % sur la valeur arrondie fait échouer le script.
Le modèle de la machine d'exemple (figures 3, 7, 8, 9) est recalculé, et
les démarrages sont simulés (Euler, pas fin).
"""
import json
from collections import Counter
from math import sqrt, pi, hypot

RACINE = __import__("pathlib").Path(__file__).resolve().parents[2]
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


def bissection(fn, a, b, n=200):
    fa = fn(a)
    for _ in range(n):
        m = (a + b) / 2
        fm = fn(m)
        if (fm > 0) == (fa > 0):
            a, fa = m, fm
        else:
            b = m
    return (a + b) / 2


print("── En bref : fréquence et relevé")
cartes = json.loads((RACINE / "cards.json").read_text())
th = next(t for t in cartes["themes"] if t["code"] == "T13")
verifier("présence dans les sujets (cartes)", th["presence_n"], 7)
releve = json.loads((RACINE / "cours/releve-sujets.json").read_text())
qs = [(e["id"], q) for e in releve["epreuves"] for q in e["questions"] if "T13" in q["themes"]]
verifier("questions mobilisant T13", len(qs), 37)
verifier("épreuves", len({e for e, _ in qs}), 8)
verifier("questions en thème principal", sum(1 for _, q in qs if q["themes"][0] == "T13"), 23)
formes = Counter(q.get("forme") for _, q in qs)
verifier("forme calcul", formes["calcul"], 12)
verifier("forme conclure/valider", formes["conclure/valider"], 9)
cites = {("2024-E2", q) for q in ("A3", "A4", "A5", "A6", "A7", "A8", "C1", "C2", "D15", "D16", "D17")}
cites |= {("2021-E1", q) for q in ("13", "16", "17", "18", "19", "20")} | {("2023-E1", "18"), ("2023-E1", "19")}
cites |= {("2025-E1", "54"), ("2017-E1", "8"), ("2015-E1", "19")}
vrai("questions citées en bref : toutes au relevé", cites <= {(e, q["q"]) for e, q in qs})
n_f = sum(1 for c in cartes["cards"] if c.get("theme") == "T13" and c["type"] == "formule")
n_p = sum(1 for c in cartes["cards"] if c.get("theme") == "T13" and c["type"] == "piege")
verifier("cartes : formules", n_f, 17)
verifier("cartes : pièges", n_p, 7)

print("── §1-§2 : synchronisme et glissement")
for p, Ns in ((1, 3000), (2, 1500), (3, 1000), (4, 750)):
    verifier(f"N_s pour p = {p}", 60 * 50 / p, Ns, tol=1e-9)
verifier("400/√3", 400 / sqrt(3), 230, tol=0.005)
verifier("f_r à g = 3 %", 0.03 * 50, 1.5, tol=1e-9)
verifier("60f/N à 1 455 tr/min", 3000 / 1455, 2.06, tol=0.002)
verifier("g à 1 455 tr/min", (1500 - 1455) / 1500, 0.03, tol=1e-9)
vrai("p = partie entière de 60f/N, y compris à fort glissement (8 pôles, 660 tr/min)",
     int(3000 / 660) == 4 and round(3000 / 660) == 5)
verifier("borne η < 1 − g à 5 %", 1 - 0.05, 0.95, tol=1e-9)

print("── Machine d'exemple : bilan nominal (§4, exemple 1-2)")
U = 400.0; V = U / sqrt(3); f = 50.0; p = 2; ws = 2 * pi * f; OMs = ws / p
N = 1460.0; g = (1500 - N) / 1500; W = 2 * pi * N / 60
I = 21.0; cphi = 0.83; Rmes = 0.60; Rs = Rmes / 2; PFs = 250.0; Ppm = 150.0
Pa = sqrt(3) * U * I * cphi; PJs = 1.5 * Rmes * I ** 2
Pt = Pa - PJs - PFs; PJr = g * Pt; Pm = (1 - g) * Pt; Pu = Pm - Ppm
verifier("V_s", V, 231, tol=0.001)
verifier("60f/N", 3000 / N, 2.05, tol=0.003)
verifier("g", g, 0.0267, tol=0.002)
verifier("f_r", g * f, 1.33, tol=0.003)
verifier("Ω_s", OMs, 157.08, tol=1e-4)
verifier("Ω", W, 152.89, tol=1e-4)
verifier("P_a", Pa, 12076, tol=0.0005)
verifier("P_Js", PJs, 397, tol=0.002)
verifier("P_Js = 3 R_s I²", 3 * Rs * I ** 2, 397, tol=0.002)
verifier("P_t", Pt, 11429, tol=0.0005)
verifier("P_Jr", PJr, 305, tol=0.002)
verifier("P_méca", Pm, 11124, tol=0.0005)
verifier("P_u", Pu, 10974, tol=0.0005)
verifier("η", Pu / Pa, 0.909, tol=0.001)
verifier("1 − g", 1 - g, 0.973, tol=0.001)
Cem = Pt / OMs; Cu = Pu / W; Cp = Ppm / W
verifier("C_em", Cem, 72.8, tol=0.002)
verifier("C_em = P_méca/Ω", Pm / W, 72.8, tol=0.002)
verifier("C_u", Cu, 71.8, tol=0.002)
verifier("C_p", Cp, 0.98, tol=0.005)
verifier("P_Jr/P_t (exemple 6)", PJr / Pt, 0.027, tol=0.02)
verifier("P_Js/P_a (exemple 6)", PJs / Pa, 0.033, tol=0.01)

print("── Exemple 3 : modèle")
Rr = 0.36; Lf = 8e-3; X = Lf * ws; r = Rr / g


def C_em(gl, Vs=V, w=ws):
    Xw = Lf * w
    return 3 * p * Vs ** 2 * (Rr / gl) / (w * ((Rr / gl) ** 2 + Xw ** 2))


verifier("R'_r/g", r, 13.5, tol=1e-6)
verifier("L_f ω_s", X, 2.51, tol=0.002)
Ir = V / hypot(r, X)
verifier("I'_r nominal", Ir, 16.8, tol=0.002)
verifier("P_t du modèle", 3 * r * Ir ** 2, 11455, tol=0.0005)
verifier("écart modèle / bilan (%)", (3 * r * Ir ** 2 - Pt) / Pt * 100, 0.2, tol=0.15)
verifier("R'_r par la formule linéarisée", 3 * V ** 2 * g / Pt, 0.373, tol=0.002)
verifier("… soit 4 % de trop", (3 * V ** 2 * g / Pt - Rr) / Rr * 100, 4, tol=0.1)
gmax = Rr / X
verifier("g/g_max nominal", g / gmax, 0.19, tol=0.03)
# courant de ligne : la différence I_s − I'_r est le courant magnétisant
vrai("I'_r < I_s", Ir < I)

print("── Exemple 4 et §5 : couple maximal, démarrage")
Cmax = 3 * p / (2 * Lf) * (V / ws) ** 2
verifier("g_max", gmax, 0.143, tol=0.002)
verifier("vitesse au couple maximal (tr/min)", 1500 * (1 - gmax), 1285, tol=0.001)
verifier("C_max", Cmax, 203, tol=0.003)
verifier("C_max par la forme complète", C_em(gmax), 203, tol=0.003)
verifier("C_max/C_u nominal", Cmax / Cu, 2.8, tol=0.01)
verifier("forme de Kloss = forme complète (g = 0,05)", 2 * Cmax / (0.05 / gmax + gmax / 0.05), C_em(0.05), tol=1e-9)
verifier("linéarisation 2 C_max g/g_max = 3pV²g/(R'ω)", 2 * Cmax / gmax, 3 * p * V ** 2 / (Rr * ws), tol=1e-9)
Id = V / hypot(Rr, X); Cd = C_em(1.0)
verifier("I'_r au démarrage", Id, 91, tol=0.003)
verifier("I_d/I_n", Id / I, 4.3, tol=0.01)
verifier("C_d", Cd, 57, tol=0.005)
verifier("C_d/C_n", Cd / Cu, 0.79, tol=0.005)
verifier("A (exemple 5)", 3 * p / Rr * (V / ws) ** 2, 9.01, tol=0.001)

print("── Figure 7 : points A, B, P")
gA = bissection(lambda x: C_em(x) - 120, 1e-5, gmax)
gB = bissection(lambda x: C_em(x) - 120, gmax, 1.0)
vrai(f"A sur la partie stable (g = {gA:.4f} < g_max)", gA < gmax)
vrai(f"B sur la partie instable (g = {gB:.4f} > g_max)", gB > gmax)
vrai("C_d < 120 N·m : pas de démarrage sous ce couple", Cd < 120)
vrai("ventilateur : coupe la courbe au point nominal (C_em nominal)", abs(C_em(g) - 72.76) / 72.76 < 0.01)
verifier("chute de tension de 10 % : perte de couple (%)", (1 - 0.9 ** 2) * 100, 19, tol=0.001)

print("── Figure 8 : étoile-triangle")
RF = 3 * V ** 2 / PFs; XM = 26.8


def i_ligne(gl, Vs=V):
    zr = complex(Rr / gl, X)
    zm = 1 / (1 / RF + 1 / complex(0, XM))
    return abs(Vs / zr + Vs / zm)


verifier("courant de ligne nominal du modèle (A)", i_ligne(g), 21, tol=0.03)
verifier("L_M = X_M/ω (mH)", XM / ws * 1e3, 85, tol=0.005)
verifier("courant de démarrage en triangle / I_n", i_ligne(1.0) / I, 4.7, tol=0.01)
# en étoile, l'enroulement du moteur triangle reçoit U/√3 : vu du schéma étoile équivalent,
# ses impédances sont multipliées par 3 sous la même tension simple
zr1 = complex(Rr, X); zm = 1 / (1 / RF + 1 / complex(0, XM))
verifier("rapport étoile/triangle (courant)", abs(V / (3 * zr1) + V / (3 * zm)) / abs(V / zr1 + V / zm), 1 / 3, tol=1e-9)
verifier("rapport étoile/triangle (couple)", (3 * V ** 2 * (3 * Rr) / abs(3 * zr1) ** 2) / (3 * V ** 2 * Rr / abs(zr1) ** 2), 1 / 3, tol=1e-9)
verifier("… soit tension d'enroulement divisée par √3", C_em(1.0, V / sqrt(3)) / C_em(1.0), 1 / 3, tol=1e-9)
verifier("couple triangle à 0,85 Ω_s / C_n (≈ 2,8)", C_em(0.15) / C_em(g), 2.78, tol=0.01)

print("── §6 : démarrage, énergie rotorique")
for J in (0.08, 0.1):
    w = 0.0; dt = 1e-5; E = 0.0
    while w < OMs * 0.999:
        gl = (OMs - w) / OMs
        c = C_em(gl)
        E += c * (OMs - w) * dt
        w += c / J * dt
    verifier(f"W_Jr simulé, J = {J} (½JΩ_s²)", E, 0.5 * J * OMs ** 2, tol=0.005)
verifier("auto-test 6 : ½ × 0,08 × 157,08²", 0.5 * 0.08 * OMs ** 2, 987, tol=0.001)
verifier("auto-test 6 : variateur, 4,2 × 0,08 × 157", 4.2 * 0.08 * 157, 53, tol=0.01)
verifier("… rapport", 987 / 53, 18.6, tol=0.01)
verifier("annexe A3 2021-E1 (11 kW) : I_L/I_N", 7.2, 7.2, tol=0)

print("── §7 : variation de vitesse")
verifier("η < 1 − g à 30 %", 1 - 0.30, 0.7, tol=1e-9)
verifier("C_max à 65 Hz sous tension nominale (fraction)", C_em(Rr / (Lf * 2 * pi * 65), V, 2 * pi * 65) / Cmax, 0.59, tol=0.005)
for fr in (15, 30):
    w2 = 2 * pi * fr
    gm2 = Rr / (Lf * w2)
    verifier(f"C_max à {fr} Hz, V/f constant", C_em(gm2, V * fr / 50, w2), Cmax, tol=1e-6)
    vrai(f"pulsation rotorique au maximum constante à {fr} Hz", abs(gm2 * w2 - gmax * ws) < 1e-9)
# THD 2024-E2, lecture du chapitre 4
thd_po = sqrt(95 ** 2 + 31 ** 2 + 31 ** 2 + 18 ** 2) / 170
thd_mli = sqrt(2 ** 2 + 38 ** 2 + 21 ** 2 + 2 ** 2) / 171
verifier("THD pleine onde (lecture du chapitre 4)", thd_po, 0.62, tol=0.01)
verifier("THD MLI (lecture du chapitre 4)", thd_mli, 0.25, tol=0.02)

print("── §8 : modèle scalaire")
pente = Cem / (OMs - W)
verifier("Ω_s − Ω_n", OMs - W, 4.19, tol=0.002)
verifier("pente pA", pente, 17.4, tol=0.003)
verifier("τ_m = J/(pA), J = 0,1", 0.1 / pente, 0.006, tol=0.05)
# réponse du modèle complet à un petit échelon de couple résistant
J = 0.1; w = W; Cr = Cem; dt = 1e-6; t = 0.0
w_fin = OMs * (1 - bissection(lambda x: C_em(x) - (Cr + 1.0), 1e-6, gmax))
w0 = w; t63 = None
while t < 0.05:
    c = C_em((OMs - w) / OMs)
    w += (c - Cr - 1.0) / J * dt
    t += dt
    if t63 is None and (w0 - w) >= 0.632 * (w0 - w_fin):
        t63 = t
verifier("constante de temps simulée (échelon de 1 N·m)", t63, 0.006, tol=0.05)

print("── Méthode : 2021-E1, 2023-E1")
vrai("2021-E1 annexe A3 : 930 à 995 tr/min, p = 3 pour toutes", all(int(3000 / n) == 3 for n in (930, 995)))
verifier("Q17 : g à 970 tr/min", (1000 - 970) / 1000, 0.03, tol=1e-9)
verifier("2023-E1 Q18 : 3 000/950", 3000 / 950, 3.16, tol=0.002)
verifier("2024-E2 A3 : g", 100 / 1500, 0.067, tol=0.005)
verifier("2021-E1 Q18 : L_P ω (Ω)", 3 * 133 ** 2 / 2137, 24.8, tol=0.002)
verifier("2021-E1 Q18 : L_P (mH)", 3 * 133 ** 2 / 2137 / (100 * pi) * 1e3, 79, tol=0.005)
verifier("… lu par phase (mH)", 133 ** 2 / 2137 / (100 * pi) * 1e3, 26, tol=0.02)
verifier("133 V = 230/√3", 230 / sqrt(3), 133, tol=0.002)
verifier("2021-E1 Q19 : 2,5 × 108", 2.5 * 108, 270, tol=1e-9)
verifier("… 7,2 × 22,5", 7.2 * 22.5, 162, tol=1e-9)
verifier("… écart de couple rotor bloqué (%)", (280 - 270) / 270 * 100, 4, tol=0.1)
verifier("2023-E1 Q19 : 16/50", 16 / 50, 0.32, tol=1e-9)
for Nv, Cr_, fv in ((450, 3.58, 23.1), (800, 11.3, 41.8)):
    c = 1.77e-5 * Nv ** 2
    verifier(f"2023-E1 Q20 : C_r à {Nv} tr/min", c, Cr_, tol=0.005)
    verifier(f"2023-E1 Q20 : f à {Nv} tr/min", (Nv + c / 0.32) / 20, fv, tol=0.003)

print("── Méthode : 2024-E2")
g24 = 100 / 1500; Rr24 = 0.1; Lf24 = 3.6e-3; w24 = 100 * pi
verifier("A4 : I'_r", 230 / hypot(Rr24 / g24, Lf24 * w24), 122, tol=0.005)
Pa24 = 3 * 230 * 229 * 0.85; Pjr24 = 3 * 0.1 * 122 ** 2; W24 = 2 * pi * 1400 / 60; Ppm24 = 200 * W24
verifier("A5 : P_a (kW)", Pa24 / 1e3, 134.3, tol=0.001)
verifier("A5 : P_Jr (kW)", Pjr24 / 1e3, 4.47, tol=0.002)
verifier("Ω à 1 400 tr/min", W24, 146.6, tol=0.001)
verifier("A5 : P_pm (kW)", Ppm24 / 1e3, 29.3, tol=0.002)
verifier("A6 : P_u selon le DT1 (kW)", (Pa24 - Pjr24 - Ppm24) / 1e3, 100.5, tol=0.001)
verifier("pertes fer 3 × 230²/420 (kW)", 3 * 230 ** 2 / 420 / 1e3, 0.38, tol=0.01)
verifier("A6 avec pertes fer (kW)", (Pa24 - Pjr24 - Ppm24 - 3 * 230 ** 2 / 420) / 1e3, 100.1, tol=0.001)
Dt = 10 * (2500 + 2750) / 3600
verifier("A1 : D_t (m³/s)", Dt, 14.58, tol=0.002)
verifier("A2 : P_extra (kW)", 5297 * Dt / 1e3, 77.2, tol=0.002)
verifier("A2 : P_u requise (kW)", 5297 * Dt / 0.78 / 1e3, 99.0, tol=0.002)
verifier("remarque : P_t du modèle (kW)", 3 * (Rr24 / g24) * 122 ** 2 / 1e3, 67, tol=0.005)
verifier("A8 : couple nominal (N·m)", 100e3 / W24, 682, tol=0.002)
verifier("A8 : surcharge à 865 N·m (%)", (865 / 682 - 1) * 100, 27, tol=0.02)
A24 = 3 * 2 / Rr24 * (230 / w24) ** 2
verifier("C2 : A (N·m·s/rad)", A24, 32.2, tol=0.002)
Cmax24 = 3 * 2 / (2 * Lf24) * (230 / w24) ** 2; gmax24 = Rr24 / (Lf24 * w24)
verifier("C1 : 2 C_max/g_max = 3pV²/(R'ω)", 2 * Cmax24 / gmax24, 3 * 2 * 230 ** 2 / (Rr24 * w24), tol=1e-9)
verifier("C3 : K_méca", 1 / 4e-3, 250, tol=1e-9)
verifier("C3 : τ_méca (s)", 0.035 / 4e-3, 8.75, tol=1e-9)
verifier("g_max du DT1", gmax24, 0.088, tol=0.01)

print("── Méthode : 2025-E1, 2015-E1")
Pp = 1380 * 9.81 * 0.11; Pm25 = Pp / (0.9 * 0.94)
verifier("Q50 : P (kW)", Pp / 1e3, 1.49, tol=0.002)
verifier("Q51 : sur l'arbre (kW)", Pm25 / 1e3, 1.76, tol=0.002)
Ne = 0.11 / (pi * 0.06545) * 60
verifier("Q52 : enrouleur (tr/min)", Ne, 32.1, tol=0.002)
rr = 16 * 8 * 12 / (35 * 45 * 70)
verifier("Q53 : 1/r", 1 / rr, 71.8, tol=0.001)
verifier("Q53 : N moteur (tr/min)", Ne / rr, 2304, tol=0.001)
vrai("Q53 : une paire de pôles (N_s = 3 000 tr/min)", int(3000 / (Ne / rr)) == 1)
verifier("Q54 : marge du 1,8 kW (%)", (1.8 / (Pm25 / 1e3) - 1) * 100, 2, tol=0.15)
verifier("Q54 : vitesse de levage à 2 780 tr/min", 0.11 * 2780 / 2304, 0.13, tol=0.03)
verifier("Q60 : poids (kN)", 1380 * 9.81 / 1e3, 13.5, tol=0.005)
verifier("2015-E1 Q19 : 2,2 × 3,7", 2.2 * 3.7, 8.1, tol=0.006)

print("── Exemple 5 : 1 200 tr/min à V/f constant")
W2 = 2 * pi * 1200 / 60
Cu2 = Cu * (1200 / N) ** 2; Cem2 = Cu2 + Cp
A = 3 * p / Rr * (V / ws) ** 2
wr2 = Cem2 / A; ws2 = p * W2 + wr2; f2 = ws2 / (2 * pi)
verifier("couple du ventilateur", Cu2, 48.5, tol=0.002)
verifier("C_em", Cem2, 49.5, tol=0.002)
verifier("ω_r", wr2, 5.49, tol=0.002)
verifier("Ω à 1 200 tr/min", W2, 125.66, tol=1e-4)
verifier("ω_s", ws2, 256.8, tol=0.001)
verifier("f", f2, 40.9, tol=0.002)
verifier("V_s", V * f2 / 50, 189, tol=0.003)
verifier("U", sqrt(3) * V * f2 / 50, 327, tol=0.003)
f_exact = bissection(lambda fx: C_em((2 * pi * fx / p - W2) / (2 * pi * fx / p), V * fx / 50, 2 * pi * fx) - Cem2, 40.05, 45)
vrai(f"modèle complet : f = {f_exact:.3f} Hz, à 0,1 Hz près", abs(f_exact - f2) < 0.1)
verifier("P_u", Cu2 * W2, 6090, tol=0.002)
verifier("P_u / P_u nominale", Cu2 * W2 / Pu, 0.55, tol=0.01)
verifier("(1 200/1 460)³", (1200 / 1460) ** 3, 0.555, tol=0.001)
verifier("1 200/1 460", 1200 / 1460, 0.82, tol=0.003)

print("── Auto-test")
verifier("Q1 : 3 000/2 880", 3000 / 2880, 1.04, tol=0.002)
verifier("Q1 : g", 120 / 3000, 0.04, tol=1e-9)
verifier("Q1 : f_r", 0.04 * 50, 2, tol=1e-9)
verifier("Q2 : 400/√3", 400 / sqrt(3), 231, tol=0.001)
verifier("Q3 : C_em = 10 000/157,08", 10000 / OMs, 63.7, tol=0.002)
verifier("Q3 : C_em = 9 600/150,8", 9600 / (OMs * 0.96), 63.7, tol=0.002)
verifier("Q3 : Ω à g = 4 %", OMs * 0.96, 150.8, tol=0.001)
g4 = -30 / 1500; W4 = 2 * pi * 1530 / 60
verifier("Q4 : g", g4, -0.02, tol=1e-9)
verifier("Q4 : Ω (rad/s)", W4, 160.2, tol=0.001)
verifier("Q4 : P_t (kW)", -100 * OMs / 1e3, -15.7, tol=0.002)
verifier("Q4 : P_méca (kW)", -100 * W4 / 1e3, -16.0, tol=0.002)
verifier("Q4 : P_Jr (W)", g4 * (-100 * OMs), 314, tol=0.002)
verifier("Q4 : P_méca − P_t = −P_Jr", (-100 * W4) - (-100 * OMs), -314, tol=0.003)
verifier("Q5 : N à 25 Hz", 750 - 40, 710, tol=1e-9)
verifier("Q5 : g", 40 / 750, 0.053, tol=0.01)
gm25 = Rr / (Lf * 2 * pi * 25)
verifier("Q5 : C_max à 25 Hz", C_em(gm25, V / 2, 2 * pi * 25), 203, tol=0.003)
vrai("Q5 : vitesse sous C_em nominal, modèle complet (écart N_s − N = 40 tr/min)",
     abs(750 * (1 - bissection(lambda x: C_em(x, V / 2, 2 * pi * 25) - C_em(g), 1e-6, gm25)) - 710) < 0.5)

print()
if ECARTS:
    print(f"{len(ECARTS)} écart(s) :", ", ".join(ECARTS))
    raise SystemExit(1)
print("Aucun écart.")
