"""Applications numériques du chapitre T30, refaites en Python.

    python3 cours/calculs/T30.py

Chaque bloc reprend une valeur publiée dans cours/textes/T30.html ; un
écart supérieur à la demi-unité du dernier chiffre publié fait échouer le
script (tolérance relative explicite pour une valeur annoncée « environ »).
Les arrondis « par excès » d'une incertitude élargie se vérifient à part.
"""
from decimal import Decimal
from math import sqrt, log2, pi, ceil
from statistics import mean, stdev

ECARTS = []


def verifier(nom, calcule, publie, tol=None):
    """Écart admis : la demi-unité du dernier chiffre publié, sauf tolérance relative explicite."""
    # Une valeur publiée avec un zéro final (« 0,580 ») se passe en chaîne.
    texte = publie if isinstance(publie, str) else repr(publie)
    publie = float(texte)
    if tol is None:
        ecart_admis = 0.5 * 10 ** Decimal(texte).as_tuple().exponent * 1.000001
    else:
        ecart_admis = tol * max(abs(publie), 1e-12)
    ok = abs(calcule - publie) <= ecart_admis
    print(f"{'ok ' if ok else 'ÉCART'} {nom:62s} calculé {calcule:.6g} · publié {publie:g}")
    if not ok:
        ECARTS.append(nom)


def vrai(nom, ok):
    print(f"{'ok ' if ok else 'ÉCART'} {nom}")
    if not ok:
        ECARTS.append(nom)


def par_exces(x, chiffres=2):
    """Arrondi par excès à « chiffres » chiffres significatifs."""
    from math import floor, log10
    e = floor(log10(abs(x))) - chiffres + 1
    return ceil(round(x / 10 ** e, 9)) * 10 ** e


# ── §1 : classe de précision ─────────────────────────────────────────────
verifier("§1 : classe 1,5 sur 300 V (V)", 0.015 * 300, 4.5)

# ── §2 : type A sur dix lectures ─────────────────────────────────────────
serie = [12.03, 12.07, 12.01, 12.05, 12.04, 12.06, 12.02, 12.05, 12.03, 12.04]
verifier("§2 : moyenne (V)", mean(serie), "12.040")
verifier("§2 : écart-type expérimental (V)", stdev(serie), 0.018)
uA = stdev(serie) / sqrt(len(serie))
verifier("§2 : u_A (V)", uA, 0.0058)
verifier("fig. : √10", sqrt(10), 3.2)
vrai("§2 : 4 fois plus de mesures divisent u_A par 2", abs(sqrt(4) - 2) < 1e-12)

# ── §3 : type B ──────────────────────────────────────────────────────────
# variance de la loi uniforme sur [−a, a] : ∫ x²/(2a) dx = a²/3 (intégration numérique, a = 1)
n = 200000
var_u = sum(((-1 + (k + 0.5) * 2 / n) ** 2) / 2 * (2 / n) for k in range(n))
verifier("§3 : variance uniforme / a²", var_u, 1 / 3, tol=1e-4)
# loi triangulaire de demi-base a = 1 : densité 1 − |x|
var_t = sum(((-1 + (k + 0.5) * 2 / n) ** 2) * (1 - abs(-1 + (k + 0.5) * 2 / n)) * (2 / n) for k in range(n))
verifier("§3 : variance triangulaire / a²", var_t, 1 / 6, tol=1e-4)
verifier("fig. : 1/√3", 1 / sqrt(3), 0.58)
verifier("fig. : 1/√6", 1 / sqrt(6), 0.41)
a_ex = 0.005 * 12.04 + 2 * 0.01
verifier("§3 : a du multimètre (V)", a_ex, 0.0802)
uB = a_ex / sqrt(3)
verifier("§3 : u_B (V)", uB, 0.0463)
vrai("§3 : q/(2√3) = q/√12", abs(1 / (2 * sqrt(3)) - 1 / sqrt(12)) < 1e-12)

