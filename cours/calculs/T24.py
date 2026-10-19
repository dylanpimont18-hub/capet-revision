"""Applications numériques du chapitre T24, refaites en Python.

    python3 cours/calculs/T24.py

Chaque valeur publiée dans cours/textes/T24.html est recalculée ; les
débordements d'entiers sont simulés sur 16 bits. Un écart fait échouer le
script.
"""
import math
import sys
from decimal import Decimal

ECARTS = []


def verifier(nom, calcule, publie, tol=None):
    """Écart admis : la demi-unité du dernier chiffre publié, sauf tolérance relative explicite."""
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


def int16(x):
    """Valeur d'un calcul entier tronqué à 16 bits signés."""
    x &= 0xFFFF
    return x - 0x10000 if x & 0x8000 else x


# ── §3 : scrutation ─────────────────────────────────────────────────────
v, R = 60 / 3.6, 0.20
n = v / (2 * math.pi * R) * 60
verifier("§3 / carte f-001 : 2024-E1, vitesse de la roue (tr/min)", n, "795.8")
verifier("§3 / carte f-001 : 2024-E1, f par voie (Hz)", 100 * n / 60, "1326")

# ── §4 : temporisateurs, MLI, servomoteur ───────────────────────────────
f_timer = 16e6 / 8
verifier("§4 : pas d'un temporisateur à 16 MHz / 8 (µs)", 1e6 / f_timer, "0.5")
verifier("§4 : période avec TOP = 39 999 (ms)", (39999 + 1) / f_timer * 1e3, "20")
vrai("§4 : TOP = 39 999 exige 16 bits", 255 < 39999 < 65536)
verifier("§4 : analogWrite, 16 MHz / 64 (kHz)", 16e6 / 64 / 1e3, "250")
verifier("§4 : phase correcte, 2 × 255 / 250 kHz (ms)", 2 * 255 / 250e3 * 1e3, "2.04")
verifier("§4 : soit (Hz)", 250e3 / 510, "490")
verifier("§4 : broches 5 et 6, MLI rapide, 250 kHz / 256 (Hz)", 250e3 / 256, "976", tol=0.001)
t_on = lambda th: 1.5 + th / 180
verifier("§4 : servomoteur, t_on à 60° (ms)", t_on(60), "1.833")
verifier("§4 : 0,1° en durée (µs)", 0.1 / 180 * 1000, "0.556")
vrai("§4 : t_on = 1 ms à −90°, 2 ms à +90°", abs(t_on(-90) - 1) < 1e-12 and abs(t_on(90) - 2) < 1e-12)

# ── §5 : conversion et mise à l'échelle ─────────────────────────────────
verifier("§5 : 4 mA sur 250 Ω (V)", 0.004 * 250, "1")
verifier("§5 : 20 mA sur 250 Ω (V)", 0.020 * 250, "5")
verifier("§5 : 1 024/5 à 1 V", 1024 * 1 / 5, "204.8")
vrai("§5 : 204 par troncature, 205 à l'arrondi", int(1024 / 5) == 204 and round(1024 / 5) == 205)
vrai("§5 : N pour 5 V sature à 1 023", min(int(1024 * 5 / 5), 1023) == 1023)
adcon0 = lambda voie, go=1, adon=1: (voie << 2) | (go << 1) | adon
verifier("§5 / fig. 8 : AN2, conversion lancée", adcon0(2), str(0x0B))
verifier("§5 : AN2 en service, sans lancer", adcon0(2, go=0), str(0x09))
vrai("§5 : 0x0B = 0000 1011", f"{adcon0(2):08b}" == "00001011")
verifier("§6 : 0x0336 / 16 (°C)", 0x0336 / 16, "51.375")

