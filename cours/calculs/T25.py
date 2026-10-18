"""Applications numériques du chapitre T25, refaites en Python.

    python3 cours/calculs/T25.py

Chaque valeur publiée dans cours/textes/T25.html est recalculée ; les trames
série, l'arbitrage et le bourrage CAN, les adresses IP sont simulés. Un écart
fait échouer le script.
"""
import ipaddress
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


def trame_uart(octet, parite="paire", stops=1):
    """Bits émis pour un octet : start, données poids faible d'abord, parité, stop."""
    d = [(octet >> k) & 1 for k in range(8)]
    bits = [0] + d
    if parite == "paire":
        bits.append(sum(d) % 2)
    return bits + [1] * stops


def lire_uart(bits, parite="paire"):
    """Décode une trame : renvoie l'octet et la validité de la parité."""
    assert bits[0] == 0
    d = bits[1:9]
    octet = sum(b << k for k, b in enumerate(d))
    ok = (sum(d) + bits[9]) % 2 == 0 if parite == "paire" else True
    return octet, ok


def bourrage(bits):
    """Insère un bit contraire après cinq bits identiques, comme l'émetteur CAN."""
    sortie, n, prec = [], 0, None
    for b in bits:
        sortie.append(b)
        n = n + 1 if b == prec else 1
        prec = b
        if n == 5:
            sortie.append(1 - b)
            prec, n = 1 - b, 1
    return sortie


def arbitrage(ids, n=11):
    """Simule l'arbitrage CAN : renvoie le gagnant et le rang du bit décisif."""
    en_lice = list(ids)
    for k in range(n):
        bits = {i: (i >> (n - 1 - k)) & 1 for i in en_lice}
        bus = min(bits.values())  # ET câblé : 0 dominant
        restants = [i for i in en_lice if bits[i] == bus]
        if len(restants) < len(en_lice) and len(restants) == 1:
            return restants[0], k + 1
        en_lice = restants
    return en_lice[0], None


def crc16_modbus(octets):
    crc = 0xFFFF
    for o in octets:
        crc ^= o
        for _ in range(8):
            crc = (crc >> 1) ^ 0xA001 if crc & 1 else crc >> 1
    return crc


def db(x):
    return 10 ** (x / 10)


lora = lambda sf, bw, cr: sf * bw / 2 ** sf * cr

# ── §1 : débits ─────────────────────────────────────────────────────────
verifier("§1 / carte f-001 : T_b à 9 600 bit/s (µs)", 1e6 / 9600, "104")
verifier("§1 : T_b à 115 200 bit/s (µs)", 1e6 / 115200, "8.68")
verifier("§1 : rendement 8 bits sur 11 (%)", 800 / 11, "73")
vrai("§1 / carte f-002 : M = 4 → 2 bits par symbole", math.log2(4) == 2)

# ── §2 : liaison série ─────────────────────────────────────────────────
vrai("§2 / figure uart : 'A' = 0x41", ord("A") == 0x41)
vrai("§2 / figure uart : trame de 0x41, parité paire",
     trame_uart(0x41) == [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1])
vrai("§2 : '0' = 0x30", ord("0") == 0x30)
verifier("§2 : caractère de 11 bits à 9 600 bit/s (ms)", 11 / 9600 * 1e3, "1.15")

# ── §4 : Modbus et DMX ─────────────────────────────────────────────────
vrai("§4 : 0x01F4 = 500 et 0x0FA0 = 4 000", 0x01F4 == 500 and 0x0FA0 == 4000)
verifier("§4 : consigne 500 au facteur 10", 500 / 10, "50.0")
crc = crc16_modbus([0x01, 0x06, 0x0F, 0xA0, 0x01, 0xF4])
print(f"    (CRC de 01 06 0F A0 01 F4 : {crc & 0xFF:02X} {crc >> 8:02X}, poids faible en tête)")
verifier("§4 : bit DMX à 250 kbit/s (µs)", 1e6 / 250e3, "4")
t_dmx = 88 + 8 + 513 * 11 * 4
verifier("§4 : univers DMX complet (µs)", t_dmx, "22700", tol=0.003)
verifier("§4 : rafraîchissement DMX (Hz)", 1e6 / t_dmx, "44")

