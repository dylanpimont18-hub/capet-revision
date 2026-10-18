"""Applications numériques et comportements séquentiels du chapitre T29, refaits en Python.

    python3 cours/calculs/T29.py

Mémoires, bascules, compteurs, temporisations, diagrammes d'états et GRAFCET
sont simulés pas à pas ; chaque valeur publiée dans cours/textes/T29.html est
recalculée. Un écart fait échouer le script.
"""
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


# ── §1 : mémoires ────────────────────────────────────────────────────────
def memoire(entrees, prio):
    M, sortie = 0, []
    for m, a in entrees:
        M = (1 - a) & (m | M) if prio == "arret" else m | ((1 - a) & M)
        sortie.append(M)
    return sortie


fig = list(zip([0, 1, 0, 0, 0, 1, 1, 0], [0, 0, 0, 1, 0, 1, 0, 0]))
A, B = memoire(fig, "arret"), memoire(fig, "marche")
vrai("fig. 2 : arrêt prioritaire = 1 aux intervalles 2, 3, 7, 8", A == [0, 1, 1, 0, 0, 0, 1, 1])
vrai("fig. 2 : marche prioritaire = 1 aux intervalles 2, 3, 6 à 8", B == [0, 1, 1, 0, 0, 1, 1, 1])
vrai("fig. 2 : les deux ne diffèrent qu'à l'intervalle 6", [k + 1 for k in range(8) if A[k] != B[k]] == [6])
vrai("§1 : sans appui, M+ = M (deux mémoires)",
     all(memoire([(0, 0)], p) == [0] for p in ("arret", "marche")))
q1 = [(0, 0), (1, 0), (0, 0), (1, 1), (0, 0), (0, 1), (0, 0)]
vrai("Q1 : arrêt prioritaire 0, 1, 1, 0, 0, 0, 0", memoire(q1, "arret") == [0, 1, 1, 0, 0, 0, 0])
vrai("Q1 : marche prioritaire 0, 1, 1, 1, 1, 0, 0", memoire(q1, "marche") == [0, 1, 1, 1, 1, 0, 0])
# Auto-maintien (fig. 1) : S2 marche, S1 arrêt, KM = S1 barre · (S2 + KM)
vrai("fig. 1 : KM = 0, 1, 1, 1, 0, 0",
     memoire(list(zip([0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0])), "arret") == [0, 1, 1, 1, 0, 0])


# ── §2 : bascule RS à deux NON-OU ────────────────────────────────────────
def nor(x, y):
    return 1 - (x | y)


def rs(S, R, Q, Qb):
    for _ in range(6):          # relaxation jusqu'à stabilité
        Q, Qb = nor(R, Qb), nor(S, Q)
    return Q, Qb


vrai("§2 : S = 1, R = 0 → Q = 1, Q̄ = 0", rs(1, 0, 0, 1) == (1, 0))
vrai("§2 : S retombé, Q = 1 mémorisé", rs(0, 0, 1, 0) == (1, 0))
vrai("§2 : R = 1 → Q = 0, Q̄ = 1", rs(0, 1, 1, 0) == (0, 1))
vrai("§2 : S = R = 1 → Q = Q̄ = 0", rs(1, 1, 1, 0) == (0, 0) and rs(1, 1, 0, 1) == (0, 0))


# Données des figures 4 et 6, recopiées de leur script de tracé
def d_signal():
    """Horloge et donnée de la fig. 4, par pas : fronts montants de H aux pas 2, 6, 10…"""
    n = 48
    D = [0] * n
    for k in list(range(4, 13)) + [16] + list(range(24, 36)) + list(range(41, 48)):
        D[k] = 1
    Q, q = [], 0
    for k in range(n):
        if k % 4 == 2:
            q = D[k]
        Q.append(q)
    return D, Q


D, Q = d_signal()
vrai("fig. 4 : Q recopie D au front montant, D stable aux fronts",
     all(Q[k] == D[k] for k in range(2, 48, 4)) and all(D[k - 1] == D[k] for k in range(2, 48, 4)))