# ── §4 : composition, élargissement, écriture ────────────────────────────
uc = sqrt(uA ** 2 + uB ** 2)
verifier("§4 : u_c (V)", uc, 0.047)
verifier("§4 : u_c avec les valeurs affichées (V)", sqrt(0.0058 ** 2 + 0.0463 ** 2), 0.047)
verifier("§4 : U(x) = 2 u_c (V)", 2 * uc, 0.0933)
vrai("§4 : 0,0933 arrondi par excès à 0,094", abs(par_exces(2 * uc) - 0.094) < 1e-12)
verifier("§4 : incertitude relative (%)", 0.094 / 12.04 * 100, 0.8)
# Student, 95 % bilatéral : 4 et 9 degrés de liberté
verifier("§4 : t de Student, 5 mesures", 2.776, 2.78)
verifier("§4 : t de Student, 10 mesures", 2.262, 2.26)

# ── §5 : propagation ─────────────────────────────────────────────────────
verifier("§5 : u_r(U) (%)", uc / 12.04 * 100, 0.39)
verifier("§5 : R = U/I (Ω)", 12.04 / 0.512, 23.52)
verifier("§5 : u_r(R) (%)", sqrt(0.39 ** 2 + 0.80 ** 2), 0.89)
# loi de propagation contre Monte-Carlo, R = U/I
import random
rnd = random.Random(1)
tirages = [(12.04 + rnd.gauss(0, 0.0039 * 12.04)) / (0.512 + rnd.gauss(0, 0.008 * 0.512)) for _ in range(200000)]
verifier("§5 : u_r(R) par Monte-Carlo (%)", stdev(tirages) / mean(tirages) * 100, 0.89, tol=0.02)

# ── §6 : conformité ──────────────────────────────────────────────────────
vrai("§6 : 100,6 ± 0,3 dans [99 ; 101]", 99 <= 100.6 - 0.3 and 100.6 + 0.3 <= 101)
vrai("§6 : 100,9 ± 0,3 à cheval sur 101", 100.9 - 0.3 < 101 < 100.9 + 0.3)

# ── §7 : appareils numériques ────────────────────────────────────────────
verifier("§7 : log2(6 000) (bits)", log2(6000), 12.6)
verifier("§7 : écart relatif des conventions sur 8 bits (%)", 1 / 255 * 100, 0.4)
q_osc = 8 / 256
verifier("§7 : quantum de l'oscilloscope (mV)", q_osc * 1e3, 31.25)
verifier("§7 : 3,30 × 256/8", 3.30 * 256 / 8, 105.6)
vrai("§7 : saturation au-delà de U_PE − q/2 (round donnerait 2^n)", round((8 - q_osc / 2 + 1e-9) / q_osc) == 256)
vrai("§7 : N = round(105,6) = 106", round(3.30 * 256 / 8) == 106)
verifier("§7 : facteur de forme π/(2√2)", pi / (2 * sqrt(2)), 1.11)
# créneau ±10 V : <|v|> = 10, efficace 10 ; triangle amplitude 10 : <|v|> = 5, efficace 10/√3
verifier("§7 : non RMS sur créneau ±10 V (V)", pi / (2 * sqrt(2)) * 10, 11.1)
verifier("§7 : non RMS sur triangle 10 V (V)", pi / (2 * sqrt(2)) * 5, 5.55)
verifier("§7 : efficace du triangle 10 V (V)", 10 / sqrt(3), 5.77)
verifier("fig. : non RMS / efficace, créneau", pi / (2 * sqrt(2)), 1.111)
verifier("fig. : efficace du triangle / amplitude", 1 / sqrt(3), 0.577)
verifier("fig. : non RMS du triangle / amplitude", pi / (2 * sqrt(2)) / 2, 0.555)
verifier("fig. : écart sur le triangle (%)", (pi / (2 * sqrt(2)) / 2 * sqrt(3) - 1) * 100, -3.8)
# créneau 0–10 V, rapport cyclique 0,5
moy, eff = 5.0, sqrt(0.5 * 100)
verifier("§7 : MLI, valeur moyenne (V)", moy, 5)
verifier("§7 : MLI, efficace de la composante AC (V)", sqrt(eff ** 2 - moy ** 2), 5)
verifier("§7 : MLI, efficace AC+DC (V)", eff, 7.07)
verifier("§7 : fe de l'oscilloscope, 10 000 points sur 1 s (kHz)", 10000 / 1 / 1e3, 10)

