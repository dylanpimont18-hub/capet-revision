"""Applications numériques du chapitre T22, refaites en Python.

    python3 cours/calculs/T22.py

Chaque bloc reprend une valeur publiée dans cours/textes/T22.html ; un
écart supérieur à la demi-unité du dernier chiffre publié fait échouer le
script (tolérance relative explicite pour une valeur annoncée « environ »).
"""
from decimal import Decimal
from math import sqrt, log10, log2, pi, cos, floor, ceil

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


def hexa(n):
    return format(n, 'X')


# ── §2 : échantillonnage ─────────────────────────────────────────────────
for f, fe, m in ((9e3, 10e3, 1), (1e3, 800, 1), (1.5e3, 800, 2), (50, 10, 5)):
    # même échantillons pour f et |f − m fe|
    vrai(f"§2 : {f:g} Hz et |f − {m} fe| donnent les mêmes échantillons à {fe:g} Hz",
         all(abs(cos(2 * pi * f * k / fe) - cos(2 * pi * abs(f - m * fe) * k / fe)) < 1e-9 for k in range(50)))
verifier("§2 : fréquence apparente de 9 kHz à 10 kHz (Hz)", abs(9e3 - 10e3), 1000)
vrai("§2 : à fe = 2 fmax, sinusoïde échantillonnée à ses zéros", all(abs(__import__('math').sin(pi * k)) < 1e-9 for k in range(20)))
# échantillonneur-bloqueur : 2π f A Tconv ≤ q/2, 12 bits, A = Vref/2, Tconv = 10 µs
fmax_eb = (1 / 4096) / 2 / (2 * pi * 0.5 * 10e-6)
verifier("§2 : fréquence limite sans bloqueur (Hz), « environ »", fmax_eb, 3.9)

# ── §3 : quantification ──────────────────────────────────────────────────
verifier("§3 : écart des conventions sur 8 bits (%)", 100 / 255, 0.4)
verifier("§3 : écart des conventions sur 12 bits (%)", 100 / 4095, 0.02)
q1 = 10 / 4096
verifier("§3 : q = 10/4096 (mV)", q1 * 1e3, 2.441)
verifier("§3 : 4,5/q (convention 2^n)", 4.5 / q1, 1843.2)
verifier("§3 : N (convention 2^n)", floor(4.5 / q1), 1843)
q2 = 10 / 4095
verifier("§3 et f-009 : q = 10/4095 (mV)", q2 * 1e3, 2.442)
verifier("§3 : 4,5/q (convention 2^n − 1)", 4.5 * 4095 / 10, 1842.75)
verifier("§3 : N (convention 2^n − 1)", floor(4.5 * 4095 / 10), 1842)
vrai("f-009 : 1842 = 0x732 ; 1843 = 0x733", hexa(1842) == '732' and hexa(1843) == '733')
# bruit de quantification et RSB
import numpy as np
e = np.linspace(-0.5, 0.5, 200001)
verifier("§3 : valeur efficace de ε, uniforme sur q (en q)", sqrt(np.mean(e ** 2)), 1 / sqrt(12), tol=1e-4)
for n, rsb in ((8, 50), (12, 74), (16, 98)):
    verifier(f"§3 : RSB idéal sur {n} bits (dB)", 20 * log10(2 ** n * sqrt(1.5)), rsb)
    verifier(f"§3 : 6,02 n + 1,76 sur {n} bits (dB)", 6.02 * n + 1.76, rsb)
verifier("§3 : nombre de bits, 0 à 150 °C au dixième", ceil(log2(1500)), 11)
vrai("§3 : 2^10 = 1024 < 1500 ≤ 2048 = 2^11", 2 ** 10 < 1500 <= 2 ** 11)

# ── §4 : codage ──────────────────────────────────────────────────────────
vrai("§4 : 0111 0011 0010 = 0x732 = 1842 = 7×256 + 3×16 + 2",
     int('011100110010', 2) == 0x732 == 1842 == 7 * 256 + 3 * 16 + 2)
