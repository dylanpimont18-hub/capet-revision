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