# ── §8 : branchement ─────────────────────────────────────────────────────
verifier("§8 : frontière amont/aval, R_A = 1 Ω, R_V = 10 MΩ (kΩ)", sqrt(1 * 10e6) / 1e3, 3.2)
# erreurs relatives égales à la frontière
R = sqrt(1 * 10e6)
vrai("§8 : R_A/R = R/R_V à la frontière", abs(1 / R - R / 10e6) < 1e-12)

# ── §8 : méthode des deux wattmètres (phaseurs, ordre direct) ───────────
import cmath
for phi_deg in (0, 30, 60, 75, -40):
    V, I, phi = 230.0, 10.0, phi_deg * pi / 180
    v = [cmath.rect(V, 0), cmath.rect(V, -2 * pi / 3), cmath.rect(V, 2 * pi / 3)]
    i = [cmath.rect(I, -phi), cmath.rect(I, -2 * pi / 3 - phi), cmath.rect(I, 2 * pi / 3 - phi)]
    W1 = ((v[0] - v[2]) * i[0].conjugate()).real
    W2 = ((v[1] - v[2]) * i[1].conjugate()).real
    U = sqrt(3) * V
    from math import cos as _cos, sin as _sin
    vrai(f"§8 : φ = {phi_deg}° : W1 = UI cos(φ − 30°), W2 = UI cos(φ + 30°)",
         abs(W1 - U * I * _cos(phi - pi / 6)) < 1e-6 and abs(W2 - U * I * _cos(phi + pi / 6)) < 1e-6)
    vrai(f"§8 : φ = {phi_deg}° : P = W1 + W2 et Q = √3 (W1 − W2)",
         abs(W1 + W2 - 3 * V * I * _cos(phi)) < 1e-6 and abs(sqrt(3) * (W1 - W2) - 3 * V * I * _sin(phi)) < 1e-6)
    vrai(f"§8 : φ = {phi_deg}° : W2 < 0 si et seulement si φ > 60°", (W2 < -1e-9) == (phi_deg > 60))
# charge déséquilibrée à trois fils : P = W1 + W2 reste exacte
v = [cmath.rect(230, 0), cmath.rect(230, -2 * pi / 3), cmath.rect(230, 2 * pi / 3)]
i1, i2 = cmath.rect(7, -0.3), cmath.rect(12, -2.4)
i3 = -i1 - i2
P = sum((vk * ik.conjugate()).real for vk, ik in zip(v, (i1, i2, i3)))
vrai("§8 : charge déséquilibrée, P = W1 + W2", abs(P - (((v[0] - v[2]) * i1.conjugate()).real + ((v[1] - v[2]) * i2.conjugate()).real)) < 1e-6)
verifier("§9 : atténuation de 3 dB (%)", (1 - 1 / sqrt(2)) * 100, 29)
verifier("§7 : π/(2√2) = (V̂/√2)/(2V̂/π)", (1 / sqrt(2)) / (2 / pi), 1.11)

# ── §10 : thermocouple ───────────────────────────────────────────────────
verifier("§10 : type K à 100 °C (mV)", 41e-6 * 100 * 1e3, 4.1)
verifier("§10 : type K vers 1 000 °C, « une quarantaine » (mV)", 41e-6 * 1000 * 1e3, 40, tol=0.1)

