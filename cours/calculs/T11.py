"""Applications numériques du chapitre T11, refaites en Python.

    python3 cours/calculs/T11.py

Chaque bloc reprend une valeur publiée dans cours/textes/T11.html ; un
écart de plus de 0,5 % sur la valeur arrondie fait échouer le script.
Les démarrages et la réponse dynamique sont simulés (Euler, pas fin).
"""
import json
from collections import Counter
from math import sqrt, pi
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


print("── En bref : fréquence")
cartes = json.loads((RACINE / "cards.json").read_text())
th = next(t for t in cartes["themes"] if t["code"] == "T11")
verifier("présence dans les sujets (cartes)", th["presence_n"], 10)
releve = json.loads((RACINE / "cours/releve-sujets.json").read_text())
qs = [(e["id"], q) for e in releve["epreuves"] for q in e["questions"] if "T11" in q["themes"]]
verifier("questions mobilisant T11", len(qs), 2)
vrai("… 2020-E2, Q16 et Q18, en thème secondaire",
     sorted((e, q["q"]) for e, q in qs) == [("2020-E2", "16"), ("2020-E2", "18")]
     and all(q["themes"][0] != "T11" for _, q in qs))
n_f = sum(1 for c in cartes["cards"] if c.get("theme") == "T11" and c["type"] == "formule")
n_p = sum(1 for c in cartes["cards"] if c.get("theme") == "T11" and c["type"] == "piege")
verifier("cartes : formules", n_f, 15)
verifier("cartes : pièges", n_p, 6)

print("── §2 : constante")
verifier("0,06 V·s/rad en V pour 1 000 tr/min", 0.06 * 1000 * 2 * pi / 60, 6.28, tol=0.002)
verifier("facteur 1 000 tr/min → rad/s", 1000 * 2 * pi / 60, 104.7, tol=0.001)

print("── §5 : caractéristiques (moteur du convoyeur)")
K, R = 0.06, 0.8
verifier("pente R/K²", R / K ** 2, 222.2, tol=0.001)
verifier("I pour 0,32 N·m", 0.32 / K, 5.33, tol=0.002)
for U, w in ((24, 328.9), (12, 128.9)):
    verifier(f"Ω sous {U} V (rad/s)", U / K - R * 0.32 / K ** 2, w, tol=0.001)
verifier("400 − 222,2 × 0,32", 400 - 222.2 * 0.32, 328.9, tol=0.001)
vrai("figure 6 : 12 V, couple de démarrage 0,9 N·m (droite coupée à Ω = 0)", abs(K * 12 / R - 0.9) < 1e-12)

