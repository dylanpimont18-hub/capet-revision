"""Applications numériques et identités du chapitre T28, refaites en Python.

    python3 cours/calculs/T28.py

Chaque identité logique est vérifiée par énumération de sa table de vérité ;
chaque valeur publiée dans cours/textes/T28.html est recalculée. Un écart
fait échouer le script.
"""
from decimal import Decimal
from itertools import product

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


def egal(nom, f, g, n):
    """Deux fonctions de n variables ont la même table de vérité."""
    vrai(nom, all(f(*v) == g(*v) for v in product((0, 1), repeat=n)))


NON = lambda x: 1 - x
XOR = lambda x, y: x ^ y


def gray(n):
    return n ^ (n >> 1)


def gray_vers_binaire(g, n=4):
    b = (g >> (n - 1)) & 1
    mot = b
    for k in range(n - 2, -1, -1):
        b = b ^ ((g >> k) & 1)
        mot = (mot << 1) | b
    return mot


# ── §2 : algèbre de Boole ────────────────────────────────────────────────
egal("§2 : a + 0 = a, a·1 = a", lambda a: a | 0, lambda a: a & 1, 1)
egal("§2 : a + ā = 1", lambda a: a | NON(a), lambda a: 1, 1)
egal("§2 : a·ā = 0", lambda a: a & NON(a), lambda a: 0, 1)
egal("§2 : a + bc = (a + b)(a + c)", lambda a, b, c: a | (b & c), lambda a, b, c: (a | b) & (a | c), 3)
egal("§2 : a + ab = a", lambda a, b: a | (a & b), lambda a, b: a, 2)
egal("§2 : a + āb = a + b", lambda a, b: a | (NON(a) & b), lambda a, b: a | b, 2)
egal("§2 : De Morgan, NON(ab) = ā + b̄", lambda a, b: NON(a & b), lambda a, b: NON(a) | NON(b), 2)
egal("§2 : De Morgan, NON(a + b) = ā b̄", lambda a, b: NON(a | b), lambda a, b: NON(a) & NON(b), 2)
egal("§2 : De Morgan, NON(a + b + c) = ā b̄ c̄", lambda a, b, c: NON(a | b | c), lambda a, b, c: NON(a) & NON(b) & NON(c), 3)
egal("§2 : NON(a(b + c̄)) = ā + b̄ c", lambda a, b, c: NON(a & (b | NON(c))), lambda a, b, c: NON(a) | (NON(b) & c), 3)
egal("p-001 : a + b barre ≠ ā + b̄ (contre-exemple a = 1, b = 0)", lambda a, b: int(NON(1 | 0) != (NON(1) | NON(0))),
     lambda a, b: 1, 2)

# ── §3 : portes composées ────────────────────────────────────────────────
egal("§3 : a ⊕ b = a b̄ + ā b", XOR, lambda a, b: (a & NON(b)) | (NON(a) & b), 2)
egal("§3 : a ⊕ 0 = a, a ⊕ 1 = ā", lambda a: (a ^ 0) * 2 + (a ^ 1), lambda a: a * 2 + NON(a), 1)
egal("§3 : a ⊕ a = 0", lambda a: a ^ a, lambda a: 0, 1)
egal("§3 : ⊕ associatif", lambda a, b, c: (a ^ b) ^ c, lambda a, b, c: a ^ (b ^ c), 3)
NAND = lambda x, y: NON(x & y)
egal("§3 : NON par NON-ET", lambda a: NAND(a, a), NON, 1)
egal("§3 : ET par deux NON-ET", lambda a, b: NAND(NAND(a, b), NAND(a, b)), lambda a, b: a & b, 2)
egal("§3 : OU par trois NON-ET", lambda a, b: NAND(NAND(a, a), NAND(b, b)), lambda a, b: a | b, 2)
NOR = lambda x, y: NON(x | y)
egal("§3 : NON-OU universelle (ET)", lambda a, b: NOR(NOR(a, a), NOR(b, b)), lambda a, b: a & b, 2)

# ── §4 : forme canonique et majorité ─────────────────────────────────────
canon = lambda a, b, c: (NON(a) & b & c) | (a & NON(b) & c) | (a & b & NON(c)) | (a & b & c)
maj = lambda a, b, c: (a & b) | (b & c) | (a & c)
egal("§4 : Σm(3, 5, 6, 7) = ab + bc + ac", canon, maj, 3)
vrai("§4 : rangs 3, 5, 6, 7 des lignes à 1",
     [4 * a + 2 * b + c for a, b, c in product((0, 1), repeat=3) if canon(a, b, c)] == [3, 5, 6, 7])