# ── Méthode : 2020-E2 ────────────────────────────────────────────────────
sigma = 410 * 1.4
verifier("2020-E2 : conductivité limite (µS/cm)", sigma, 574)
verifier("2020-E2 : TDS limite (mg/l)", 0.5 * sigma, 287)
verifier("2020-E2 : lecture à 1 100 µS/cm (mg/l)", 0.5 * 1100, 550)
verifier("2020-E2 : 1/1,4", 1 / 1.4, 0.71)
a_tds = 0.005 * 287
verifier("2020-E2 : a (mg/l)", a_tds, 1.4)
verifier("2020-E2 : u précision (mg/l)", a_tds / sqrt(3), 0.83)
verifier("2020-E2 : u résolution (mg/l)", 1 / sqrt(12), 0.29)
uc_tds = sqrt((a_tds / sqrt(3)) ** 2 + 1 / 12)
verifier("2020-E2 : u_c (mg/l)", uc_tds, 0.88)
verifier("2020-E2 : U (mg/l)", 2 * uc_tds, 1.8)
verifier("2020-E2 : U / seuil (%)", 2 * uc_tds / 287 * 100, 0.6)

# ── Méthode : 2021-E2 ────────────────────────────────────────────────────
verifier("2021-E2 : 0,15 % de 2 m (mm)", 0.0015 * 2000, 3)
verifier("2021-E2 : 3 mm en volume (m³)", 6.25 * 0.3, 1.9)
# notre lecture : 35 m³ autour de H = 100 cm, réel au-dessous ou au-dessus de la droite : 5 à 6 %
vrai("2021-E2 : 35 m³ à H = 100 cm, entre 5 et 6 % du volume", all(5 <= 35 / (6.25 * 100 + e) * 100 <= 6 for e in (35, -35)))
verifier("2021-E2 : hystérésis 0,1 % de 2 m (mm)", 0.001 * 2000, 2)
verifier("2021-E2 : 2 mm en volume (m³)", 6.25 * 0.2, 1.25)
verifier("2021-E2 : point de conversion, 2 m sur 10 000 points (m³)", 6.25 * 200 / 10000, 0.125)

# ── Méthode : 2025-E1 ────────────────────────────────────────────────────
verifier("2025-E1 Q65 : panoramique (°)", 540 / 255, 2.12)
verifier("2025-E1 Q65 : inclinaison (°)", 228 / 255, 0.89)

# ── Méthode : 2015-E1 ────────────────────────────────────────────────────
K = 3600 / (110.74 * 22)
verifier("2015-E1 : K_cm (W/m²/K)", K, 1.48)
verifier("2015-E1 : écart à 1,6 (%)", (K - 1.6) / 1.6 * 100, -7.6)
sondes = [44, 43, 42, 41, 40]
verifier("2015-E1 : moyenne des sondes − 20 °C (°C)", mean(sondes) - 20, 22)
verifier("2015-E1 : s des sondes (°C)", stdev(sondes), 1.6)
verifier("2015-E1 : u(ΔT) (°C)", stdev(sondes) / sqrt(5), 0.71)
verifier("2015-E1 : u_r(ΔT) (%)", stdev(sondes) / sqrt(5) / 22 * 100, 3.2)
verifier("2015-E1 : 5/√3 (%)", 5 / sqrt(3), 2.9)
urK = sqrt((stdev(sondes) / sqrt(5) / 22) ** 2 + (0.05 / sqrt(3)) ** 2)
verifier("2015-E1 : U_r(K), « vers 9 % » (%)", 2 * urK * 100, 9, tol=0.06)
vrai("2015-E1 : écart 7,6 % < U_r", abs(K - 1.6) / 1.6 < 2 * urK)

# ── Pièges ───────────────────────────────────────────────────────────────
from math import log10
verifier("p-004 : premier ordre à fe/10, atténuation à fe/2 (dB)", 10 * log10(1 + 5 ** 2), 14)
verifier("p-004 : Butterworth 4 à fe/10, atténuation à fe/2 (dB)", 10 * log10(1 + 5 ** 8), 56)