print("── §3 : réciproque du critère moteur")
E_, I_ = 5.0, -120.0          # freinage en fin de course : E faible, I négatif (convention récepteur)
U_ = E_ + 0.15 * I_
vrai("EI < 0 mais |U| > |E| et UI > 0 (contre-courant, fin de freinage)", E_ * I_ < 0 and abs(U_) > abs(E_) and U_ * I_ > 0)
verifier("2023-E2 D5 : K_GT = 5,0 / 104,7 (V·s/rad)", 5.0 / (1000 * 2 * pi / 60), 0.0477, tol=0.002)
print("── Exemple : treuil")
Un, In, Nn, Ra, Pc, Udc = 440, 120, 1500, 0.15, 1600, 540
Wn = 2 * pi * Nn / 60
verifier("Ω_n (rad/s)", Wn, 157.1, tol=0.001)
En = Un - Ra * In
verifier("E_n (V)", En, 422)
kP = En / Wn
verifier("kΦ (V·s/rad)", kP, 2.687, tol=0.001)
I0 = Pc / Wn / kP
verifier("I_0 à vide (A)", I0, 3.8, tol=0.01)
verifier("R I_0 (V)", Ra * I0, 0.6, tol=0.06)
verifier("vitesse à vide réelle (rad/s)", (Un - Ra * I0) / kP, 163.5, tol=0.001)
verifier("chute de vitesse en charge, à vide réel (%)", 100 * (1 - Wn / ((Un - Ra * I0) / kP)), 4, tol=0.03)
m_, rt, red = 2546, 0.25, 20
verifier("C_r = m g r_t / 20 (N·m)", m_ * 9.81 * rt / red, 312.2, tol=0.0005)
verifier("tambour : Ω_n/20 (rad/s)", Wn / red, 7.85, tol=0.001)
verifier("vitesse de levage (m/s)", Wn / red * rt, 1.96, tol=0.002)
verifier("… à mi-vitesse (m/s)", Wn / 2 / red * rt, 0.98, tol=0.002)
verifier("inertie ramenée m r²/20² (kg·m²)", m_ * rt ** 2 / red ** 2, 0.40, tol=0.01)
verifier("chute de vitesse en charge (%)", 100 * (1 - Wn / (Un / kP)), 4, tol=0.05)
Cem = kP * In
verifier("C_em (N·m)", Cem, 322.4, tol=0.001)
Cp = Pc / Wn
verifier("C_p (N·m)", Cp, 10.2, tol=0.002)
Cu = Cem - Cp
verifier("C_u (N·m)", Cu, 312.2, tol=0.001)
Pa, Pj, Pem = Un * In, Ra * In ** 2, En * In
verifier("P_a (kW)", Pa / 1e3, 52.8)
verifier("P_J (kW)", Pj / 1e3, 2.16)
verifier("P_em (kW)", Pem / 1e3, 50.64)
Pu = Pem - Pc
verifier("P_u (kW)", Pu / 1e3, 49.04)
verifier("P_u = C_u Ω_n (kW)", Cu * Wn / 1e3, 49.04)
verifier("η induit (%)", 100 * Pu / Pa, 92.9, tol=0.001)
verifier("P_ex (W)", 220 * 3.6, 792)
verifier("η avec excitation (%)", 100 * Pu / (Pa + 792), 91.5, tol=0.001)
verifier("P_a + P_ex (kW)", (Pa + 792) / 1e3, 53.59, tol=0.0005)
Idem = Un / Ra
verifier("démarrage direct (A)", Idem, 2933, tol=0.001)
verifier("… en I_n", Idem / In, 24.4, tol=0.002)
Id = 1.5 * In
verifier("R_rh(0) (Ω)", Un / Id - Ra, 2.29, tol=0.002)
wz = (Un - Ra * Id) / kP
verifier("R_rh nul à (rad/s)", wz, 153.7, tol=0.001)
verifier("… en tr/min", wz * 30 / pi, 1468, tol=0.001)
verifier("couple de démarrage (N·m)", kP * Id, 484, tol=0.002)
# crans
Imax, ncr = 240, 4
R1 = Un / Imax
q = (Ra / R1) ** (1 / ncr)
verifier("rapport des crans", q, 0.535, tol=0.001)
verifier("I_min (A)", q * Imax, 128, tol=0.003)
for k, v in enumerate((1.833, 0.981, 0.524, 0.280)):
    verifier(f"cran {k + 1} : résistance totale (Ω)", R1 * q ** k, v, tol=0.002)
vrai("après le 4e cran, il reste R = 0,15 Ω", abs(R1 * q ** 4 - Ra) < 1e-12)
vrai("I_min > 120 A : la machine accélère toujours", q * Imax > 120)
# simulation du démarrage par crans : le courant reste entre I_min et I_max
J = 3.0
w = 0.0; k = 0; Rk = R1; imin_vu, imax_vu = 1e9, 0
dt = 1e-4
for _ in range(400000):
    I = (Un - kP * w) / Rk
    if k < ncr and I <= q * Imax:
        k += 1; Rk = R1 * q ** k; I = (Un - kP * w) / Rk
    imax_vu = max(imax_vu, I)
    if k < ncr:
        imin_vu = min(imin_vu, I)
    w += (kP * I - Cu - Cp) / J * dt