vrai("fig. 4 : l'impulsion brève de D, entre deux fronts, ne passe pas", D[16] == 1 and Q[16] == Q[15] == Q[17])


def registre(entree=(1, 0, 1, 1)):
    q, etats = [0, 0, 0, 0], []
    for e in entree:
        q = [e] + q[:3]
        etats.append(list(q))
    return etats


# ── §3 : compteurs ──────────────────────────────────────────────────────
for k, f in enumerate((500, 250, 125)):
    verifier(f"§3 : f(Q{k}) avec fH = 1 kHz", 1000 / 2 ** (k + 1), str(f))


def compteur_async(n_bits, fronts, modulo=None):
    """Compteur à bascules T déclenchées par le front descendant du bit précédent ; états transitoires notés."""
    q = [0] * n_bits
    etats, transitoires = [], []
    for _ in range(fronts):
        k = 0
        while True:
            q[k] ^= 1
            transitoires.append(sum(b << i for i, b in enumerate(q)))
            if q[k] == 1 or k == n_bits - 1:
                break
            k += 1
        v = sum(b << i for i, b in enumerate(q))
        if modulo and v == modulo:
            q = [0] * n_bits
            v = 0
        etats.append(v)
    return etats, transitoires


e3, _ = compteur_async(3, 16)
vrai("fig. 5 : le mot compte 1, 2, … 7, 0", e3[:8] == [1, 2, 3, 4, 5, 6, 7, 0])
_, tr = compteur_async(3, 4)
vrai("§3 : de 011 à 100, passages par 010 puis 000", tr[-3:] == [0b010, 0b000, 0b100])
vrai("§3 : décade, remise à zéro sur Q3 Q1 = 1 : 1010 est le premier état concerné",
     min(v for v in range(16) if (v >> 3) & 1 and (v >> 1) & 1) == 10)
vrai("§3 : 4 bascules pour 10 états, 6 pour 60", min(n for n in range(10) if 2 ** n >= 10) == 4
     and min(n for n in range(10) if 2 ** n >= 60) == 6)
e10, _ = compteur_async(4, 40, modulo=10)
q3 = [(v >> 3) & 1 for v in e10]
verifier("Q3 : f(Q3) d'un compteur 4 bits, 1 kHz", 1000 / 16, "62.5")
verifier("Q3 : décade, f(Q3)", 1000 / 10, "100")
verifier("Q3 : décade, rapport cyclique de Q3 (%)", 100 * sum(q3) / len(q3), "20")
vrai("fig. 6 : registre, 1 0 0 0 / 0 1 0 0 / 1 0 1 0 / 1 1 0 1",
     registre() == [[1, 0, 0, 0], [0, 1, 0, 0], [1, 0, 1, 0], [1, 1, 0, 1]])


# ── §4 : temporisations (simulation fine, pas de 10 ms) ──────────────────
def tempos(IN, PT, t_fin, dt=0.01):
    n = int(round(t_fin / dt))
    ton = tof = tp = None
    res = {"TON": [], "TOF": [], "TP": []}
    e, off, p_fin, prev = 0.0, n, -1.0, 0
    n_pt = int(round(PT / dt))
    for k in range(n + 1):
        t = k * dt
        x = 1 if any(a - 1e-9 <= t < b - 1e-9 for a, b in IN) else 0
        e = e + dt if x and prev else 0.0
        ton = 1 if x and e >= PT - 1e-9 else 0
        off = -1 if x else off + 1              # pas écoulés depuis la retombée de IN
        tof = 1 if x or off < n_pt else 0
        if x and not prev and t >= p_fin - 1e-9:
            p_fin = t + PT
        tp = 1 if t < p_fin - 1e-9 else 0
        for nom, v in (("TON", ton), ("TOF", tof), ("TP", tp)):
            res[nom].append((t, v))
        prev = x
    return res


def intervalles(serie):
    out, debut = [], None
    for t, v in serie:
        if v and debut is None:
            debut = t
        if not v and debut is not None:
            out.append((round(debut, 2), round(t, 2)))
            debut = None
    if debut is not None:
        out.append((round(debut, 2), None))
    return out