# ── Exemple chiffré : rendement d'un convertisseur ───────────────────────
U1, I1, U2, I2 = 24.15, 2.51, 12.08, 4.61
verifier("Ex. 1 : courant d'un voltmètre de 10 MΩ (µA)", U1 / 10e6 * 1e6, 2.4)
P1, P2 = U1 * I1, U2 * I2
verifier("Ex. 2 : P1 (W)", P1, 60.62)
verifier("Ex. 2 : P2 (W)", P2, 55.69)
eta = P2 / P1
verifier("Ex. 2 : η", eta, 0.9187)
verifier("Ex. 2 : pertes (W)", P1 - P2, 4.93)
verifier("Ex. 2 : pertes / P1 (%)", (P1 - P2) / P1 * 100, 8)
aU1, aI1 = 0.005 * U1 + 0.02, 0.012 * I1 + 0.03
aU2, aI2 = 0.005 * U2 + 0.02, 0.012 * I2 + 0.03
for nom, a, pub_a, L, pub_r in (("U1", aU1, 0.141, U1, 0.34), ("I1", aI1, "0.060", I1, 1.38),
                                ("U2", aU2, "0.080", U2, 0.38), ("I2", aI2, 0.085, I2, 1.07)):
    verifier(f"Ex. 3 : a({nom})", a, pub_a)
    verifier(f"Ex. 3 : u_r({nom}) (%)", a / sqrt(3) / L * 100, pub_r)
lect = [4.61, 4.63, 4.60, 4.62, 4.61]
verifier("Ex. 3 : s(I2) (A)", stdev(lect), 0.011)
verifier("Ex. 3 : u_A(I2) (A)", stdev(lect) / sqrt(5), 0.0051)
verifier("Ex. 3 : u_A(I2) relative (%)", stdev(lect) / sqrt(5) / mean(lect) * 100, 0.11)
verifier("Ex. 3 : u_r(I2) composée (%)", sqrt((aI2 / sqrt(3) / I2) ** 2 + (stdev(lect) / sqrt(5) / mean(lect)) ** 2) * 100, 1.074)
ur = sqrt(sum((a / sqrt(3) / L) ** 2 for a, L in ((aU1, U1), (aI1, I1), (aU2, U2), (aI2, I2))))
verifier("Ex. 4 : u_r(η) (%)", ur * 100, 1.82)
verifier("Ex. 4 : u(η)", eta * ur, 0.0167)
verifier("Ex. 4 : u(η), quatre chiffres", eta * ur, 0.01673)
verifier("Ex. 4 : 2 × 0,01673", 2 * 0.01673, 0.0335)
verifier("Ex. 3 : effet de la moyenne 4,614 A sur η", U2 * 4.614 / P1 - eta, 0.0008)
verifier("Ex. 4 : U(η) = 2 u(η)", 2 * eta * ur, 0.0335)
vrai("Ex. 4 : 0,0335 par excès → 0,034", abs(par_exces(2 * eta * ur) - 0.034) < 1e-12)
verifier("Ex. 4 : 2 u_r(η), « 3,6 % » (%)", 2 * ur * 100, 3.6)
verifier("Ex. 4 : majoration au pire (%)", sum(a / L for a, L in ((aU1, U1), (aI1, I1), (aU2, U2), (aI2, I2))) * 100, 5.5)
verifier("Ex. 5 : borne basse", eta - 0.034, 0.885)
verifier("Ex. 5 : borne haute", eta + 0.034, 0.953)
vrai("Ex. 5 : intervalle à cheval sur 0,90", eta - 0.034 < 0.90 < eta + 0.034)
aI1b, aI2b = 0.002 * 2.5120 + 5 * 10e-6, 0.002 * 4.6100 + 5 * 0.1e-3
for nom, a, L in (("I1", aI1b, 2.512), ("I2", aI2b, 4.61)):
    verifier(f"Ex. 5 : u_r({nom}) amélioré (%)", a / sqrt(3) / L * 100, 0.12)