verifier("simulation des crans : courant maximal (A)", imax_vu, 240, tol=0.002)
verifier("simulation des crans : courant minimal pendant les crans (A)", imin_vu, 128, tol=0.005)
verifier("simulation des crans : vitesse finale (rad/s)", w, Wn, tol=0.001)
# montée et descente à mi-vitesse
W2 = Wn / 2
verifier("Ω à 750 tr/min", W2, 78.54, tol=0.0005)
E2 = kP * W2
verifier("E montée (V)", E2, 211)
U2 = E2 + Ra * In
verifier("U montée (V)", U2, 229)
verifier("α montée, pont en H", 0.5 * (U2 / Udc + 1), 0.712, tol=0.001)
Cd = Cu - Cp
verifier("C_em descente (N·m)", Cd, 302.0, tol=0.001)
Id2 = Cd / kP
verifier("I descente (A)", Id2, 112.4, tol=0.001)
Ud = -E2 + Ra * Id2
verifier("U descente (V)", Ud, -194.1, tol=0.001)
verifier("U I descente (kW)", Ud * Id2 / 1e3, -21.8, tol=0.003)
verifier("puissance fournie par la charge (kW)", Cu * W2 / 1e3, 24.5, tol=0.003)
verifier("pertes collectives à mi-vitesse (kW)", Cp * W2 / 1e3, 0.8)
verifier("pertes Joule en descente (kW)", Ra * Id2 ** 2 / 1e3, 1.9, tol=0.01)
vrai("bilan de la descente bouclé", abs(Cu * W2 - Cp * W2 - Ra * Id2 ** 2 + Ud * Id2) < 1e-6)
verifier("α descente, pont en H", 0.5 * (Ud / Udc + 1), 0.320, tol=0.001)
verifier("U_dc = 1,35 × 400 V", 1.35 * 400, 540)
verifier("P_J / P_a (%)", 100 * Pj / Pa, 4.1, tol=0.01)
verifier("I_dém / I_n = U/(R I_n), sans dimension", Un / (Ra * In), 24, tol=0.02)
# §2 : démonstration de k
p_, Nc, a_, r_, l_, Phi = 2, 400, 1, 0.12, 0.25, 0.02
B = p_ * Phi / (pi * r_ * l_)
vrai("k : B moyen × surface polaire = Φ", abs(B * 2 * pi * r_ * l_ / (2 * p_) - Phi) < 1e-15)
W_ = 100.0
e_c = B * l_ * r_ * W_
vrai("k : e d'un conducteur = pΦΩ/π", abs(e_c - p_ * Phi * W_ / pi) < 1e-12)
vrai("k : E = (N_c/2a) e = pN_cΦΩ/(2πa)", abs(Nc / (2 * a_) * e_c - p_ * Nc * Phi * W_ / (2 * pi * a_)) < 1e-9)
# figure 12 : points sur les droites
vrai("figure 12 : montée sur la droite U = 229 V", abs(229 / kP - Ra * Cem / kP ** 2 - W2) < 0.01)
vrai("figure 12 : descente sur la droite U = −194,1 V", abs(-194.1 / kP - Ra * Cd / kP ** 2 + W2) < 0.05)
# figure 7 : le rhéostat continu, nul à 153,7 rad/s, rejoint I_n à Ω_n le long de la droite R seule
vrai("figure 7 : après annulation du rhéostat, I = (U − kΦΩ)/R vaut I_n à Ω_n", abs((Un - kP * Wn) / Ra - In) < 1e-9)

print("── Méthode : 2020-E2, Q18 ; 2023-E2, D4")
for U, v in ((12, 35.9), (24, 17.9)):
    verifier(f"I sous {U} V, 370 W utiles, η = 0,86", 370 / 0.86 / U, v, tol=0.002)