# ── §5 : bus CAN ───────────────────────────────────────────────────────
champs = {"SOF": 1, "ID": 11, "RTR": 1, "IDE r0": 2, "DLC": 4, "CRC": 16, "ACK": 2, "EOF": 7}
vrai("§5 / carte f-008 : champs fixes = 44 bits", sum(champs.values()) == 44)
verifier("§5 : trame de 8 octets (bits)", 44 + 64, "108")
verifier("§5 / carte f-009 : 108 bits à 500 kbit/s (µs)", 108 / 500e3 * 1e6, "216")
verifier("§5 : 64 bits utiles sur 111 (%)", 6400 / 111, "58", tol=0.01)
vrai("§5 : 64/111 < 58 %", 64 / 111 < 0.58)
id1 = int("0110010", 2) << 4 | 0b1010
id2 = int("0110100", 2) << 4 | 0b0001
g, k = arbitrage([id1, id2], 11)
vrai("§5 / figure arbitrage : le plus petit gagne au bit 5", g == min(id1, id2) == id1 and k == 5)
vrai("§5 / figure bourrage : 1 000000 11 → 1 00000 1 0 11",
     bourrage([1, 0, 0, 0, 0, 0, 0, 1, 1]) == [1, 0, 0, 0, 0, 0, 1, 0, 1, 1])

# ── §6 : IP ────────────────────────────────────────────────────────────
n = ipaddress.ip_interface("192.168.10.37/24").network
vrai("§6 / figure ip : réseau 192.168.10.0", str(n.network_address) == "192.168.10.0")
vrai("§6 : diffusion 192.168.10.255", str(n.broadcast_address) == "192.168.10.255")
verifier("§6 : hôtes d'un /24", n.num_addresses - 2, "254")
verifier("§6 / figure encapsulation : en-têtes UDP + IP + Ethernet + FCS (o)", 8 + 20 + 14 + 4, "46")

# ── §7 : parité ────────────────────────────────────────────────────────
vrai("§7 / figure parité : 0x41 a deux 1, parité 0", bin(0x41).count("1") == 2)
vrai("§7 : une erreur détectée, deux non",
     sum([0, 1, 0, 0, 0, 0, 1, 1, 0]) % 2 == 1 and sum([0, 1, 0, 0, 1, 0, 1, 1, 0]) % 2 == 0)

# ── §8 : modulations ───────────────────────────────────────────────────
verifier("§8 : 0 dBm (mW)", db(0), "1")
verifier("§8 : 10 dBm (mW)", db(10), "10")
verifier("§8 : 20 dBm (mW)", db(20), "100")
verifier("§8 : +3 dB, facteur", db(3), "2", tol=0.003)
# phase FM : dérivée de Φ / 2π = f0 + kf vm, vérifiée numériquement
f0, kf, Vm, fm = 1000.0, 50.0, 2.0, 10.0
phi = lambda t: 2 * math.pi * f0 * t + (kf * Vm / fm) * math.sin(2 * math.pi * fm * t)
t, h = 0.0123, 1e-7
finst = (phi(t + h) - phi(t - h)) / (2 * h) / (2 * math.pi)
vrai("§8 / carte f-004 : dΦ/dt / 2π = f0 + kf vm", abs(finst - (f0 + kf * Vm * math.cos(2 * math.pi * fm * t))) < 1e-4)

# ── §9 : Shannon ───────────────────────────────────────────────────────
verifier("§9 : 30 dB en rapport", db(30), "1000")
verifier("§9 : canal de 3 kHz à 30 dB (kbit/s)", 3000 * math.log2(1 + 1000) / 1e3, "30", tol=0.01)
verifier("§9 / figure shannon : C/B à 30 dB", math.log2(1001), "10", tol=0.005)

# ── §10 : LoRa ─────────────────────────────────────────────────────────
verifier("§10 : débit SF12, 125 kHz, CR 4/5 (bit/s)", lora(12, 125e3, 0.8), "293")