r = tempos([(1, 3), (5, 11)], 3, 15)
vrai("fig. 8 : TON à 1 de 8 à 11 s", intervalles(r["TON"]) == [(8.0, 11.0)])
vrai("fig. 8 : TOF à 1 de 1 à 14 s", intervalles(r["TOF"]) == [(1.0, 14.0)])
vrai("fig. 8 : TP, impulsions 1–4 s et 5–8 s", intervalles(r["TP"]) == [(1.0, 4.0), (5.0, 8.0)])
r = tempos([(0, 2), (4, 10)], 3, 16)
vrai("Q2 : TON à 1 de 7 à 10 s", intervalles(r["TON"]) == [(7.0, 10.0)])
vrai("Q2 : TOF à 1 de 0 à 13 s", intervalles(r["TOF"]) == [(0.0, 13.0)])
vrai("Q2 : TP, impulsions 0–3 s et 4–7 s", intervalles(r["TP"]) == [(0.0, 3.0), (4.0, 7.0)])


# ── §5 : minuterie (diagramme d'états) ───────────────────────────────────
def minuterie(appuis, t_fin, dt=0.01):
    etat, t_entree, journal = "eteinte", 0.0, []
    for k in range(int(round(t_fin / dt)) + 1):
        t = k * dt
        fm = any(abs(t - a) < dt / 2 for a in appuis)
        nouvel = etat
        if etat == "eteinte" and fm:
            nouvel = "allumee"
        elif etat == "allumee":
            if fm:
                nouvel = "allumee"
            elif t - t_entree >= 80 - 1e-9:
                nouvel = "preavis"
        elif etat == "preavis":
            if fm:
                nouvel = "allumee"
            elif t - t_entree >= 10 - 1e-9:
                nouvel = "eteinte"
        if nouvel != etat or (fm and nouvel == "allumee"):
            t_entree = t
            if nouvel != etat:
                journal.append((round(t, 2), nouvel))
        etat = nouvel
    return journal


j = minuterie([0, 85], 300)
vrai("Q5 : allumée 0, préavis 80, allumée 85, préavis 165, éteinte 175",
     j == [(0.0, "allumee"), (80.0, "preavis"), (85.0, "allumee"), (165.0, "preavis"), (175.0, "eteinte")])
verifier("Q5 : durée de clignotement (s)", (85 - 80) + (175 - 165), "15")


# ── §7 : GRAFCET, règles 2 à 5 avec recherche de stabilité ──────────────
def evoluer(actives, transitions, recep):
    """transitions : nom → (amont, aval) ; recep : nom → bool. Renvoie la situation stable et les étapes fugaces."""
    fugaces = set()
    while True:
        franch = [n for n, (am, av) in transitions.items() if set(am) <= actives and recep(n, actives)]
        if not franch:
            return actives, fugaces
        desact = set().union(*(set(transitions[n][0]) for n in franch))
        act = set().union(*(set(transitions[n][1]) for n in franch))
        nouv = (actives - desact) | act          # règle 5 : l'activation l'emporte
        fugaces |= actives - nouv
        actives = nouv


tr = {"t1": ([1], [2]), "t2": ([2], [3])}
# Un seul pas d'évolution : les réceptivités ne restent pas vraies.
franch = [n for n, (am, av) in tr.items() if set(am) <= {1, 2}]
pas = ({1, 2} - {1, 2}) | {2, 3}
vrai("fig. 12 : étapes 1 et 2 actives, deux transitions → étapes 2 et 3", pas == {2, 3} and len(franch) == 2)
# Faute à éviter : réseaux en place, R puis S transition par transition
X = {1: 1, 2: 1, 3: 0}
for am, av in ((1, 2), (2, 3)):
    if X[am]:
        X[av], X[am] = 1, 0
vrai("§9 : programmation naïve, réseau par réseau, perdrait l'étape 2", X == {1: 0, 2: 0, 3: 1})