verifier("P_a = 370/0,86 (W)", 370 / 0.86, 430, tol=0.002)
verifier("lecture « absorbée », 12 V (A)", 370 / 12, 30.8, tol=0.002)
calibres = (0.5, 1, 2, 3, 4, 6, 10, 13, 16, 20, 25, 32, 40, 50, 63)
verifier("calibre iC60 juste supérieur à 35,9 A", min(c for c in calibres if c >= 370 / 0.86 / 12), 40)
verifier("calibre iC60 juste supérieur à 30,8 A", min(c for c in calibres if c >= 370 / 12), 32)
wa, wb = 10, 7000
te, tm = 1 / (wa + wb), 1 / wa + 1 / wb
verifier("τ_e (ms)", 1e3 * te, 0.14, tol=0.02)
verifier("τ_m (s)", tm, 0.1, tol=0.002)
for p in (1j, 50 + 3j, 4000j):
    vrai(f"(1 + p/ωa)(1 + p/ωb) = 1 + τm p + τe τm p² en p = {p}",
         abs((1 + p / wa) * (1 + p / wb) - (1 + tm * p + te * tm * p * p)) < 1e-9 * abs(p) ** 2 + 1e-12)

print("── §6 et §8 : démarrage, dynamique")
for frac, n_ in ((0.10, 10), (0.02, 50)):
    verifier(f"R I_n = {frac:.0%} de U_n : I_dém / I_n", 1 / frac, n_)
verifier("petit moteur : convoyeur, I_dém / I en charge (30 A / 5,33 A)", (24 / 0.8) / (0.32 / 0.06), 5.6, tol=0.01)
verifier("convoyeur : R I / U en charge (%)", 100 * 0.8 * (0.32 / 0.06) / 24, 18, tol=0.02)
# rhéostat continu à vide : énergie dissipée = énergie cinétique si E finit à U
Jv, Uv, kv, Id_ = 0.5, 220.0, 1.0, 10.0
wf = Uv / kv
t_f = Jv * wf / (kv * Id_)
fournie = Uv * Id_ * t_f
cine = 0.5 * Jv * wf ** 2
vrai("p-005 : à vide, jusqu'à E = U, dissipée = cinétique = moitié de la fournie",
     abs((fournie - cine) - cine) < 1e-9 * fournie)
# convoyeur : constantes de temps (rappel chapitre 12)
L, Jc = 1.6e-3, 4e-4
verifier("τ_e convoyeur (ms)", 1e3 * L / R, 2.0)
verifier("τ_m convoyeur (ms)", 1e3 * R * Jc / K ** 2, 88.9, tol=0.001)
poles = np.roots([L * Jc, R * Jc, K ** 2])
verifier("pôle lent ≈ −1/τ_m (rad/s)", max(poles.real), -11.5, tol=0.003)
# §8 : sous un échelon, le courant monte en quelques τ_e puis retombe avec τ_m
dt = 1e-6; i = w = 0.0; ts, is_ = [], []
for k in range(int(0.5 / dt)):
    i += (24 - R * i - K * w) / L * dt
    w += (K * i) / Jc * dt
    if k % 50 == 0:
        ts.append(k * dt); is_.append(i)
ts, is_ = np.array(ts), np.array(is_)
k0 = is_.argmax()
verifier("échelon 24 V à vide : pic de courant (A), près de U/R = 30 A", is_[k0], 28, tol=0.01)
verifier("… atteint vers (ms), quelques τ_e", 1e3 * ts[k0], 7.9, tol=0.03)
vrai("… puis le courant retombe : sous 2 A après 0,3 s (≈ 3 τ_m)", is_[ts.searchsorted(0.3)] < 2)
vrai("le courant ne s'établit pas en quelques τ_e (encore > 20 A à 5 τ_e = 10 ms)", is_[ts.searchsorted(0.010)] > 20)