vrai("§4 : 1 0110 1101 = 0x16D = 365", int('101101101', 2) == 0x16D == 365)
vrai("§4 : 1842 = 115×16 + 2 et 115 = 7×16 + 3", 1842 == 115 * 16 + 2 and 115 == 7 * 16 + 3)
for v, c2, dec in ((3, '011', '111'), (1, '001', '101'), (0, '000', '100'), (-1, '111', '011'), (-4, '100', '000')):
    vrai(f"§4 : {v} en complément à deux {c2}, en binaire décalé {dec}",
         format(v & 0b111, '03b') == c2 and format(v + 4, '03b') == dec)
vrai("§4 : 16 bits signés de −32768 à 32767", -2 ** 15 == -32768 and 2 ** 15 - 1 == 32767)
vrai("piège p-006 : grouper depuis le MSB donne B6 suivi d'un bit", hexa(int('1011', 2)) + hexa(int('0110', 2)) == 'B6')

# ── §5 : CAN ─────────────────────────────────────────────────────────────
# approximations successives, 4 bits, VE = 11,3 q
ve, code, essais = 11.3, 0, []
for b in range(3, -1, -1):
    essai = code | (1 << b)
    essais.append(essai)
    if essai <= ve:
        code = essai
vrai("§5 : essais 8, 12, 10, 11 et N = 1011", essais == [8, 12, 10, 11] and code == 0b1011)
verifier("§5 : comparateurs d'un flash de 8 bits", 2 ** 8 - 1, 255)
verifier("§5 : fe maximale à 10 µs par conversion (kHz)", 1 / 10e-6 / 1e3, 100)
# double rampe : charge à pente VE/RC pendant T1, décharge à pente Vref/RC ; T2 indépendant de R, C
for RC in (1e-3, 4.7e-3):
    T1, VE_, Vref_ = 20e-3, 1.25, 5.0
    vmax = VE_ / RC * T1
    T2 = vmax / (Vref_ / RC)
    verifier(f"§5 : double rampe, T2/T1 pour VE = Vref/4, RC = {RC:g} s", T2 / T1, 0.25)
verifier("§5 : fe = 100 kHz, signal utile à 10 fe (kHz)", 100 / 10, 10)
verifier("§5 : fe = 100 kHz, signal utile à 5 fe (kHz)", 100 / 5, 20)
verifier("§5 : limite de Shannon (kHz)", 100 / 2, 50)

# ── §6 : CNA ─────────────────────────────────────────────────────────────
verifier("§6 : pas d'un CNA de 8 bits sous 5 V (mV)", 5 / 256 * 1e3, 19.5)


def r2r(bits, vref=1.0):
    """Réseau R-2R en tension : Thévenin de proche en proche depuis le LSB (bits = b0, b1, …)."""
    e, r = 0.0, 2.0                       # fermeture 2R à la masse
    for b in bits:
        # branche b : 2R vers b·Vref, en parallèle avec (e, r)
        e = (e / r + b * vref / 2.0) / (1 / r + 1 / 2.0)
        r = 1 / (1 / r + 1 / 2.0)
        vrai_r = abs(r - 1.0) < 1e-12
        r += 1.0                          # résistance R vers le nœud suivant
    return e, vrai_r


for n in range(16):
    bits = [(n >> i) & 1 for i in range(4)]
    vs, rth = r2r(bits)
    if not (abs(vs - n / 16) < 1e-12 and rth):
        ECARTS.append(f"R-2R code {n}")
vrai("§6 : R-2R de 4 bits, VS = N Vref/16 pour les 16 codes, Thévenin R à chaque nœud",
     not any(e_.startswith('R-2R') for e_ in ECARTS))
verifier("§5 : gain du suréchantillonnage seul par doublement de fe (bit)", 10 * log10(2) / 6.02, 0.5)

# ── §7 : sensibilité et mise à l'échelle ─────────────────────────────────
q5 = 5 / 4096
verifier("§7 : q sous 5 V, 12 bits (mV)", q5 * 1e3, 1.22)
S = 0.010 * 4 / q5
verifier("§7 : S (points par °C)", S, 32.8)
verifier("§7 : résolution 1/S (°C)", 1 / S, 0.03)
verifier("§7 : 16 mA / 27 648 (nA)", 16e-3 / 27648 * 1e9, 578.7)
vrai("§7 : 27 648 = 0x6C00, 32 511 = 0x7EFF, 32 767 = 0x7FFF, −4 864 = 0xED00",
     hexa(27648) == '6C00' and hexa(32511) == '7EFF' and hexa(32767) == '7FFF' and hexa(-4864 & 0xFFFF) == 'ED00')