par = {"t": ([1], [2, 4]), "r2": ([2], [3]), "r4": ([4], [5]), "r6": ([3, 5], [6])}
vraies = {"r4", "r6"}
stable, fug = evoluer({3, 4}, par, lambda n, s: n in vraies)
vrai("Q4 : situation stable, étape 6 seule ; étape 5 fugace", stable == {6} and 5 in fug)


def equation_etape(Xprec, rprec, Xi, ri):
    return (Xprec & rprec) | (Xi & (1 - (Xi & ri)))


vrai("§7 : X(i-1) r(i-1) + Xi·NON(Xi ri) = X(i-1) r(i-1) + Xi r̄i",
     all(equation_etape(a, b, c, d) == ((a & b) | (c & (1 - d)))
         for a in (0, 1) for b in (0, 1) for c in (0, 1) for d in (0, 1)))
vrai("§7 : activée et désactivée à la fois, l'étape reste active", equation_etape(1, 1, 1, 1) == 1)


# ── §8 : cycle d'automate ───────────────────────────────────────────────
def vu(t_debut, duree, Tc, phase):
    """Une impulsion [t_debut, t_debut + duree) est-elle lue par des lectures aux instants phase + k Tc ?"""
    k = 0
    while phase + k * Tc < t_debut + duree:
        t = phase + k * Tc
        if t >= t_debut:
            return True
        k += 1
    return False


Tc = 0.010
vrai("§8 : une impulsion de 0,9 Tc peut échapper à la lecture", not vu(0.0101, 0.9 * Tc, Tc, 0.0))
vrai("§8 : une impulsion de 1,1 Tc est toujours vue",
     all(vu(0.0, 1.1 * Tc, Tc, ph / 100 * Tc) for ph in range(100)))

# ── Méthode : 2021-E1, 2019-E1 ───────────────────────────────────────────
t_ar = 2.5 / 0.1 + 10 + (6.5 - 2.5) / 0.1 + 6.5 / 0.2
verifier("2021-E1 Q29 : durée de l'aller-retour (s)", t_ar, "107.5")
verifier("2021-E1 Q29 : en minutes", t_ar / 60, "1.8")
verifier("2021-E1 Q30 : passage d'un bras long (min)", 1 / (2 * 0.064), "7.8")
verifier("2021-E1 Q30 : avec 10 s d'attente au départ (min)", (t_ar + 10) / 60, "2")
vrai("fig. 19 : profil 0 → 25 s, 2,5 m → 35 s → 75 s, 6,5 m → 107,5 s",
     [2.5 / 0.1, 2.5 / 0.1 + 10, 2.5 / 0.1 + 10 + 4 / 0.1, t_ar] == [25.0, 35.0, 75.0, 107.5])
verifier("2019-E1 Q3 : seuil bas (lux)", 2000 * (1 - 0.05), "1900")
verifier("2019-E1 Q3 : seuil haut (lux)", 2000 * (1 + 0.05), "2100")