print("── Auto-test")
U1, I1, R1a = 220, 12, 1.0
W1 = 2 * pi * 1500 / 60
E1 = U1 - R1a * I1
verifier("Q1 : E (V)", E1, 208)
k1 = E1 / W1
verifier("Q1 : kΦ", k1, 1.324, tol=0.001)
verifier("Q1 : C_em (N·m)", k1 * I1, 15.9, tol=0.002)
verifier("Q2 : U génératrice (V)", E1 - R1a * 10, 198)
verifier("Q2 : puissance délivrée (W)", (E1 - 10) * 10, 1980)
verifier("Q2 : E I (W)", E1 * 10, 2080)
Pa1 = U1 * I1
verifier("Q3 : P_a (W)", Pa1, 2640)
verifier("Q3 : P_J (W)", R1a * I1 ** 2, 144)
verifier("Q3 : P_em (W)", E1 * I1, 2496)
Pu1 = E1 * I1 - 150
verifier("Q3 : P_u (W)", Pu1, 2346)
verifier("Q3 : C_u (N·m)", Pu1 / W1, 14.9, tol=0.003)
verifier("Q3 : η induit (%)", 100 * Pu1 / Pa1, 88.9, tol=0.001)
verifier("Q3 : η global (%)", 100 * Pu1 / (Pa1 + 110), 85.3, tol=0.001)
verifier("Q4 : démarrage direct (A)", U1 / R1a, 220)
verifier("Q4 : en I_n", U1 / R1a / I1, 18.3, tol=0.002)
verifier("Q4 : R_rh(0) pour 24 A (ohms)", U1 / 24 - R1a, 8.17, tol=0.002)
verifier("Q3 : puissance d'excitation 220 V × 0,5 A (W)", 220 * 0.5, 110)
w4 = (U1 - R1a * 24) / k1
verifier("Q4 : R_rh nul à (rad/s)", w4, 148, tol=0.002)
verifier("Q4 : … en tr/min", w4 * 30 / pi, 1413, tol=0.002)
W5 = -2 * pi * 1000 / 60
verifier("Q5 : Ω (rad/s)", W5, -104.7, tol=0.001)
E5 = k1 * W5
verifier("Q5 : E (V)", E5, -138.7, tol=0.001)
U5 = E5 + R1a * (-6)
verifier("Q5 : U (V)", U5, -144.7, tol=0.001)
verifier("Q5 : α", 0.5 * (U5 / 300 + 1), 0.259, tol=0.003)
vrai("Q5 : E I > 0 avec E < 0 et I < 0 : quadrant 3", E5 < 0 and E5 * (-6) > 0)
C6 = k1 * 24
verifier("Q6 : couple (N·m)", C6, 31.8, tol=0.002)
t6 = 0.5 * w4 / C6
verifier("Q6 : durée (s)", t6, 2.33, tol=0.003)
F6 = U1 * 24 * t6
verifier("Q6 : énergie fournie (kJ)", F6 / 1e3, 12.3, tol=0.004)
K6 = 0.5 * 0.5 * w4 ** 2
verifier("Q6 : énergie cinétique (kJ)", K6 / 1e3, 5.48, tol=0.002)
verifier("Q6 : énergie dissipée (kJ)", (F6 - K6) / 1e3, 6.8, tol=0.005)
verifier("Q6 : part dissipée (%)", 100 * (F6 - K6) / F6, 55, tol=0.01)
verifier("Q6 : E finale (V)", k1 * w4, 196)
verifier("Q6 : avec hacheur, R I² t (kJ)", R1a * 24 ** 2 * t6 / 1e3, 1.34, tol=0.003)
# simulation du démarrage rhéostatique de Q6
w = 0.0; dt = 1e-4; diss = 0.0; fourn = 0.0
while w < w4:
    I = 24.0
    Rtot = (U1 - k1 * w) / I
    diss += Rtot * I * I * dt; fourn += U1 * I * dt
    w += k1 * I / 0.5 * dt
verifier("Q6 simulé : énergie dissipée (kJ)", diss / 1e3, 6.8, tol=0.005)

print()
if ECARTS:
    print(f"{len(ECARTS)} écart(s) :", ", ".join(ECARTS))
    raise SystemExit(1)
print("Aucun écart.")