# ── §7 : entiers ────────────────────────────────────────────────────────
verifier("§7 / fig. 12 : 60*60*1000 en int 16 bits", int16(60 * 60 * 1000), "-4480")
verifier("§7 : 220/27 648 en division entière", 220 // 27648, "0")
vrai("§7 : −7/2 vaut −3 en C (troncature), −7 // 2 vaut −4 en Python", int(-7 / 2) == -3 and -7 // 2 == -4)
verifier("Q4 : −4 480 converti en unsigned long (ms)", (-4480) % 2 ** 32, "4294962816")
verifier("Q4 : soit en jours", ((-4480) % 2 ** 32) / 86400e3, "49.7", tol=0.002)

# ── Exemple ─────────────────────────────────────────────────────────────
T = lambda N: -10 + 60 * (N - 205) / (1023 - 205)
verifier("ex. 1 : T pour N = 512 (°C)", T(512), "12.5")
verifier("ex. 1 : un point (°C)", 60 / 818, "0.073")
verifier("ex. 2 : 3,6 mA sur 250 Ω (V)", 0.0036 * 250, "0.9")
verifier("ex. 2 : seuil de défaut N", 1024 * 0.9 / 5, "184")
verifier("ex. 2 : 21 mA sur 250 Ω (V)", 0.021 * 250, "5.25")
vrai("fig. 9 : bande de défaut sous 3,6 mA, N ≤ 184", int(1024 * 0.9 / 5) == 184)
verifier("ex. 3 : f_max du capteur à effet Hall (Hz)", 2 * 3000 / 60, "100")
verifier("ex. 3 : période des impulsions (ms)", 1000 / 100, "10")
verifier("ex. 3 : une impulsion par seconde vaut (tr/min)", 60 / 2, "30")
verifier("ex. 3 : soit du régime maximal (%)", 100 * 30 / 3000, "1")


def fenetres(n_reel, boucle_ms, duree_ms=120000, corrige=True):
    """Simule la boucle de l'exemple : impulsions à 2 par tour, lecture quand millis() - t0 >= 1 000."""
    f = 2 * n_reel / 60
    t, t0, lu, mesures = 0.0, 0.0, 0.0, []
    while t < duree_ms:
        t += boucle_ms
        if t - t0 >= 1000:
            k = math.floor(t * f / 1000) - math.floor(lu * f / 1000)
            lu = t
            if corrige:
                mesures.append(30000 * k / (t - t0))
                t0 = t
            else:
                mesures.append(30 * k)
                t0 += 1000
    return mesures[1:]


m_nouveau = fenetres(3000, 100.2)
vrai("ex. 3 : divisé par la durée réelle, écart d'une impulsion au plus",
     max(abs(x - 3000) for x in m_nouveau) <= 30 * 1.001)
vrai("ex. 6 : 30000L * k tient dans un long", 30000 * 110 < 2 ** 31)
alpha = (26 - 20) / 10
verifier("ex. 4 : α à 26 °C", alpha, "0.6")
verifier("ex. 4 : consigne analogWrite", alpha * 255, "153")
verifier("ex. 4 : période à 490 Hz (ms)", 1000 / 490, "2.04")
verifier("ex. 4 : t_on (ms)", alpha * 1000 / 490, "1.22")
verifier("ex. 4 : tension moyenne (V)", alpha * 12, "7.2")
verifier("ex. 5 : (1 023 − 205) × 60", (1023 - 205) * 60, "49080")
vrai("ex. 5 : 49 080 déborde un int de 16 bits", int16(49080) != 49080)
verifier("ex. 5 : conversion, 13 cycles à 125 kHz (ms)", 13 / 125e3 * 1e3, "0.1", tol=0.05)

# ── Auto-test ───────────────────────────────────────────────────────────
verifier("Q2 : codeur 500 pts à 1 500 tr/min (Hz)", 500 * 1500 / 60, "12500")
verifier("Q2 : une impulsion toutes les (µs)", 1e6 / 12500, "80")
verifier("Q2 : limite d'une scrutation à 1 ms (Hz)", 1 / (2 * 1e-3), "500")
verifier("Q3 : AN5, conversion lancée", adcon0(5), str(0x17))
vrai("Q3 : 0x17 = 0001 0111", f"{adcon0(5):08b}" == "00010111")


def depasse(mesures, seuil):
    i = 0
    while i < len(mesures):
        if mesures[i] > seuil:
            return i
        i = i + 1
    return -1


vrai("Q5 : depasse([1, 5, 9], 4) = 1 ; [] → −1 ; égalité non retenue",
     depasse([1, 5, 9], 4) == 1 and depasse([], 4) == -1 and depasse([4, 4], 4) == -1)
verifier("Q6 : t_on à −45° (ms)", t_on(-45), "1.25")
verifier("Q6 : en pas de 0,5 µs", t_on(-45) * 1000 / 0.5, "2500")
verifier("Q6 : un pas en angle (°)", 180 * 0.5 / 1000, "0.09")

# ── Méthode ─────────────────────────────────────────────────────────────
verifier("2025-E1 Q68 : 5 s / 25 ms", 5 / 0.025, "200")
i, trames = 0, 0
while True:
    trames += 1
    i += 1
    if i == 200:
        break
vrai("2025-E1 Q68 : incrément avant le test, 200 trames", trames == 200)
verifier("2018-E1 Q23 : d_max = V Cr / (60 Ci), coefficient", 5 * 1.8 / 60, "0.15")
verifier("2021-E2 Q24 : V pour N = 8 000 (m³)", 0.125 * 8000, "1000")
verifier("2021-E1 Q26 : Kcod (mm par incrément)", 2 * math.pi * 0.18 / 500 * 1e3, "2.26")
verifier("2020-E1 Q14 : pas p = π m (mm)", math.pi * 3.18, "9.99")
verifier("2020-E1 Q13 : Hf = D1 + (i − 1) Dist − 10 − Dec pour i = 24 (mm)", 300 + 23 * 400 - 10 - 100, "9390")
verifier("2020-E1 Q14 : Nf pour Hf = 9 390 mm", 9390 / (math.pi * 3.18), "940")
verifier("2021-E2 Q24 : 95 % du volume (m³)", 0.95 * 1000, "950")
verifier("2021-E2 Q24 : 5 % du volume (m³)", 0.05 * 1000, "50")
verifier("2018-E2 Q24 : rampe (V/min)", (220 - 190) / 10, "3")
verifier("2023-E1 Q57 : C/200 d'après Q54", 167.96 / 200, "0.84")
vrai("2023-E1 Q57 : C/200 = 0,84 → Nouv = 3", (1 if 0.84 < 0.33 else 2 if 0.84 < 0.66 else 3) == 3)

# ── §9 : compteur VHDL, simulé comme son process (RAZ asynchrone prioritaire, front montant) ──
def compteur_vhdl(evenements):
    """evenements : suite de (h, raz) ; le process réagit à tout changement de h ou de raz."""
    n, h_avant, sorties = 0, 0, []
    for h, raz in evenements:
        if raz == 1:
            n = 0
        elif h == 1 and h_avant == 0:          # rising_edge(h)
            n = (n + 1) % 16                   # unsigned(3 downto 0) : modulo 16
        h_avant = h
        sorties.append(n)                      # q <= n, affectation concurrente
    return sorties
horloge = [(h, 0) for _ in range(20) for h in (1, 0)]
vrai("§9 : 17 fronts montants mènent à 1 (modulo 16)", compteur_vhdl(horloge[:34])[-1] == 17 % 16)
vrai("§9 : après 1111 vient 0000", compteur_vhdl(horloge[:32])[-1] == 0 and compteur_vhdl(horloge[:30])[-1] == 15)
vrai("§9 : seuls les fronts montants comptent", compteur_vhdl([(1, 0), (1, 0), (0, 0), (0, 0)]) == [1, 1, 1, 1])
vrai("§9 : RAZ asynchrone, sans front d'horloge", compteur_vhdl([(1, 0), (0, 0), (1, 0), (1, 1)])[-1] == 0)
vrai("§9 : RAZ prioritaire sur un front montant simultané", compteur_vhdl([(1, 0), (0, 0), (1, 1)])[-1] == 0)
texte = open("cours/textes/T24.html", encoding="utf-8").read()
import re as _re, html as _html
bloc = _re.search(r"<pre><code>(library ieee;[\s\S]*?)</code></pre>", texte)
vrai("§9 : extrait VHDL présent, lignes de 36 caractères au plus",
     bool(bloc) and max(len(l) for l in _html.unescape(bloc.group(1)).split("\n")) <= 36)

# ── 2024-E1, Q68 : galets, d'après sa figure 2 (ordre et côté des voies) et la règle du texte ──
ORDRE = ["station 1", "maintenance", "station 2"]          # sens de parcours, en boucle
COTE = {"station 1": "droite", "maintenance": "gauche", "station 2": "droite"}
def trajet(depart, galets_bas):
    """La capsule prend la voie du côté où ses galets sont en bas ; elle s'arrête à la première voie prise."""
    i = ORDRE.index(depart)
    for k in range(1, 4):
        lieu = ORDRE[(i + k) % 3]
        if COTE[lieu] == galets_bas:
            return lieu
vrai("Q68 : se garer en station = galets droits en bas (texte du sujet)", COTE["station 1"] == COTE["station 2"] == "droite")
galets = "droite"                                          # position d'arrivée à la station 1
vrai("Q68 : départ de la station 1, destination 2, sans changement", trajet("station 1", galets) == "station 2")
vrai("Q68 : destination 0 : galets gauches en bas", trajet("station 1", "gauche") == "maintenance")
vrai("figure 22 : départ de la maintenance, destination 2, galets droits en bas", trajet("maintenance", "droite") == "station 2")
vrai("figure 22 : la branche destination 1, sans changement, ne mène pas à la station 1 (réserve)",
     trajet("maintenance", "gauche") != "station 1")

print("\nAucun écart." if not ECARTS else f"\n{len(ECARTS)} écart(s) : {ECARTS}")
sys.exit(1 if ECARTS else 0)