# ── Exemple : poste de remplissage ──────────────────────────────────────
v, pas_b, D_b, Vb, Qv, Tc = 0.25, 0.50, 0.16, 5, 0.625, 0.020
t_rempl = Vb / Qv
t_amen = pas_b / v
verifier("ex. 2 : remplissage (s)", t_rempl, "8")
verifier("ex. 2 : amenée d'un bidon (s)", t_amen, "2")
t_carton = 6 * (t_amen + t_rempl) + 5
verifier("ex. 2 : carton (s)", t_carton, "65")
verifier("ex. 2 : cadence (bidons/h)", 6 * 3600 / t_carton, "332")
cartons = int(8 * 3600 // t_carton)
verifier("ex. 2 : cartons par jour", cartons, "443")
verifier("ex. 2 : bidons par jour", 6 * cartons, "2658")
verifier("ex. 2 : volume par jour (L)", 6 * cartons * Vb, "13290")
verifier("ex. 3 : le bidon plein quitte la cellule (s)", D_b / v, "0.64")
verifier("ex. 3 : p à 0 pendant (s)", (pas_b - D_b) / v, "1.36")
verifier("ex. 3 : en cycles de 20 ms", (pas_b - D_b) / v / Tc, "68")
verifier("ex. 4 : course pendant deux cycles (m)", v * 2 * Tc, "0.010")
vrai("ex. 5 : N de 0 à 6 sur 3 bits", 6 < 2 ** 3)
vrai("ex. 5 : 2 658 bidons sur 12 bits", 2 ** 11 < 2658 <= 2 ** 12)
verifier("ex. 6 : exécutions du programme par seconde", 1 / Tc, "50")


def poste(p_niveau, cycles=6):
    """GRAFCET du poste, réceptivité ↑p ou p ; renvoie le nombre de remplissages par bidon présent."""
    # Bidon plein encore sous la buse à la fin du remplissage : p = 1.
    remplissages_meme_bidon = 0
    p, p_prec = 1, 1
    etape = 1                                  # retour à l'étape 1 après comptage
    for _ in range(cycles):
        cond = p if p_niveau else (p and not p_prec)
        if etape == 1 and cond:
            remplissages_meme_bidon += 1       # l'étape 2 rouvre la vanne sans que le bidon ait bougé
            break
        p_prec = p
    return remplissages_meme_bidon


vrai("ex. 3 : avec la réceptivité p, la vanne se rouvre sur le bidon plein", poste(True) == 1)
vrai("ex. 3 : avec ↑p, rien tant que le bidon n'a pas bougé", poste(False) == 0)

# ── Q6 : codeur sur une entrée ordinaire ────────────────────────────────
fmax = 1 / (2 * 0.010)
verifier("Q6 : fréquence maximale lisible (Hz)", fmax, "50")
verifier("Q6 : vitesse maximale (tr/min)", fmax / 100 * 60, "30")
verifier("Q6 : fréquence à 1 500 tr/min (Hz)", 100 * 1500 / 60, "2500")
verifier("Q6 : rapport à la limite", 2500 / fmax, "50")

# ── Ajouts du tour 1 ────────────────────────────────────────────────────
vrai("§2 : bascule T, Q+ = T ⊕ Q (garde si T = 0, bascule si T = 1)",
     all((T ^ Q) == (Q if T == 0 else 1 - Q) for T in (0, 1) for Q in (0, 1)))
jk = {(0, 0): "mémoire", (1, 0): "mise à 1", (0, 1): "mise à 0", (1, 1): "basculement"}
ok = True
for (J, K), effet in jk.items():
    for Q in (0, 1):
        Qp = (J & (1 - Q)) | ((1 - K) & Q)
        attendu = {"mémoire": Q, "mise à 1": 1, "mise à 0": 0, "basculement": 1 - Q}[effet]
        ok &= Qp == attendu
vrai("§2 : bascule JK, Q+ = J Q̄ + K̄ Q", ok)
# Fig. 17 : franchissements calculés d'abord, puis toutes les mises à 0, puis toutes les mises à 1
X = {0: 1, 1: 1, 2: 0, 3: 0}
trans = [(0, 1), (1, 2), (2, 3), (3, 0)]
F = [X[am] == 1 for am, av in trans[:2]] + [False, False]     # F1 et F2 vraies
for (am, av), f in zip(trans, F):
    if f:
        X[am] = 0
for (am, av), f in zip(trans, F):
    if f:
        X[av] = 1
vrai("fig. 17 : X0 et X1 actives, F1 et F2 vraies → X1 et X2 actives", X == {0: 0, 1: 1, 2: 1, 3: 0})
verifier("2021-E1 Q30 : durée d'un tour du bras (min)", 1 / 0.064, "15.6")
vrai("ex. 5 : 2 659 états, de 0 à 2 658, sur 12 bits", 2 ** 11 < 2659 <= 2 ** 12)

# ── Ajouts du tour 2 ────────────────────────────────────────────────────
PT_alarme = 3.0
vrai("ex. 5 : amenée normale (2 s) < PT = 3 s < amenée sans bidon (4 s)",
     0.50 / 0.25 < PT_alarme < 2 * 0.50 / 0.25)

print("\nAucun écart." if not ECARTS else f"\n{len(ECARTS)} écart(s) : {ECARTS}")
sys.exit(1 if ECARTS else 0)