verifier("§7 : courant pour 32 511 (mA)", 4 + 32511 * 16 / 27648, 22.81)
verifier("§7 : courant pour −4 864 (mA)", 4 - 4864 * 16 / 27648, 1.185)
verifier("§7 : 220/27 648 en division entière", 220 // 27648, 0)

# ── Méthode : 2022-E1 ────────────────────────────────────────────────────
qp = 3.5 / 4096
verifier("2022-E1 Q24 : q (mV)", qp * 1e3, 0.854)
verifier("2022-E1 Q24 : N pour 1 V (2^n)", floor(1 / qp), 1170)
verifier("2022-E1 Q24 : N pour 1 V (2^n − 1)", floor(1 / (3.5 / 4095) + 1e-9), 1170)
vrai("2022-E1 Q24 : 1170 = 0x492 ; 0xAF = 175", hexa(1170) == '492' and 0xAF == 175)
verifier("2022-E1 Q24 : 175 q (V)", 175 * qp, "0.150")
verifier("2022-E1 Q24 : tension du Peltier (V)", 2 * 175 * qp, "0.30")
vrai("2022-E1 Q25 : ADCON0 = 00 0010 1 1 = 0x0B", int('00001011', 2) == 0x0B)
verifier("2022-E1 Q27 : seuil de conduction de D1 (mA)", 0.6 / 23.7 * 1e3, 25)
verifier("2022-E1 Q30 : ADC2 pour 2 574 (V), 2^n − 1", 2574 * 3.5 / 4095, "2.200")
verifier("2022-E1 Q30 : tension du Peltier (V)", 2 * 2574 * 3.5 / 4095, 4.4)
verifier("2022-E1 Q30 : ADC2 avec 4 096 (V)", 2574 * 3.5 / 4096, 2.1995)
verifier("2022-E1 Q27 : coupure de R1 C (Hz), notre lecture", 1 / (2 * pi * 2500 * 1e-6), 64)
verifier("2022-E1 Q30 : n = 4096 (1 − 12,176/32,768)", 4096 * (1 - 12.176 / 32.768), 2574)

# ── Méthode : 2023-E2 ────────────────────────────────────────────────────
qb = 4 / 1024
verifier("2023-E2 F3 : q (mV)", qb * 1e3, 3.906)
verifier("2023-E2 F3 : N à 80 %", floor(2.24 / qb), 573)
verifier("2023-E2 F3 : N à 90 %", floor(2.18 / qb), 558)
verifier("2023-E2 F4 : quantum en points de décharge (%)", qb / (0.060 / 10), 0.65)
verifier("2023-E2 D2 : impulsions", floor(680 / 0.15 + 1e-9), 4533)
vrai("2023-E2 D2 : 13 bits pour 4 534 positions", 2 ** 12 < 4534 <= 2 ** 13)
vrai("2023-E2 D2 : 4 533 = 1 0001 1011 0101 = 0x11B5", format(4533, 'b') == '1000110110101' and hexa(4533) == '11B5')
verifier("2023-E2 D3 : pas sur 8 bits de poids fort (mm)", 2 ** 5 * 0.15, 4.8)
vrai("2023-E2 D3 : 4 533 >> 5 = 141 = 1000 1101 = 0x8D", 4533 >> 5 == 141 == 0x8D and format(141, '08b') == '10001101')

# ── Méthode : 2025-E1 ────────────────────────────────────────────────────
verifier("2025-E1 Q19 : 2^24", 2 ** 24, 16777216)
vrai("2025-E1 Q19 : 2^24 − 1 = 16 777 215 = 0xFFFFFF", 2 ** 24 - 1 == 16777215 == 0xFFFFFF)
dth = 288 / (2 ** 24 - 1)
verifier("2025-E1 Q23 : Δθ (°)", dth, 1.72e-5)
verifier("2025-E1 Q24 : Δθ (rad)", dth * pi / 180, 2.996e-7)
verifier("2025-E1 Q24 : déplacement de M (mm)", 1460 * dth * pi / 180, 4.4e-4)
n17 = ceil(log2((288 * pi / 180) / (0.1 / 1460) + 1))
verifier("2025-E1 Q24 : bits minimaux (notre calcul)", n17, 17)
verifier("2025-E1 Q24 : pas sur 17 bits (mm)", 1460 * 288 * pi / 180 / (2 ** 17 - 1), 0.056)
dV = 10 / (2 ** 24 - 1)
verifier("2025-E1 Q26 : ΔV (µV)", dV * 1e6, 0.596)
verifier("2025-E1 Q27 : log2(10/(ΔV/10))", log2(10 / (dV / 10)), 27.3)
verifier("2025-E1 Q27 : bits", ceil(log2(10 / (dV / 10))), 28)
verifier("2025-E1 Q27 : bits avec q/2", ceil(log2(10 / (2 * dV / 10))), 27)
verifier("2025-E1 Q27 : quantum sur 28 bits (nV)", 10 / 2 ** 28 * 1e9, 37)
verifier("2025-E1 Q65 : pas Pan (°)", 540 / 255, 2.12)
verifier("2025-E1 Q65 : pas Tilt (°)", 228 / 255, 0.89)
verifier("2025-E1 Q66 : 30 × 255/540", 30 * 255 / 540, 14.2)
verifier("2025-E1 Q66 : 60 × 255/228", 60 * 255 / 228, 67.1)
vrai("2025-E1 Q66 : 14 = 0000 1110 ; 67 = 0100 0011", format(14, '08b') == '00001110' and format(67, '08b') == '01000011')
verifier("2025-E1 Q66 : depuis 128, Pan", 128 + floor(30 * 255 / 540), 142)
verifier("2025-E1 Q66 : depuis 128, Tilt", 128 + floor(60 * 255 / 228), 195)
verifier("2025-E1 Q21 : impulsion pour 60° (µs)", 1000 + 1000 * 150 / 180, 1833)
verifier("2025-E1 Q21 : durée à zéro (µs)", 20000 - (1000 + 1000 * 150 / 180), 18167)
verifier("2025-E1 Q21 : 1000/1800 (µs)", 1000 / 1800, 0.556)
verifier("2025-E1 Q21 : fréquence d'échantillonnage (MHz)", 1 / (1000e-6 / 1800) / 1e6, 1.8)

# ── Méthode : 2024-E2 ────────────────────────────────────────────────────
verifier("2024-E2 D7 : 27 648/16", 27648 / 16, 1728)
for i, p in ((1.185, -4864), (4, 0), (20, 27648)):
    verifier(f"2024-E2 D7 : PIW8 à {i} mA", 1728 * (i - 4), p, tol=1e-4 if p else None)
verifier("2024-E2 D7 : PIW8 calculé à 22,81 mA", 1728 * (22.81 - 4), 32504)
verifier("2024-E2 D10 : 220/27 648", 220 / 27648, 7.957e-3)
verifier("2024-E2 D12 : PIW8 pour 35 °C", 27648 * 55 / 220, 6912)
verifier("2024-E2 D12 : PIW8 pour 50 °C", 27648 * 70 / 220, 8797.1)
verifier("figure 16 : 8 mA donnent 6 912", 1728 * (8 - 4), 6912)

# ── Méthode : 2021-E2 ────────────────────────────────────────────────────
verifier("2021-E2 Q23 : N/H (points par cm)", 10000 / 200, 50)
verifier("2021-E2 Q23 : V/N (m³)", 6.25 / 50, 0.125)
verifier("2021-E2 Q23 : N à 1,6 m", 50 * 160, 8000)

# ── Exemple chiffré : four ───────────────────────────────────────────────
qf = 5 / 1024
verifier("Ex. 1 : q (mV)", qf * 1e3, 4.883)
verifier("Ex. 1 : transmetteur (mV/°C)", 5000 / 400, 12.5)
Sf = 0.0125 / qf
verifier("Ex. 1 : S (points par °C)", Sf, 2.56)
verifier("Ex. 1 : 1/S (°C)", 1 / Sf, 0.39)
VE = 237 * 0.0125
verifier("Ex. 2 : VE à 237 °C (mV)", VE * 1e3, 2962.5)
verifier("Ex. 2 : VE/q", VE / qf, 606.72)
vrai("Ex. 2 : N = 606 = 10 0101 1110 = 0x25E",
     floor(VE / qf) == 606 and format(606, 'b') == '1001011110' and hexa(606) == '25E')
vrai("Ex. 2 : 0x1F4 = 1×256 + 15×16 + 4 = 500", 0x1F4 == 500 == 256 + 240 + 4)
verifier("Ex. 2 : 500 q (V)", 500 * qf, 2.441)
verifier("Ex. 2 : température (°C)", 500 * qf / 0.0125, 195.3)
verifier("Ex. 2 : marche suivante (°C)", 501 * qf / 0.0125, 195.7)
vrai("Ex. 3 : 4 000 intervalles, 2^11 < 4000 ≤ 2^12", 2 ** 11 < 4000 <= 2 ** 12)
verifier("Ex. 3 : q sur 12 bits (mV)", 5 / 4096 * 1e3, 1.22)
verifier("Ex. 3 : en °C", 5 / 4096 / 0.0125, 0.098)
verifier("Ex. 4 : erreur maximale du ronflement (°C)", 20 / 12.5, 1.6)
verifier("Ex. 4 : atténuation du RC à 50 Hz", sqrt(1 + 50 ** 2), 50)
verifier("Ex. 4 : ronflement résiduel (mV)", 20 / sqrt(1 + 50 ** 2), 0.4)
verifier("Ex. 4 : q/2 (mV)", qf / 2 * 1e3, 2.4)
verifier("Ex. 4 : erreur résiduelle (°C)", 20 / sqrt(1 + 50 ** 2) / 12.5, 0.03)
vrai("Ex. 5 : plus de 7 000 conversions dans 100 ms", 0.1 / 13e-6 > 7000)
qc = 10 / 256
verifier("Ex. 5 : pas du CNA (mV)", qc * 1e3, 39.06)
verifier("Ex. 5 : pas en % de puissance", qc / 10 * 100, 0.39)
verifier("Ex. 5 : 6,2/q", 6.2 / qc, 158.7)
verifier("Ex. 5 : entier le plus proche", round(6.2 / qc), 159)
vrai("Ex. 5 : 159 = 0x9F", hexa(159) == '9F')
verifier("Ex. 5 : VS (V)", 159 * qc, 6.21)
verifier("Ex. 5 : puissance obtenue (%)", 159 * qc * 10, 62.1)
verifier("Ex. 5 : puissance avec 158 (%)", 158 * qc * 10, 61.7)

# ── Auto-test ────────────────────────────────────────────────────────────
verifier("Q1 : q sur 8 bits (mV)", 5 / 256 * 1e3, 19.5)
verifier("Q1 : 3/q", 3 / (5 / 256), 153.6)
vrai("Q1 : 153 = 0x99", hexa(153) == '99')
vrai("Q2 : 1 1010 0111 = 0x1A7 = 423 ; 0x3FF = 1023",
     int('110100111', 2) == 0x1A7 == 423 == 256 + 160 + 7 and 0x3FF == 1023 == 768 + 240 + 15)
vrai("Q3 : 3 000 intervalles, 12 bits", 2 ** 11 < 3000 <= 2 ** 12)
verifier("Q4 : 1 kHz à 800 Hz (Hz)", abs(1000 - 800), 200)
verifier("Q4 : 1,5 kHz à 800 Hz (Hz)", abs(1500 - 1600), 100)
verifier("Q5 : Tconv (µs)", 14 / 2e6 * 1e6, 7)
verifier("Q5 : fe maximale (kHz)", 2e6 / 14 / 1e3, 143)
verifier("Q5 : fmax à 10 fe (kHz)", 2e6 / 14 / 10 / 1e3, 14)
verifier("Q5 : fmax à 5 fe (kHz)", 2e6 / 14 / 5 / 1e3, 29)
verifier("Q5 : RSB (dB)", 6.02 * 12 + 1.76, 74)
verifier("Q6 : 0xC0 sous 5 V (V)", 0xC0 * 5 / 256, 3.75)
verifier("Q6 : 1 V × 256/5", 256 / 5, 51.2)
vrai("Q6 : 51 = 0x33", hexa(51) == '33')
verifier("Q6 : 51 q (V)", 51 * 5 / 256, 0.996)

print("\nAucun écart." if not ECARTS else f"\n{len(ECARTS)} écart(s) : {ECARTS}")