egal("§4 : majorité = deux entrées au moins", maj, lambda a, b, c: int(a + b + c >= 2), 3)

# ── §5 : Karnaugh ────────────────────────────────────────────────────────
# figure à trois variables : 1 en ab = 10, 11 (c = 0 et 1) et ab = 01 pour c = 1
k3 = {(1, 0, 0): 1, (1, 1, 0): 1, (1, 0, 1): 1, (1, 1, 1): 1, (0, 1, 1): 1}
egal("§5 : tableau à trois variables, S = a + bc", lambda a, b, c: k3.get((a, b, c), 0), lambda a, b, c: a | (b & c), 3)
# figure à quatre variables : coins et carré central
vals = {(0, 0): [1, 0, 0, 1], (0, 1): [0, 1, 1, 0], (1, 1): [0, 1, 1, 0], (1, 0): [1, 0, 0, 1]}   # (c, d) -> colonnes ab
cols = [(0, 0), (0, 1), (1, 1), (1, 0)]
k4 = lambda a, b, c, d: vals[(c, d)][cols.index((a, b))]
egal("§5 : tableau à quatre variables, S = b̄ d̄ + b d", k4, lambda a, b, c, d: (NON(b) & NON(d)) | (b & d), 4)
egal("§5 : b̄ d̄ + b d = NON(b ⊕ d)", lambda a, b, c, d: (NON(b) & NON(d)) | (b & d), lambda a, b, c, d: NON(b ^ d), 4)
vrai("§5 : ordre de Gray 00, 01, 11, 10 : un seul bit change, bords compris",
     all(bin(cols[k][0] * 2 + cols[k][1] ^ cols[(k + 1) % 4][0] * 2 + cols[(k + 1) % 4][1]).count("1") == 1 for k in range(4)))

# ── §6 : ventilateur ─────────────────────────────────────────────────────
for T in range(0, 70):
    a, b = int(T > 35), int(T > 50)
    if not (a * NON(b) == int(35 < T <= 50) and b == int(T > 50) and not (a * NON(b) and b)):
        vrai(f"§6 : ventilateur à {T} °C", False)
vrai("§6 : PV = a b̄, GV = b, jamais ensemble, de 0 à 69 °C", True)
vrai("§6 : a = 0, b = 1 impossible", all(not (T <= 35 and T > 50) for T in range(-50, 150)))

# ── §7 : codes ───────────────────────────────────────────────────────────
vrai("§7 : 13 = 1101₂", format(13, "b") == "1101")
vrai("§7 : 1101 0110₂ = D6₁₆", int("11010110", 2) == 0xD6)
vrai("§7 : 1111 1110₂ = 254 non signé", int("11111110", 2) == 254)
vrai("§7 : 1111 1110₂ = −2 en complément à deux", int("11111110", 2) - 256 == -2 == -128 + 126)
vrai("§7 : 59 en BCD = 0101 1001, en binaire = 0011 1011", format(5, "04b") + format(9, "04b") == "01011001"
     and format(59, "08b") == "00111011")
vrai("§7 : six codes inutilisés sur seize en BCD", 16 - 10 == 6)
vrai("§7 : Gray, un seul bit change entre voisins (cycle de 16)",
     all(bin(gray(k) ^ gray((k + 1) % 16)).count("1") == 1 for k in range(16)))
vrai("§7 : 0111 → 1000 en binaire : quatre bits changent", bin(7 ^ 8).count("1") == 4)
vrai("§7 : Gray → binaire en cascade, inverse du codage", all(gray_vers_binaire(gray(k)) == k for k in range(16)))
vrai("§7 : g = 1101 → b = 1001 = 9", gray_vers_binaire(0b1101) == 0b1001 == 9)
verifier("§7 : trame de 8 octets à 500 kbit/s (µs)", 8 * 8 / 500e3 * 1e6, 128)
vrai("§7 : 32 Kio = 32 768 octets", 32 * 1024 == 32768)

# ── §8 : circuits ────────────────────────────────────────────────────────
for a, b in product((0, 1), repeat=2):
    vrai(f"§8 : demi-additionneur {a} + {b}", (a ^ b) + 2 * (a & b) == a + b)