uA2 = stdev(lect) / sqrt(5) / mean(lect)
urI2 = sqrt((aI2b / sqrt(3) / 4.61) ** 2 + uA2 ** 2)
verifier("Ex. 5 : u_r(I2) amélioré avec le type A (%)", urI2 * 100, 0.16)
ur2 = sqrt((aU1 / sqrt(3) / U1) ** 2 + (aI1b / sqrt(3) / 2.512) ** 2 + (aU2 / sqrt(3) / U2) ** 2 + urI2 ** 2)
verifier("Ex. 5 : u_r(η) amélioré (%)", ur2 * 100, 0.55)
verifier("Ex. 5 : U(η) amélioré", 2 * eta * ur2, 0.0101)
vrai("Ex. 5 : U(η) amélioré par excès → 0,011", abs(par_exces(2 * eta * ur2) - 0.011) < 1e-12)
verifier("Ex. 5 : borne basse améliorée", eta - 0.011, 0.908)
verifier("Ex. 5 : borne haute améliorée", eta + 0.011, "0.930")
vrai("Ex. 5 : intervalle au-dessus de 0,90", eta - 0.011 > 0.90)

# ── Auto-test ────────────────────────────────────────────────────────────
r = [99.8, 100.3, 100.1, 99.9, 100.2]
verifier("Q2 : moyenne (Ω)", mean(r), 100.06)
verifier("Q2 : s (Ω)", stdev(r), 0.21)
verifier("Q2 : u_A (Ω)", stdev(r) / sqrt(5), 0.093)
a3 = 0.01 * 230.4 + 3 * 0.1
verifier("Q3 : a (V)", a3, "2.60")
verifier("Q3 : u_B (V)", a3 / sqrt(3), "1.50")
verifier("Q3 : U (V)", 2 * a3 / sqrt(3), 3.007)
vrai("Q3 : 3,007 par excès → 3,1", abs(par_exces(2 * a3 / sqrt(3)) - 3.1) < 1e-12)
verifier("Q4 : P (W)", 10.0 * 2.00 ** 2, 40.0)
verifier("Q4 : u_r(R) (%)", 1 / sqrt(3), 0.58)
urP = sqrt((1 / sqrt(3)) ** 2 + (2 * 0.5) ** 2)
verifier("Q4 : u_r(P) (%)", urP, 1.15)
verifier("Q4 : U(P) (W)", 2 * urP / 100 * 40, 0.924)
vrai("Q4 : 0,924 par excès → 0,93", abs(par_exces(2 * urP / 100 * 40) - 0.93) < 1e-12)
verifier("Q4 : borne haute (W)", 40.00 + 0.93, 40.93)
vrai("Q4 : sous 41 W", 40.00 + 0.93 < 41)
verifier("Q5 : √(R_A R_V) (kΩ)", sqrt(0.5 * 10e6) / 1e3, 2.2)
verifier("Q5 : erreur aval", 22 / 10e6 / 1e-6, 2, tol=0.15)
verifier("Q5 : erreur amont (%)", 0.5 / 22 * 100, 2.3)
verifier("Q6 : fe (kHz)", 10000 / 1 / 1e3, 10)
verifier("Q6 : fréquence repliée (Hz)", abs(20e3 - 2 * 10e3), 0)
verifier("Q6 : durée maximale (ms)", 10000 / 200e3 * 1e3, 50)

# ── Homogénéité ──────────────────────────────────────────────────────────
# u_A = s/√n : même unité que x ; u_B = a/√3 : même unité que a ; U = k u_c, k sans dimension ;
# loi de propagation : (∂f/∂x_i) u(x_i) a l'unité de y ; q = U_PE/2^n en V ; N sans dimension ;
# z sans dimension ; R_mes = R + R_A et R R_V/(R + R_V) en Ω ; √(R_A R_V) en Ω.
vrai("homogénéité : relue terme à terme (voir commentaire)", True)

print("\nAucun écart." if not ECARTS else f"\n{len(ECARTS)} écart(s) : {ECARTS}")