# ── §11 : servomoteur ──────────────────────────────────────────────────
verifier("§11 : 50 consignes par seconde", 1 / 0.020, "50")

# ── Exemple ────────────────────────────────────────────────────────────
Tb = 1 / 9600
Tc = 11 * Tb
verifier("ex. 1 : T_b (µs)", Tb * 1e6, "104.2")
verifier("ex. 1 : caractère (ms)", Tc * 1e3, "1.146")
verifier("ex. 1 : t3,5 (ms)", 3.5 * Tc * 1e3, "4.01")
bits = trame_uart(0x02)
vrai("ex. 2 : trame de 0x02 = 0 0 1 0 0 0 0 0 0 1 1", bits == [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1])
paliers = [(bits[0], 0)]
for b in bits:
    if b == paliers[-1][0]:
        paliers[-1] = (b, paliers[-1][1] + 1)
    else:
        paliers.append((b, 1))
durees = [round(n * Tb * 1e6) for b, n in paliers[:3]]
vrai("ex. 2 / figure octet : paliers 208, 104, 625 µs", durees == [208, 104, 625])
vrai("ex. 2 : décodage 0x02, parité correcte", lire_uart(bits) == (2, True))
vrai("ex. 2 : lu poids fort d'abord → 64", int("".join(map(str, bits[1:9])), 2) == 64)
t_ech = (8 + 9) * Tc + 2 * 3.5 * Tc + 5e-3
verifier("ex. 3 : durée d'un échange (ms)", t_ech * 1e3, "32.5")
verifier("ex. 3 / figure échange : fin de requête (ms)", 8 * Tc * 1e3, "9.2")
verifier("ex. 3 / figure échange : début de traitement (ms)", 11.5 * Tc * 1e3, "13.2")
verifier("ex. 3 / figure échange : début de réponse (ms)", (11.5 * Tc + 5e-3) * 1e3, "18.2")
verifier("ex. 3 / figure échange : fin de réponse (ms)", (20.5 * Tc + 5e-3) * 1e3, "28.5")
verifier("ex. 3 : cycle de 4 esclaves (ms)", 4 * t_ech * 1e3, "130")
verifier("ex. 3 : débit utile (bit/s)", 32 / t_ech, "985", tol=0.002)
verifier("ex. 3 : part du débit de ligne (%)", 32 / t_ech / 9600 * 100, "10")
Tc2 = 11 / 19200
verifier("ex. 3 : caractère à 19 200 bit/s (ms)", Tc2 * 1e3, "0.573")
verifier("ex. 3 : échange à 19 200 bit/s (ms)", (24 * Tc2 + 5e-3) * 1e3, "18.8")
verifier("ex. 3 : cycle à 19 200 bit/s (ms)", 4 * (24 * Tc2 + 5e-3) * 1e3, "75")
vrai("ex. 4 : réponse de 9 octets", len([0x02, 0x03, 0x04, 0x01, 0x2C, 0x00, 0x00, 0, 0]) == 5 + 2 * 2)
verifier("ex. 4 : 0x012C", 0x012C, "300")
verifier("ex. 4 : débit (m³/h)", 0x012C / 10, "30.0")
a = ipaddress.ip_interface("192.168.1.20/24")
vrai("ex. 5 : serveur dans le même réseau", ipaddress.ip_address("192.168.1.200") in a.network)
vrai("ex. 5 : portable 192.168.2.15 hors réseau", ipaddress.ip_address("192.168.2.15") not in a.network)
verifier("ex. 5 : trame UDP de 8 octets utiles (o)", 8 + 8 + 20 + 14 + 4, "54")
verifier("ex. 5 : trame minimale à 100 Mbit/s (µs)", 64 * 8 / 100e6 * 1e6, "5", tol=0.05)
verifier("ex. 6 : f(1) (MHz)", 868.3 + 0.0048, "868.3048")
verifier("ex. 6 : f(0) (MHz)", 868.3 - 0.0048, "868.2952")
verifier("ex. 6 : f_m = D_b/2 (kHz)", 4.8 / 2, "2.4")
verifier("ex. 6 : indice m", 4.8 / 2.4, "2")
verifier("ex. 6 : bande de Carson (kHz)", 2 * (4.8 + 2.4), "14.4")
verifier("ex. 6 : capacité à 10 dB (kbit/s)", 25e3 * math.log2(1 + db(10)) / 1e3, "86.5")
t_msg = 128 / 4800
verifier("ex. 6 : message de 16 octets (ms)", t_msg * 1e3, "26.7")
verifier("ex. 6 : intervalle à 1 % (s)", 100 * t_msg, "2.7")