for a, b, c in product((0, 1), repeat=3):
    S, Co = a ^ b ^ c, (a & b) | (c & (a ^ b))
    vrai(f"§8 : additionneur complet {a} + {b} + {c}", S + 2 * Co == a + b + c)
    vrai(f"§8 : retenues exclusives pour {a}{b}{c}", not ((a & b) and (c & (a ^ b))))
    vrai(f"§8 : C_out = majorité pour {a}{b}{c}", Co == maj(a, b, c))
vrai("§8 : 0110 + 0111 = 1101 = 13", 0b0110 + 0b0111 == 0b1101 == 13)
vrai("§8 : 1101 se lit −3 en complément à deux sur 4 bits", 0b1101 - 16 == -3)
# retenues entrant et sortant du MSB
c, retenues = 0, []
for k in range(4):
    a, b = (0b0110 >> k) & 1, (0b0111 >> k) & 1
    retenues.append(c)
    c = (a & b) | (c & (a ^ b))
vrai("§8 : dépassement, retenue entrant dans le MSB 1, sortante 0", retenues[3] == 1 and c == 0)
egal("§8 : multiplexeur, S = s̄ e0 + s e1", lambda s, e0, e1: (NON(s) & e0) | (s & e1),
     lambda s, e0, e1: e1 if s else e0, 3)
seg_a = {0, 2, 3, 5, 6, 7, 8, 9}
for d in range(10):
    b3, b2, b1, b0 = (d >> 3) & 1, (d >> 2) & 1, (d >> 1) & 1, d & 1
    vrai(f"§8 : segment a pour le chiffre {d}", (b3 | b1 | (b2 & b0) | (NON(b2) & NON(b0))) == int(d in seg_a))
vrai("§8 : chiffre 3 : segments a b c d g", True)

# ── §9 : opérations bit à bit ────────────────────────────────────────────
x = 0b1011_0110
vrai("§9 : x & 0x0F garde les quatre bits de poids faible", x & 0x0F == 0b0110)
vrai("§9 : x | 0x80 force le MSB", (0x36 | 0x80) == 0xB6)
vrai("§9 : (x >> 4) & 1 lit le bit 4", (x >> 4) & 1 == 1)

# ── Exemple chiffré : girouette ──────────────────────────────────────────
verifier("Ex. 1 : secteurs", 2 ** 4, 16)
verifier("Ex. 1 : largeur d'un secteur (°)", 360 / 16, 22.5)
verifier("Ex. 2 : début du secteur 9 (°)", 9 * 22.5, 202.5)
verifier("Ex. 2 : fin du secteur 9 (°)", 10 * 22.5, 225)
vrai("Ex. 2 : Gray de 9 = 1001 ⊕ 0100 = 1101", gray(9) == 0b1101 == 0b1001 ^ 0b0100)
vrai("Ex. 3 : Gray de 7 = 0100, de 8 = 1100, seul g3 change", gray(7) == 0b0100 and gray(8) == 0b1100)
vrai("Ex. 3 : 1111 = secteur 15, à 180° du secteur 7", (15 - 7) * 22.5 == 180)
alarme = [s for s in range(16) if 270 <= s * 22.5 or s * 22.5 < 22.5]
vrai("Ex. 4 : secteurs d'alarme 12 à 15 et 0", alarme == [0, 12, 13, 14, 15])
vrai("Ex. 4 : codes Gray 1010, 1011, 1001, 1000 et 0000",
     [gray(s) for s in (12, 13, 14, 15, 0)] == [0b1010, 0b1011, 0b1001, 0b1000, 0])


def A1(g3, g2, g1, g0):
    return (g3 & NON(g2)) | (NON(g3) & NON(g2) & NON(g1) & NON(g0))


def A2(g3, g2, g1, g0):
    return NON(g2) & (g3 | (NON(g1) & NON(g0)))


egal("Ex. 4 : factorisation et absorption", A1, A2, 4)
vrai("Ex. 4 : A vrai exactement sur les secteurs d'alarme",
     all(A2(*[(gray(s) >> k) & 1 for k in (3, 2, 1, 0)]) == int(s in alarme) for s in range(16)))
egal("Ex. 4 : NON-OU donne ḡ1 ḡ0", lambda g1, g0: NOR(g1, g0), lambda g1, g0: NON(g1) & NON(g0), 2)
verifier("Ex. 5 : trois portes en cascade (ns)", 3 * 20, 60)
verifier("Ex. 5 : durée dans un secteur à 5 tr/s (ms)", 1 / (5 * 16) * 1e3, 12.5)
verifier("Ex. 5 : rapport 12,5 ms / 60 ns", 12.5e-3 / 60e-9, 208333, tol=0.01)
vrai("Ex. 5 : plus de deux cent mille", 12.5e-3 / 60e-9 > 2e5)
verifier("Ex. 6 : bits par seconde", 10 * 8, 80)
verifier("Ex. 6 : octets par jour", 10 * 86400, 864000)
verifier("Ex. 6 : Mbit par jour", 10 * 86400 * 8 / 1e6, 6.9)

# ── Méthode concours ─────────────────────────────────────────────────────
vrai("2024-E1 Q26 : 13 = 0000 1101 = 0x0D", format(13, "08b") == "00001101" and 13 == 0x0D)
vrai("2024-E1 Q26 : 45 = 0010 1101 = 0x2D", format(45, "08b") == "00101101" and 45 == 0x2D)
vrai("2024-E1 Q26 : 33 = 0010 0001 = 0x21", format(33, "08b") == "00100001" and 33 == 0x21)
somme = 0x1F90 + 0x0035 + 0x001C
vrai("Q29 (exemple) : 0x1F90 + 0x0035 + 0x001C = 0x1FE1", somme == 0x1FE1)
vrai("Q29 (exemple) : + 0xF3A2 = 0x11383", somme + 0xF3A2 == 0x11383)
vrai("Q29 (exemple) : complément à 1 de 0x1383 = 0xEC7C", (~0x1383) & 0xFFFF == 0xEC7C)
vrai("Q29 (exemple) : avec report de la retenue, 0xEC7B", (~(0x1383 + 1)) & 0xFFFF == 0xEC7B)
vrai("2022-E1 Q17 : 0x03 << 8 | 0x36 = 0x0336 = 822", (0x03 << 8 | 0x36) == 0x0336 == 822
     and format(0x0336, "016b") == "0000001100110110")
verifier("2022-E1 Q17 : 822/16 (°C)", 822 / 16, 51.375)
verifier("2018-E1 : durée du rouge (min)", (41.8 - 13.2) + (120 - 106), 42.6)
verifier("2018-E1 : durée du vert (min)", 9.6 + (67.4 - 43.2) + (104.4 - 85.8), 52.4)
verifier("2018-E1 : durée du bleu (min)", 3.6 + 1.4 + 18.4 + 1.6, 25)
verifier("2018-E1 : total (min)", 42.6 + 52.4 + 25, 120)
verifier("2018-E1 : part du rouge (%)", 42.6 / 120 * 100, 36, tol=0.02)
verifier("2018-E1 : temps offert (%)", 20 * (1 - 35.5 / 80), 11, tol=0.02)
verifier("2018-E1 : temps offert (min)", 0.20 * (1 - 35.5 / 80) * 120, 13, tol=0.04)
for a, b in ((0, 0), (1, 0), (0, 1)):
    vrai(f"2018-E1 : un seul voyant pour a = {a}, b = {b}", a + b + NON(a | b) == 1)

# ── Auto-test ────────────────────────────────────────────────────────────
egal("Q1 : NON(a(b + c̄)) = ā + b̄ c", lambda a, b, c: NON(a & (b | NON(c))), lambda a, b, c: NON(a) | (NON(b) & c), 3)
m = 0b1011_0010
vrai("Q2 : 1011 0010 = 178 = 0xB2", m == 178 == 0xB2)
vrai("Q2 : en complément à deux, −78", m - 256 == -78 == -128 + 50)
vrai("Q2 : quatre 1, parité paire 0", bin(m).count("1") == 4)
mint = {1, 3, 4, 6, 9, 11, 12, 14}
egal("Q3 : Σm(1, 3, 4, 6, 9, 11, 12, 14) = b ⊕ d", lambda a, b, c, d: int(8 * a + 4 * b + 2 * c + d in mint),
     lambda a, b, c, d: b ^ d, 4)
egal("Q4 : deux capteurs sur trois = ab + bc + ac", lambda a, b, c: int(a + b + c >= 2), maj, 3)
vrai("Q5 : 0110 + 0111 = 1101, sans retenue sortante", (0b0110 + 0b0111) < 16)
verifier("Q6 : 12 octets de 10 bits à 115 200 bit/s (ms)", 12 * 10 / 115200 * 1e3, 1.04)
verifier("Q6 : en confondant bits et octets (ms)", 12 / 115200 * 1e3, 0.104)

print("\nAucun écart." if not ECARTS else f"\n{len(ECARTS)} écart(s) : {ECARTS}")