# ── Méthode ────────────────────────────────────────────────────────────
verifier("2017-E1 Q29 : T_b à 9 600 bauds (µs)", 1e6 / 9600, "104.2")
verifier("2017-E1 Q29 : 1,144 ms / 11 bits (µs)", 1144 / 11, "104")
b = [0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1]
vrai("2017-E1 Q29 : D1 = 0x4B, parité paire correcte", lire_uart(b) == (0x4B, True))
vrai("2017-E1 Q29 : trame de 0x4B", trame_uart(0x4B) == b)
vrai("2017-E1 Q29 : B6…B1 = 100101, PLD 5 (100001 = PLD 1)", (0x4B >> 1) & 0x3F == 0b100101 == 0b100001 + 4)
vrai("2017-E1 Q29 : B7 = 0, B0 = 1", (0x4B >> 7) == 0 and (0x4B & 1) == 1)
vrai("2017-E1 Q29 : poids fort en tête → 0xD2", int("11010010", 2) == 0xD2)
vrai("2017-E1 Q29 : voie B complémentée → 0xB4", sum((1 - x) << k for k, x in enumerate(b[1:9])) == 0xB4)
vrai("2023-E2 E5 : 1 0 1 0 0 0 1 0 → 0x45 = 'E'", sum(x << k for k, x in enumerate([1, 0, 1, 0, 0, 0, 1, 0])) == 0x45 == ord("E"))
vrai("2023-E2 E6 : 'W' = 0x57, émis 1 1 1 0 1 0 1 0", ord("W") == 0x57 and trame_uart(0x57, parite=None)[1:9] == [1, 1, 1, 0, 1, 0, 1, 0])
nmea = "$GPGGA,091709.3,4619.088593,N,00029.479943,W,1,04,2.6,64.7,M,,,,0000*27"
ck = 0
for ch in nmea[1:nmea.index("*")]:
    ck ^= ord(ch)
vrai("2023-E2 E7 : somme NMEA = 0x27", ck == 0x27)
verifier("2023-E2 E7 : caractères", len(nmea), "71")
verifier("2023-E2 E7 : durée (ms)", len(nmea) * 10 / 115200 * 1e3, "6.16")
verifier("2023-E2 E7 : avec CR LF (ms)", (len(nmea) + 2) * 10 / 115200 * 1e3, "6.34")
verifier("2023-E2 E8 : 6 km/h (m/s)", 6 / 3.6, "1.667")
verifier("2023-E2 E8 : distance (mm)", 6 / 3.6 * len(nmea) * 10 / 115200 * 1e3, "10.3")
verifier("2023-E2 E8 : avec 8 bits par caractère (mm)", 6 / 3.6 * len(nmea) * 8 / 115200 * 1e3, "8.2")
vrai("2025-E1 Q20 : 24 bits = 3 caractères de 8 bits", 24 // 8 == 3)
verifier("2025-E1 Q20 : caractère de 12 bits", 1 + 8 + 1 + 2, "12")
vrai("2023-E1 Q22 : 1 passerelle + 51 variateurs > 32", 1 + 51 > 32)
vrai("2023-E1 Q24 : 0x0FA0 = 4 000, 0x01A2 = 418", 0x0FA0 == 4000 and 0x01A2 == 418)
verifier("2023-E1 Q24 : consigne (Hz)", 418 / 10, "41.8")
crc = crc16_modbus([0x00, 0x06, 0x0F, 0xA0, 0x01, 0xA2])
vrai("2023-E1 Q23 : CRC-16 Modbus émis 0B 04, non 22 C0", (crc & 0xFF, crc >> 8) == (0x0B, 0x04))
f_ete = lambda N: (N + 1.77e-5 * N ** 2 / 0.32) / 20
verifier("2023-E1 Q25 : f à 800 tr/min (Hz)", f_ete(800), "41.8")
verifier("2023-E1 Q25 : f à 450 tr/min (Hz)", f_ete(450), "23.1")
verifier("2023-E1 Q25 : Ns = 60 f / p, p = 3", 60 / 3, "20")
verifier("2025-E1 Q61 : lignes de 32 appareils pour 400", math.ceil(400 / 32), "13")
vrai("2025-E1 Q61 : 4 000 à 9 600 canaux", 400 * 10 == 4000 and 400 * 24 == 9600)
verifier("2025-E1 Q62 : 24 lyres × 24 canaux", 24 * 24, "576")
verifier("2025-E1 Q63 : 24 lyres × 20 canaux", 24 * 20, "480")
t63 = 88 + 8 + 44 + 480 * 44
verifier("2025-E1 Q63 : trame (µs)", t63, "21260")
verifier("2025-E1 Q63 : fréquence (Hz)", 1e6 / t63, "47.0")
verifier("2025-E1 Q64 : univers plein (ms)", (88 + 8 + 513 * 44) / 1e3, "22.7")
verifier("2025-E1 Q64 : univers plein (Hz)", 1e6 / (88 + 8 + 513 * 44), "44")
vrai("figure dmxtrame : 150 = 0x96, émis 0 1 1 0 1 0 0 1", [(150 >> k) & 1 for k in range(8)] == [0, 1, 1, 0, 1, 0, 0, 1])
verifier("2022-E1 Q16 : 2^48", 2 ** 48 / 1e14, "2.8")
verifier("2022-E1 Q16 : bits contrôlés par le CRC", 8 + 48, "56")
n = ipaddress.ip_interface("192.168.2.126/26").network
vrai("2025-E1 Q70 : réseau .64, diffusion .127",
     (str(n.network_address), str(n.broadcast_address)) == ("192.168.2.64", "192.168.2.127"))
hotes = list(n.hosts())
vrai("2025-E1 Q70 : hôtes .65 à .126, secours .125",
     str(hotes[0]) == "192.168.2.65" and str(hotes[-1]) == "192.168.2.126" and str(hotes[-2]) == "192.168.2.125")
verifier("2025-E1 Q71 : 1 Gbit/s / 250 kbit/s", 1e9 / 250e3, "4000")
v24 = 60 / 3.6
verifier("2024-E1 Q27 : erreur à la seconde (m)", v24 * 1, "16.7")
verifier("2024-E1 Q28 : résolution pour 1 cm (ms)", 0.01 / v24 * 1e3, "0.6")
verifier("2024-E1 Q30 : pseudo-en-tête (octets)", (32 + 32 + 8 + 8 + 16) / 8, "12")
nb = (12 + 8 + 20) * 8
verifier("2024-E1 Q30 : bits", nb, "320")
verifier("2024-E1 Q30 : durée à 300 Mbit/s (µs)", nb / 300e6 * 1e6, "1.067")
verifier("2024-E1 Q31 : Tret (µs)", 20 + nb / 300e6 * 1e6, "21.07")
verifier("2024-E1 Q32 : distance (mm)", v24 * (20e-6 + nb / 300e6) * 1e3, "0.35")
verifier("2024-E1 Q33 : rendement de la figure 7 (%)", 20 / 40 * 100, "50")
verifier("2015-E1 Q23 : 10 dBm (mW)", db(10), "10")
verifier("2015-E1 Q27 : pas de la PLL (kHz)", 20.48e3 / 1024, "20")
verifier("2015-E1 Q27 : N0", 432.7e6 / 20e3, "21635")
verifier("2015-E1 Q27 : N1", 433.3e6 / 20e3, "21665")
verifier("2022-E1 Q29 : débit LoRa (bit/s)", lora(12, 125e3, 0.8), "293")

verifier("2024-E1 Q28 : demi-millisecondes par jour (millions)", 86400 * 2000 / 1e6, "172.8")
vrai("2024-E1 Q28 : 28 bits suffisent, 27 non", 2 ** 27 < 86400 * 2000 <= 2 ** 28)
verifier("2024-E1 Q28 : erreur à 0,5 ms (cm)", v24 * 0.5e-3 * 100, "0.83")
verifier("2024-E1 Q30 : rendement sur la ligne (%)", 20 / (20 + 8 + 20 + 14 + 4) * 100, "30", tol=0.02)
verifier("2022-E1 Q29 : SF7 (bit/s)", lora(7, 125e3, 0.8), "5470", tol=0.001)
verifier("formule DMX : 88 + 8 + 44 (n + 1), n = 480 (µs)", 88 + 8 + 44 * (480 + 1), "21260")
verifier("formule hôtes : /26", 2 ** (32 - 26) - 2, "62")
verifier("ex. 3 : 130 / 75", 130 / 75, "1.7")

verifier("2024-E1 Q32 : avec l'attente d'une position, 1 ms (ms)", 1 + 20e-3 + nb / 300e6 * 1e3, "1.02")
verifier("2024-E1 Q32 : distance avec l'attente (cm)", v24 * (1e-3 + 20e-6 + nb / 300e6) * 100, "1.7")
verifier("2025-E1 Q63 : T_b DMX (µs)", 1e6 / 250e3, "4")
verifier("§3 : charges à 1/4 et 1/8", 32 * 4, "128")
verifier("§3 : charges à 1/8", 32 * 8, "256")

# ── Auto-test ──────────────────────────────────────────────────────────
verifier("Q1 : T_b à 115 200 bit/s (µs)", 1e6 / 115200, "8.68")
verifier("Q1 : octets par seconde, 10 bits", 115200 / 10, "11520")
verifier("Q1 : débit utile (bit/s)", 115200 / 10 * 8, "92160")
vrai("Q2 : 0x123 et 0x0F0 sur 11 bits",
     format(0x123, "011b") == "00100100011" and format(0x0F0, "011b") == "00011110000")
vrai("Q2 : 0x0F0 gagne au troisième bit", arbitrage([0x123, 0x0F0]) == (0x0F0, 3))
verifier("Q2 : trame de 4 octets à 500 kbit/s (µs)", (44 + 32) / 500e3 * 1e6, "152")
n = ipaddress.ip_interface("172.16.4.130/26").network
vrai("Q3 : masque, réseau, diffusion",
     (str(n.netmask), str(n.network_address), str(n.broadcast_address))
     == ("255.255.255.192", "172.16.4.128", "172.16.4.191"))
vrai("Q3 : 130 = 1000 0010", format(130, "08b") == "10000010")
verifier("Q3 : hôtes", n.num_addresses - 2, "62")
verifier("Q4 : débit SF7 (bit/s)", lora(7, 125e3, 0.8), "5470", tol=0.001)
verifier("Q4 : rapport SF7/SF12", lora(7, 125e3, 0.8) / lora(12, 125e3, 0.8), "19", tol=0.02)
verifier("Q4 : symboles SF12/SF7", 2 ** 12 / 2 ** 7, "32")
verifier("Q5 : excursion (kHz)", 5 * 2, "10")
verifier("Q5 : indice", 10 / 1, "10")
verifier("Q5 : Carson (kHz)", 2 * (10 + 1), "22")
recu = [1, 0, 0, 0, 0, 1, 1, 0]
vrai("Q6 : trois 1 et parité 0 → erreur détectée", sum(recu) == 3 and (sum(recu) + 0) % 2 == 1)

print("\nAucun écart." if not ECARTS else f"\n{len(ECARTS)} écart(s) : {ECARTS}")
sys.exit(1 if ECARTS else 0)
