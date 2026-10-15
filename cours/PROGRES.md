# Cours CAPET SII·IE — suivi de rédaction

Un chapitre par thème, rédigé puis passé à la boucle qualité. Une itération
traite **un seul** chapitre : le premier au statut « à faire » du tableau
ci-dessous, dans l'ordre du tableau. Statuts possibles : « à faire »,
« en cours », « validé », « à reprendre ».

Périmètre : génie électrique (T01–T04, T06–T09, T11–T15, T17–T20, T22, T23,
T30) et génie informatique et automatique (T21, T24–T29), soit 27 chapitres.
Hors périmètre : T05 (thermique), T10 (mécanique), T16 (renouvelables).

## Plan

L'ordre va du fondamental vers l'appliqué ; chaque chapitre ne suppose que
les chapitres placés avant lui (colonne « prérequis »). C'est aussi l'ordre de
lecture proposé dans l'app (chapitre précédent / suivant).

Colonne « notes » : fréquence tirée de `cards.json` (« N/13 » = tombe dans N
sujets sur 13, à citer telle quelle dans « En bref ») · relevé des 22 épreuves
de l'app (nombre d'épreuves et de questions qui mobilisent le thème, en
principal ou en secondaire, voir `cours/releve-sujets.json`) · cartes du thème
(F formules, P pièges, S schémas), toutes à couvrir · extraits rédigés de
`exercices.json` sur ce thème (ce ne sont **pas** des sujets officiels : ils
peuvent inspirer l'exemple chiffré, jamais être cités comme épreuve).

| chapitre | thème | prérequis | statut | tours | notes | défauts restants |
|---|---|---|---|---|---|---|
| 1. Électrocinétique et grandeurs fondamentales | T01 | — | à reprendre | 5 | 13/13 · relevé : 17 ép., 78 q. · 20 F, 6 P, 2 S · 23 schémas · cartes corrigées (corrections/cartes.json) : T01-p-004 (loi des nœuds aux entrées de l'ALI, pas à la sortie), T01-p-002 (S² = P² + Q²), T01-f-009 (φ = retard de i sur u), SVG de T01-s-001 et T01-s-002 redessinés (svg/T01-s-00N.svg) · notes des tours 1 à 5 en exactitude : 2, 4, 4, 4, 4 ; tour 5 : couverture, progression et lisibilité 5/5, schémas et langue 4/5 | Les défauts du tour 5 (1 majeur : sinus redressé sans « double alternance » dans la règle de p-003 ; 10 mineurs : sources commandées, hacheur série, glissement en moteur, R_ch, courants continus en majuscules, schémas de Millman et de J) sont corrigés mais n'ont pas été relus : faire un tour de relecture de confirmation en passe finale (exactitude à confirmer à 5/5). |
| 2. Représentation complexe et impédances | T03 | T01 | à reprendre | 5 | 12/13 · relevé : 3 ép., 4 q. · 19 F, 6 P, 1 S · 15 schémas · cartes corrigées (corrections/cartes.json) : T03-p-003 (hypothèses du critère), T03-p-004 (1/ω0² sur le coefficient de (jω)²), T03-p-005 (démarrage limité par L_f ω_s), T03-p-006 (titre, piège), T03-f-004 (dipôle passif), T03-f-006 (latex), T03-f-008/009 (questions), T03-f-017 (hypothèses), T03-f-018 (label), T03-f-019 (label, latex, conditions), SVG de T03-s-001 redessiné (svg/T03-s-001.svg) · notes des tours 1 à 5 en exactitude : 3, 4, 4, 4, 4 ; tour 5 : couverture, schémas, progression et lisibilité 5/5, langue 4/5, 0 bloquant, 0 majeur | Les 12 défauts mineurs du tour 5 (signe de φ1, admittance jnCω, marge « écart algébrique », convention sin/cos de la figure 1, convention de S = V I*, R'_r/g grand devant L_f ω_s au nominal, indice p (C_p, R_par, L_par), appels des figures 2 et 5, liens des chapitres 5 et 16, tournure du voltmètre, latex de la carte T03-f-006, « intégrateurs admis ») sont corrigés mais n'ont pas été relus : faire un tour de relecture de confirmation en passe finale (exactitude à confirmer à 5/5). |
| 3. Puissances en régime sinusoïdal, monophasé et triphasé | T02 | T01, T03 | à reprendre | 5 | 13/13 · relevé : 8 ép., 26 q. · 35 F, 8 P, 1 S · extraits : X-2017-01, X-2017-02 · 11 schémas, générés par un script Python (scratchpad) · cartes corrigées : T02-f-027, f-029 (validité de l'approximation de Kapp), f-033 (par phase), p-005, SVG de T02-s-001 redessiné · cartes T02-f-021 et p-004 (même φ, et non même cos φ) · tour 1 : exactitude 3/5, couverture 3/5, lisibilité 3/5 (fiches « Formules clés » coupées à droite : grille corrigée, harnais renforcé), corrigé ; tour 2 : exactitude 3/5 (3 bloquants : règle de p-004, question de la carte T02-f-024, limite de l'approximation de Kapp pour une charge inductive), corrigé avec les cartes T02-f-001, f-013, f-014, f-015, f-024, f-025, f-029, p-001, p-003 ; tour 3 : exactitude 4/5, 0 bloquant, 0 majeur, 11 mineurs, tous corrigés (approximation de Kapp sous-estimée de 17 % même en charge inductive, somme des S du spa justifiée par Boucherot, homonymies Q_1, S_1 et I_n levées, U = V en monophasé dit une fois, unités des cartes f-016, f-027, f-030, f-033) ; tour 4 : exactitude 4/5, 0 bloquant, 0 majeur, 17 mineurs, tous corrigés (terme du second ordre écrit exactement, b²/[2(V_r + a)] = 11 V et non 14 V ; indice de phase q ; deux lectures des 750 W de 2020-E2 ; cartes f-018, f-035, p-004, p-007 ; liens id-carte en ligne dans le texte) ; tour 5 : exactitude 4/5, progression, lisibilité et langue 4/5, couverture et schémas 5/5, 0 bloquant, 0 majeur, 9 mineurs | Les 9 défauts mineurs du tour 5 (cause de l'écart LUBIO de 2018-E2 : cos φ1 affiché 0,75 contre P/(V I1) ≈ 0,74, et non l'arrondi ; domaine « régime sinusoïdal » et « valeur moyenne nulle » sur les fiches f-002, f-006, f-009, f-011, f-018, f-035 et la carte f-018 ; chiffres de la ligne de 2024-E2 annoncés au §6 ; « jamais S » nuancé dans la méthode bilan ; Q29 de 2015-E1 (GPL, 40,0 kg éq. CO₂) et S_n « kVA maxi » ; indice 1L signalé ; formules du §3 et de l'auto-test 5 en bloc ; « appelés » ; « en triphasé ») sont corrigés mais n'ont pas été relus : faire un tour de relecture de confirmation en passe finale (exactitude à confirmer à 5/5). |
| 4. Harmoniques, THD et puissance déformante | T04 | T02, T03 | à reprendre | 5 | 9/13 · relevé : 5 ép., 12 q. · 15 F, 6 P, 1 S · extraits : X-2018-01 (auto-test 5) · 13 schémas, générés par un script Python (scratchpad) · spectres de 2024-E2 DT3 lus par extraction de la courbe (notre lecture) · cartes corrigées : T04-f-001, f-002, f-004 à f-008 (tension sinusoïdale, Q_1, VA), f-013 à f-015, p-002, p-006, SVG de T04-s-001 redessiné · tour 1 : exactitude 4/5, 2 bloquants (notations prêtées aux cartes), 8 majeurs, 15 mineurs, tous corrigés (k ≥ 1 dans la somme de f-010, CEI 61000-3-2 par classes et 3-12 en % de I_ref, « sans pollution harmonique » de 2018-E2 confronté aux relevés, méthode « établir », convention récepteur, schéma du PD3 à six diodes, source de courant CEI au PCC, cartes f-010, f-011, f-012, p-002) ; tour 2 : exactitude 4/5, 0 bloquant, 2 majeurs (circuit de charge ouvert sur la figure 3, THD borné au rang 40 et conclusion des 8 % chiffrée : 4,7 %), 15 mineurs, tous corrigés (remède et lecture de 2024-E2 B12–B13, homonymies θ_n, L_σ, L_ch, k, empiètement et PFC définis, cartes f-002 et f-010) ; tour 3 : exactitude 4/5, 0 bloquant, 2 majeurs (rangs 3k annulés par i_a + i_b + i_c = 0 sans neutre, et non par la symétrie ; créneau à 48 % réservé à l'onduleur monophasé, 31 % en triphasé), 15 mineurs, tous corrigés (hypothèses de V_n = nX_cc I_n, rang 40 « compatibilité et émission », cause probable des raies de 1 kHz en 2024-E2, rang 5 qui augmente en MLI, marge laissée par 4,7 %, axes n, THD_i et THD_u, cartes p-002 et f-011) ; tour 4 : exactitude 4/5, 0 bloquant, 0 majeur, 11 mineurs, tous corrigés (V_n = |j n X_cc ∥ Z_n| I_n et résonance, rangs 6k ± 1 à k impair annulés à 12 pulsations, trois diodes pendant l'empiètement, Z_n sur la figure 9, homonymie de k avec le FP du chapitre 1, φ_n défini dans la fiche f-008, attribution du 25 % à la CEI 61000-2-2 contestée dans le cours, identifiants de cartes groupés dans les fiches de T02 et T04, carte f-012) ; tour 5 : exactitude 4/5, schémas, lisibilité et langue 4/5, couverture et progression 5/5, 0 bloquant, 0 majeur, 7 mineurs | Les 7 défauts mineurs du tour 5 (self anti-harmonique accordée vers le rang 4,3 avec son mécanisme ; condition |Z_n| ≫ nX_cc sur la figure 9, sa légende et la liste des schémas ; R_sce défini pour un appareil triphasé ; homonymie L_f (fuites au chapitre 2, filtre ici) signalée ; graduation 2f_MLI sur la figure 11 ; deux puces de plus de 6 lignes scindées ; « ordre de grandeur usuel ») sont corrigés mais n'ont pas été relus : faire un tour de relecture de confirmation en passe finale (exactitude à confirmer à 5/5). |
| 5. Transformateur monophasé et triphasé | T06 | T02, T03, T04 | à reprendre | 5 | 13/13 · relevé : 2 ép., 4 q. (en secondaire) · 14 F, 6 P, 1 S · extraits : X-2020-02 · 11 schémas, générés par un script Python (scratchpad) · aucune question dédiée dans les 22 épreuves : méthodes sur données réalistes, 2024-E2 B7–B9 et 2022-E1 Q22 (DR7) · cartes corrigées : T06-f-002, f-005 à f-014 (conditions, I_2cc, ΔV_2/V_20), p-001, p-003 (R_s = R_2 + m²R_1), p-006 (Dyn11), SVG de T06-s-001 redessiné · tour 1 : exactitude 2/5, 4 bloquants (sens d'enroulement de la figure 1, I_2cc employé pour le courant de défaut, « V_2 < mV_1 » faux en capacitif, indices horaires Yy/Yd réduits à 0 et 30°), 1 majeur (U_D de 2024-E2 dépend de la charge), 29 mineurs, tous corrigés (montage de l'essai en court-circuit, rappel Ampère–Hopkinson et signes de Faraday, Dyn11 et neutre chargé, 6 %/8 % du poste privé, tableau de document réponse, question de rendement, cartes f-001, f-009, f-012, f-013) ; tour 2 : exactitude 4/5, 0 bloquant, 1 majeur (prise de réglage proposée comme remède à la chute, qu'elle ne réduit pas), 18 mineurs, tous corrigés (circuit de la figure 6 fermé, chute d'un 250 kVA à x ≈ 0,77 en 2024-E2 et 439 V à vide, Yzn11 sur poteau, cinq paramètres avec m, FP à vide de la figure 5, hypothèses d'Hopkinson, points d'homologie des figures 3 et 4, angle θ sur la figure 7, homopolaire défini, P_2 = xP_2n, Dd0y11, flèche de V_1 sur la carte s-001, carte f-011) ; tour 3 : exactitude 4/5, couverture, schémas, progression et lisibilité 5/5, 0 bloquant, 0 majeur, 13 mineurs, tous corrigés (x = 258/352 ≈ 0,73 et 1,8 % en 2024-E2, chute due à R_s en amont d'un redresseur, rendement des petits transformateurs, Ampère sous forme intégrale et hypothèses d'Hopkinson, bornes homologues de Dyn11, indices compatibles par permutation, θ dans la légende de la figure 7, I_Rf en italique, fiches f-005, f-007, f-010, f-011, homonymies I_0 et indice s, u_k) ; tour 4 : exactitude 4/5, lisibilité et langue 5/5, 0 bloquant, 1 majeur (2022-E1 Q22, bloc « Transformer » 230 V eff → 15 V eff du DR7, absent du relevé : ajouté au chapitre, à cours/releve-sujets.json en secondaire de T06 et T08, et au constat), 8 mineurs, tous corrigés (FP 0,94 = P_T/S_T de B7 et chute en volts, 438,5 V à vide ; R_s par phase de l'étoile équivalente, fiche et carte f-008 ; somme algébrique d'Ampère ; zigzag ; V_1 et m de la figure 4 ; S_n défini ; PD2 défini et empiètement renvoyé au chapitre 4 ; carte f-012 en U = √3 V) ; tour 5 : exactitude 4/5, couverture, schémas, progression, lisibilité et langue 5/5, 0 bloquant, 0 majeur, 8 mineurs | Les 8 défauts mineurs du tour 5 (chaîne du DR7 de 2022-E1 rapprochée de la figure 11 sans dire que son filtrage, sans doute capacitif, porte la tension vers la crête, ≈ 19,8 V, et non 0,90 V_2 ; « B8 fait déduire U_D », 431 V étant notre calcul, et « abaisseur parfait » de B7 ; raison des 5 % donnée par B9, transformateur du domaine public ; B9 ajouté en secondaire de T06 au relevé, 2 ép., 4 q. ; I_2 et φ_2 indicés dans l'encadré ; libellé m V_1cc de la figure 6 ; « m » des figures 3 et 4 éloigné de X_m ; contrôles orphelins et numérotation de l'auto-test dans cours/calculs/T06.py) sont corrigés mais n'ont pas été relus : faire un tour de relecture de confirmation en passe finale (exactitude à confirmer à 5/5). |
| 6. Composants : diode, transistors, thyristor | T18 | T01 | à reprendre | 5 | 4/13 · relevé : 2 ép., 2 q. · 7 F, 7 P, 1 S · 12 schémas, générés par un script Python (scratchpad) · méthodes sur 2022-E1 Q27 (diode D1 redessinée), 2025-E2 Q24 (DR6) et 2024-E1 Q48 · cartes corrigées : T18-f-001 à f-004, f-006 (PD6 → PD3), f-007, p-001, SVG de T18-s-001 redessiné · tour 1 : exactitude 4/5, schémas 3/5, 0 bloquant, 2 majeurs (masse dessinée en symbole de terre sur trois figures ; R_B de l'exemple contraire à la règle de la valeur inférieure : la commande directe du bipolaire ne tient pas avec k ≥ 2), 22 mineurs, tous corrigés (MOSFET à enrichissement, r_d pente moyenne et nU_T/I, réversibilités de 2024-E1 Q48 sur un quadrant, ordre des commutations justifié par la diode, PD3 et P3 démontrés, méthode « établir » sur 2025-E2 Q27, Zener définie et triac dessiné, homonymies Q, T, k, s, B/L/S, E, V, notation V̂, point L sur la droite de charge, carte f-005) ; tour 2 : exactitude 4/5, couverture 5/5, 0 bloquant, 0 majeur, 23 mineurs, tous corrigés (tension du transistor et non de la diode pendant la commutation, Zener tête-bêche, seuil des MOSFET niveau logique, saturation du CAN et destruction distinguées, u_L et u_ch fléchés sur la figure 9, roue libre achevée en τ ln(1 + R_b I_0/V_s), 7,4 ms dans l'exemple, PD2 mixte défini, P3 avec neutre, I_min et I_max, v_c, V_cc/R_C, rail de masse de la figure 4, homonymies T, q, b, D, C, espaces fines, cartes f-005 et p-002) ; tour 3 : exactitude 4/5, couverture, progression et lisibilité 5/5, 0 bloquant, 0 majeur, 15 mineurs, tous corrigés (r_d inverse de la pente, origine de θ du PD3 et du P3, MOSFET silicium à 1 200 V, R_DS,on multipliée par 1,5 à 2, u = −v_AK définie, homonymies G, K et indice L, figure 11 du montage P3 ajoutée, courbes de la figure 6 arrêtées à V_cc, rail de masse relié au CAN, borne de commande, fiche f-006 en 3√3 V̂/π, courant d'attraction, Th nommé) ; tour 4 : exactitude 4/5, couverture et lisibilité 5/5, 0 bloquant, 1 majeur (carte T18-p-006 : V_GS > V_th ne suffit pas pour la région ohmique ; carte et piège corrigés, V_GS ≫ V_GS(th) à la valeur de la fiche), 15 mineurs, tous corrigés (r_d défini par la droite issue de V_s, IGBT avec ou sans diode, figure 11 recentrée sur un maximum, IGBT à trait interrompu et flèches v_DS, i_D, v_CE, i_C, cellule de la figure 8 rappelée, §8 renommé « Thyristor, triac et redresseurs », homonymies déplacées à leur première rencontre, Q NPN présenté au §4, nœud N et neutre, liens avec numéro de question, R_DS,on au féminin, θ et α en italique) ; tour 5 : exactitude 4/5, progression et lisibilité 5/5, couverture, schémas et langue 4/5, 0 bloquant, 0 majeur, 12 mineurs | Les 12 défauts mineurs du tour 5 (phrase de R_b réparée et distinguée de R_B ; t_on et t_off, durées de commutation et non de conduction comme au chapitre 7 ; courant limité du MOSFET près du seuil, sa région de saturation, et le piège p-006 ; « hors des commutations » pour la cellule ; hypothèses du triangle de puissance ; régime permanent pour ⟨u_L⟩ = 0, fiche et carte f-007 ; homonymies V_s, k, i_C, i_D avec le chapitre 1 et le drain ; v_GS, v_GE et V_BE fléchés ; V = E sur la figure 8 ; échauffement chiffré dans l'exemple, 23 K pour 200 K/W ; carte p-004 en E/(4Lf) ; calibre de 1 200 V justifié) sont corrigés mais n'ont pas été relus : faire un tour de relecture de confirmation en passe finale (exactitude à confirmer à 5/5). |
| 7. Hacheurs | T07 | T01, T18 | à reprendre | 5 | 12/13 · relevé : 5 ép., 34 q. · 13 F, 6 P, 1 S · extraits : X-2025-02 · 15 schémas, générés par un script Python (scratchpad) · méthodes sur 2023-E2 C3 à C8, 2025-E2 Q14, Q19, Q25 à Q35 (fraction aplatie de l'énoncé de Q35 signalée), 2023-E2 B3, 2022-E1 Q22, 2022-E2 Q30 à Q37, 2022-E1 Q21, 2024-E1 Q48 · recalculs : cours/calculs/T07.py, avec simulation des hacheurs série et parallèle (régime permanent par tir) et des bras entrelacés · cartes corrigées : T07-f-007 (« Δi/n » faux en général, remplacé par la formule exacte), f-006 et p-004 (pire cas de la plage, à E ou à V_s fixé), p-005 (commande unipolaire), notations V_s et E harmonisées, SVG de T07-s-001 redessiné · tour 1 : exactitude 3/5, 2 bloquants (ondulation unipolaire « jusqu'à quatre fois plus faible » : rapport (1 + |D|)/|D| ≥ 2 à tension moyenne égale, 4 entre les maxima, carte p-005 corrigée ; « coquille » de Q35 qui n'était qu'une fraction aplatie à l'extraction), 1 majeur (2023-E2 C6 : 1,25 mH et 0,90 mH, carte p-004), 25 mineurs, tous corrigés (figures du hacheur réversible en tension, de la commande unipolaire et des bras de 2025-E2 à α = 0,79 ajoutées ; sortie de la figure 4 en source fléchée ; M avec signe du continu ; R_ch ; contraintes de l'élévateur ; MPPT défini ; E′ = kΩ et C = kI admis ; DR3 de C7 résolu ; Q14, B3, Q22 cités ; condensateur et résistance série de l'exemple refaits ; homonymies f, R, D) · tour 2 : exactitude 4/5 (imprécisions de cartes), 0 bloquant, 0 majeur, 14 mineurs, tous corrigés (carte f-006 relabellisée « ondulation admissible », condition de conduction continue L ≥ α(1−α)E/(2f I_ch,min) ; questions des cartes f-003, f-005, f-009, f-010, f-012, f-013 et s-001 sans réponse au recto ; étiquette « T/2 − αT » de DT11 à lire αT − T/2 ; C_em = k⟨i⟩ et j entier au §5 ; I_s signalé ; formule générale de l'entrelacement justifiée pour les abaisseurs et les élévateurs ; 2025-E2 Q24 et 2024-E1 Q49 cités ; I_max et I_min sur la figure 5 ; u = v_A − v_B) · tour 3 : exactitude 3/5, 2 bloquants (carte p-005 restée en forme « vigilance », qui affichait l'erreur comme règle ; 2024-E1 Q49 : l'énergie de freinage reste sur le bus U_0, en aval du filtre, d'où les supercondensateurs de Q50 à Q53), 12 mineurs, tous corrigés (indices des cartes entre accolades pour « Grandeurs en jeu » ; i_b = i_L1 sur DT10 seul ; E′ = kΩ à flux constant ; MPPT et température ; lois générales de Kirchhoff de Q26 et v_D sur la figure 6 ; i_L sur la figure 4 ; q au lieu de k ; noms T_x, D_x propres à chaque figure ; formules en bloc ; « fermeture et ouverture » harmonisé avec le chapitre 6 et la carte f-008) · tour 4 : exactitude 4/5, 0 bloquant, 0 majeur, 15 mineurs, tous corrigés (exemple refait au pire à 26,4 µH, 33 µH à −20 % : Δi = 3,98 A, C ≥ 71 µF, résistance série ≤ 5,1 mΩ ; principe de l'entrelacement selon α ; « à flux constant » rattaché à E′ = kΩ ; i_b dans les lois de Q26 ; v_D = −V_s ; figures 2 et 4 dégagées ; symboles d'interrupteur commandé et d'IGBT nommés ; homonymies n et k ; cartes p-001 et p-002 sans jargon, f-005 sans unité, latex de f-008) · tour 5 : exactitude 4/5, couverture, progression, lisibilité et langue 5/5, schémas 4/5 ; 2 majeurs (légende de la figure 9 qui prêtait des diodes en antiparallèle aux transistors de la figure 10 ; carte f-009 ambiguë, le hacheur réversible en tension étant lui aussi à deux quadrants), 5 mineurs ; notes des tours 1 à 5 en exactitude : 3, 4, 3, 4, 4 | Les défauts du tour 5 (2 majeurs : légende de la figure 9, carte T07-f-009 reformulée sur la structure du bras ; 5 mineurs : « tension de la charge sans filtre L, C », légende de la figure 4 (E − V_s), « grandeurs en jeu » de f-001 (langle, rangle, lfloor, rfloor ignorés dans js/card-render.js), « à E fixé » dans f-003, teintes et contour en tirets de la figure 8) sont corrigés mais n'ont pas été relus : faire un tour de relecture de confirmation en passe finale (exactitude à confirmer à 5/5). |
| 8. Redresseurs | T08 | T02, T04, T06, T18 | à reprendre | 5 | 13/13 · relevé : 4 ép., 7 q. · 12 F, 6 P, 1 S · extraits : X-2026-02, X-2022-01 · 11 schémas, générés par un script Python (scratchpad) · méthodes sur 2023-E1 (PD3, Q16), 2024-E1 Q47 à Q49, 2022-E2 Q31 et Q32 (E = 207 V expliqué par le filtre L, C), 2022-E1 Q22 · recalculs : cours/calculs/T08.py, formes d'onde intégrées numériquement, empiètement simulé · cartes corrigées : PD6 renommé PD3 (nom usuel, celui de 2023-E1 et des chapitres 4 et 6), conditions vides de f-004, f-009, f-010 remplies, f-011 (ondulation crête à crête), p-003 et p-004 précisés, p-006 en forme « erreur », notations V̂ et I_DC harmonisées, SVG de T08-s-001 redessiné · tour 1 : exactitude 3/5, 2 bloquants (mention « les cartes l'appellent PD6 », contraire aux cartes corrigées ; vocabulaire de 2022-E1 Q22 mal cité, liste exacte et lecture du DR7 donnée), 4 majeurs (FP = cos φ1/√(1 + THD²) réservé aux courants sans composante continue, P3 traité par I² = I0² + I1² + I_H² ; bornes de la source renommées X et Y, courant i fléché, conventions dites ; recto de f-012 qui livrait « cos α », cos, sin, tan ignorés dans js/card-render.js ; méthode « Établir une valeur moyenne ou efficace » ajoutée), 22 mineurs, tous corrigés (figure de l'empiètement ajoutée, ligne du pont mixte sur la figure 10, L_r dessinée, zone d'onduleur assisté sous l'axe, V_RRM et V_DRM, Q1 = U_d0 I_d sin α, |cos α|, E′ admis, spectres de 2023-E1 Q16, homonymies D, q, t_on) ; tour 2 : exactitude 3/5, schémas 3/5, couverture 5/5, 0 bloquant, 4 majeurs (flèche de i inversée sur la figure 1 ; charge de la figure 10 réduite à R_ch et L, alors que le tracé à 120° exige une f.é.m. E′ < 0 : moteur M, R, L et E′ dessinés ; démonstration de l'empiètement ajoutée, v_K = (v1 + v2)/2 et aire L_rωI_d, u_d = 0 et aire 2L_rωI_d pour le PD2 ; « 14 V eff » du DR7 lu comme valeur efficace de la tension redressée, chapitre 6 harmonisé), 14 mineurs, tous corrigés (cos φ1 conditionné à l'empiètement, ≈ μ/2, et ≈ 0,95 avec condensateur ; tan 35,5° = 0,712 ; raie à 0 Hz du DR3 lue vers 565 V, écart à 540 V signalé ; intégrale du PD3 tout thyristors ; α en degrés ou radians ; I_H, Θ et E définis ; L_r notée L_s au chapitre 4 ; R_ch des charges résistives ; pont mixte nommé sur la figure 10 ; légendes des figures 4 et 9 ; récupération impossible derrière un pont à diodes ; aria-label de la figure 7 ; rectos des cartes ; paragraphes découpés) ; tour 3 : exactitude 4/5, couverture, schémas et langue 4/5, progression et lisibilité 5/5, 0 bloquant, 0 majeur, 16 mineurs, tous corrigés (amorçage et maintien du thyristor ; ΔU valable pour μ < 60°, μ < 180° en PD2 ; règles du §1 réservées aux commutations instantanées ; harmoniques du pont à condensateur nuancés, simulation à l'appui ; appellation PD6 dite impropre ; FP = facteur de distorsion I_1/I placé avant le cas du condensateur ; « 14 V eff » et bloc « Régulateur » harmonisés avec le chapitre 5 ; 2023-E1 Q16 complétée (u12, i_red, spectres en amplitude, 2,9 A = (2√3/π) × 2,6 A, contrôles ajoutés à T08.py) ; homonymie i_1 / I_1 signalée ; flèche de u_d de la figure 6 et étiquettes Th2, Th3 de la figure 10 déplacées ; typographie de p-004, seconde règle sans étiquette (css/style.css) ; « facteur de puissance du pont » ; 0,90 V pour un PD2, 1,35 U pour un PD3 ; antécédent de ΔU ; « Sans dimension » pour f-006 à f-008, U_inv de la carte f-010) ; tour 4 : exactitude 4/5, couverture, schémas, progression, lisibilité et langue 5/5, 0 bloquant, 0 majeur, 9 mineurs, tous corrigés (monophasé compté pour deux phases dans le nom PD2, q = 1 pour le PD2 dans S = qVI ; taux d'ondulation de 4,2 % et 48 % démontrés, U_eff² = Û²(1/2 + 3√3/(4π)), contrôles ajoutés à T08.py ; courants d'accrochage et de maintien, comme au chapitre 6 ; pont mixte « jamais négatif » ; écart de la raie à 0 Hz du DR3 dit propre au document ; grandeursEnJeu de js/card-render.js : un symbole surmonté ou souligné, Ū, Ū₀, Z souligné, reste un seul symbole, décor compris (cartes T03 et T08 améliorées) ; « Sans dimension, en % » pour f-011 ; puce du pont à condensateur raccourcie ; « 12 % de V̂ » sur la figure 4) ; tour 5 : exactitude 4/5, schémas et langue 4/5, couverture, progression et lisibilité 5/5, 0 bloquant, 0 majeur, 11 mineurs | Les 11 défauts mineurs du tour 5 sont corrigés mais n'ont pas été relus : règle de T08-p-005 conditionnée, au cours et sur la carte (hacheur série en conduction continue, pont tout thyristors à courant lissé) ; carte f-008, « le meilleur des trois montages PD2, P3 et PD3 », le pont à 12 pulsations faisant mieux ; L_r du PD2, inductance totale de la maille de la source ; inductance de lissage ajoutée au pont à diodes suivi d'un hacheur de l'exemple ; U_eff renommée U_d,eff dans la démonstration de l'ondulation, U_eff des cartes ajoutée aux notations ; 14 V eff du DR7 = 15 V moins deux chutes de diode ; carte s-001 (P2 à point milieu, « sur résistance » retiré) et phrase sur le P2 au §5 ; carte f-005 sans « q » ; inductance de lissage L nommée au §2 ; axes i, i1, v, v1 et graduation I_d sur la figure 9 ; grandeursEnJeu de js/card-render.js étendu à hat, widehat, tilde, vec, dot, ddot, et mathrm, mathbf, mathit, operatorname, displaystyle ignorés (cartes T09, T10, T12, T26 améliorées). Faire un tour de relecture de confirmation en passe finale (exactitude à confirmer à 5/5). |
| 9. Onduleurs et MLI | T09 | T04, T07 | à reprendre | 5 | 12/13 · relevé : 5 ép., 11 q. · 13 F, 7 P, 1 S · extraits : X-2025-01 · 14 schémas, générés par un script Python (scratchpad) · méthodes sur 2025-E2 Q20 à Q23 (DT8, DR5 ; Q22 au premier harmonique et rang par rang), 2023-E1 Q16 et Q17 (DR3 côté onduleur), 2024-E2 B12 et B13 (renvoi au chapitre 4), 2021-E2 Q13 et 2016-E1 Q29 (onduleurs photovoltaïques) · recalculs : cours/calculs/T09.py, spectres par transformée de Fourier des formes d'onde, MLI simulée, filtre de l'exemple rang par rang · cartes corrigées : conditions vides remplies (f-002, f-003, f-006, f-010 à f-013) ou réécrites pour ne pas livrer la réponse au recto (f-001, f-005), THD du créneau 0,483 et non 0,484 (f-004), unité VA de D (f-011), label « zone linéaire » de f-009, indices entre accolades (f-003, f-006, f-009, f-012), règles de p-001, p-002, p-004, p-006, p-007 et pièges p-003, p-005 (machine synchrone ou asynchrone), p-006 (2025-E2) ; js/card-render.js : \infty ignoré · tour 1 : exactitude 3/5, couverture, schémas, progression, lisibilité et langue 4/5, 2 bloquants (carte f-005 écrite en V_n, valeur efficace dans le chapitre, corrigée en amplitude V̂_n ; 2021-E2 Q13 : 24 panneaux ne suffisaient pas par temps froid, DT7 lu, +8 % à 0 °C, 22 panneaux au plus, ou deux chaînes de 13 par entrée), 3 majeurs (τ = T/4 dans la légende de la figure 4 ; auto-test 6 à courant supposé sinusoïdal, et non charge « très inductive » ; titre de la carte p-001, qui livrait la réponse), 27 mineurs, tous corrigés (MOSFET conducteur en inverse ; raison de la commande complémentaire ; |cos nψ| ; raie de rang m_f absente des composées quel que soit m_f, multiple de 3 pour l'équilibre en MLI synchrone, carte f-008 ; 11 % en Q22 ; i_Lf de 12,8 A et 19,3 A crête à 230 V régulés ; réserve de 2016-E1 par forte chaleur ; plage assignée de 500 à 800 V de 2021-E2 ; méthode « synoptique en site isolé » pour 2016-E1 Q30 ; compte des questions ; amplitude réglable par commande décalée ; légendes des figures 1 et 7 ; figure 14 appelée, avec flèches de puissance ; figure 15, montage de l'exemple ; figures 8 et 12 aérées ; homonymies N_s et C ; « p » du §6 ; citation exacte de 2023-E1 ; DR5 pour la porteuse ; chapitre 2 en prérequis, E et u_f du chapitre 7 ; loi V/f admise ; cartes p-005, f-009, p-003, p-007) ; tour 2 : exactitude 4/5, tous les critères à 4/5, 0 bloquant, 1 majeur (2025-E2 Q22 : P = S cos φ n'est pas le premier harmonique mais l'approximation sinusoïdale ; vrai premier harmonique ajouté, V1 ≈ 207 V, I1 ≈ 11,5 A, P1 ≈ 2,35 kW, Q1 ≈ 0,42 kvar, 0,30 kW portés par les harmoniques), 20 mineurs, tous corrigés (Sunny Boy à MPPT intégré et batteries côté continu ou alternatif en 2016-E1 Q30 ; coefficient −0,3 %/K et +7,5 % à 0 °C ; 446 V sous la plage assignée ; NOCT de l'annexe A2, 196 V ; origine des phases de p(t) ; variateurs de machines alternatives ; carte f-010 (question et conditions), p-007 (titre), f-003 (conditions) ; js/card-render.js : bornes de Σ, Π, ∫ ignorées dans les grandeurs en jeu ; bras de la figure 3 continus ; figure de l'exemple complétée (R, L, i, flèche VDC) ; V_nom et f_nom sur la figure 13 ; formule de V en six marches lisible ; 1 à 20 kHz ; rangs pairs ; chapitre 1, §10 ; 2025-E2 Q14 renvoyée au chapitre 7 ; double sens d'« îlotage » et protection de découplage ; homonymie N ; tournures) ; tour 3 : exactitude 4/5, couverture et progression 5/5, schémas, lisibilité et langue 4/5, 0 bloquant, 1 majeur (2016-E1 Q30 : les Sunny Boy, onduleurs de réseau, ne forment pas le réseau ; couplage côté alternatif par un onduleur-chargeur réversible), 18 mineurs, tous corrigés (THD limité au rang 40 par les normes, 47,0 % et 29,7 % ; ondulations du bus triphasé autour de f_p et 2f_p ; courant inversé par les diodes ou le canal des MOSFET du DT8 ; 3 kVA de Q22 incohérents avec R0 et L, 2,94 kVA ; 0 °C posé en hypothèse, 22 panneaux à −10 °C, 21 à −20 °C ; φ défini ; « presque tous les variateurs » ; ±540 V comme au chapitre 4 ; THD_u signalé ; v_NO tracé sur la figure 8, V̂_ref et V̂_p sur la figure 9, légende de la figure 13 dans le cadre, i_B et i_C cités figure 7 ; cartes f-003 (rang 40), f-007 et f-008 (questions), f-010 (S²), p-006 (titre), p-007 (six transistors) ; js/card-render.js : « ; » final des rectos changé en point) ; tour 4 : exactitude 4/5, couverture, progression et lisibilité 5/5, schémas et langue 4/5, 0 bloquant, 1 majeur (piège p-003 : règle 6k ± 1 réservée à la pleine onde, et en MLI à m_f impair multiple de 3, au cours et sur la carte), 8 mineurs, tous corrigés (familles impaires annulées en unipolaire justifiées par (−1)^k ; régulateurs de 2016-E1 Q30 placés ; citation exacte de l'annexe A3 ; « seul convertisseur statique, à partir d'une source continue » ; v1 nommé figure 5 ; « 3∼ » dans le cercle du moteur, figure 13 ; −VDC gradué figure 4 ; js/card-render.js : espace avant le point final des rectos supprimée, 26 cartes concernées) ; tour 5 : exactitude 4/5, couverture, progression et lisibilité 5/5, schémas et langue 4/5, 0 bloquant, 2 majeurs, 7 mineurs | Les 9 défauts du tour 5 sont corrigés mais n'ont pas été relus : 2016-E1 Q29 (annexe A3 citée en entier, 16 A par entrée et trois entrées ; une chaîne par entrée ; aux conditions NOCT, 196 V et 242 V à vide, sous la plage MPPT et sous le démarrage ; répartition sans réserve en sept chaînes de 8 modules, 239 V, 224 V NOCT, 298 V à vide, 3 920 W) ; carte p-002 (titre « Dénominateur du THD », piège qui ne livre plus la réponse) ; figure 15 nouvelle, couplage côté alternatif de 2016-E1 Q30 (l'exemple passe en figure 16) ; ondulations du bus triphasé, famille de 2f_p dominante aux indices moyens seulement ; auto-test 2 jugé aussi rang par rang (rang 3 à 6 % pour 5 % admis : non conforme) ; « 1 000 VA » insécable ; « côté continu » au lieu de « continus » ; trois tournures ; −I_max gradué sur la figure 4. Faire un tour de relecture de confirmation en passe finale (exactitude à confirmer à 5/5). |
| 10. Filtres du premier et du second ordre | T20 | T03 | à reprendre | 5 | 5/13 · relevé : 0 ép., 0 q. · 12 F, 7 P, 1 S · extraits : X-2026-03 · 14 schémas, générés par un script Python (scratchpad), plus le schéma de la carte s-001 redessiné (svg/T20-s-001.svg) · aucune question dédiée : méthodes sur les questions voisines, 2023-E2 D4 (Bode à deux pôles du DR4, 26,4 dB indiqués, notre lecture : ω_a ≈ 10 rad/s, ω_b ≈ 7·10³ rad/s), 2024-E2 C5 (forme canonique), 2021-E1 Q31 et Q32 (réponse indicielle du premier ordre), 2022-E2 Q31 (filtre L, C de bus continu), 2024-E1 Q47 (grandeurs en amont du bloc filtre) · exemple : anti-repliement d'un analyseur de réseau (premier ordre, cascade, Butterworth, doublement de f_e, RLC à f_0 = 3 kHz) · recalculs : cours/calculs/T20.py, fonctions de transfert recalculées sur les circuits par analyse nodale, réponses indicielles intégrées (RK4) · cartes corrigées : conditions remplies (f-001, f-002, f-004 à f-006, f-008 à f-012), labels sans « (source : …) » ni doublon (f-003 à f-005, f-008, f-011, f-012), indices entre accolades et LaTeX sans V_3/V_2 ni \Longrightarrow (f-002 à f-004, f-007, f-012), pièges p-002, p-004, p-005 réécrits en erreurs, p-003 sans « gain nul » ambigu ; js/card-render.js : grandeurs en jeu prises dans le membre de droite de chaque relation (séparateurs « ; », \qquad, \quad\text{avec}\quad), texte de \text{} et flèches logiques ignorés · tour 1 : exactitude 3/5, autres critères 4/5, 2 bloquants (2023-E2 D4 : ω_b relu au pixel sur le DR4, 7·10³ rad/s et non 3,5·10³, d'où m ≈ 13 ; 2024-E1 Q47 porte sur v₁, i₁, v₂, i₂ en amont du bloc « FILTRE », plus citée comme filtre L, C), 1 majeur (recto de f-012 qui livrait la réponse, conditions réordonnées), 18 mineurs, tous corrigés (dépassement D justifié par les racines du dénominateur ; condensateur initialement déchargé ; « passe-bas d'ordre n » ; H₀ dans les notes de f-004 et f-008 ; images autour de 2f_e dans l'exemple ; PD2, PD3 et f_p avec renvois aux chapitres 8 et 9 ; « n égal à l'ordre du dénominateur » ; homonymies G, Q et indice e ; ±45° explicité ; 26,4 dB « indiqué » par le DR4 ; citation de 2022-E2 Q31 ; figures 2, 8, 10 et 13 ; fractions en ligne ; grandeurs en jeu sans j et avec indices des lettres grecques, \mathcal ignoré ; règle de p-006 avec la condition du critère du revers ; langue) · tour 2 : exactitude 3/5, couverture, schémas et langue 4/5, progression et lisibilité 5/5, 1 bloquant (critère de charge : R_ch ≫ |Z₁ ∥ Z₂|, impédance de Thévenin du filtre, et non |Z₂|), 3 majeurs (p-003 restreint au passe-bas, le passe-haut en deçà ; τ lu à 63 % de la variation depuis l'échelon, K = Δs/Δe, forme réelle de 2021-E1 Q32 ; ondulation de bus à 2f derrière un onduleur monophasé, chapitre 9 §6, et filtre de sortie MLI distingué), 18 mineurs, tous corrigés (H₀/(2m) réservé au passe-bas, carte f-004 comprise ; phase du passe-bas sans zéro et zéro instable, cartes p-006 et intégrateurs admis ; « loin au-delà » ; minimum à pulsation non nulle ; m = 1 et m > 1 justifiés par la dérivée ; phase de l'analyseur ; zéros dans les méthodes Bode ; coupe-bande ; conduction continue du filtre L, C ; k défini ; −12,55 dB ; homonymie de D ; « la plupart des cartes » ; figure 13 ajoutée, filtre L, C de bus avec R_ch ; courants I₁, I₂, I₃ fléchés en figure 10 et convention récepteur ; renvoi au chapitre 2 pour 2023-E2 D5 à D8 ; recto de la carte s-001 sans pente ni points remarquables ; unité de f-004) · tour 3 : exactitude 4/5, couverture, progression et lisibilité 5/5, schémas et langue 4/5, 0 bloquant, 1 majeur (méthode du filtre L, C : f_r réseau et f_ond ondulation, atténuation (f₀/f_ond)², ondulation de courant à 2f d'un onduleur monophasé sortie de la liste, fournie par C seul, ≈ Î/(2π·2f·C)), 14 mineurs, tous corrigés (points sûrs du Bode relatifs aux asymptotes et contributions de phase ; « loin au-delà » ; symétrie du passe-haut, gain seul, phase + 90° ; carré du dénominateur ; tangente à l'instant de l'échelon ; filtre de sortie MLI « autre rôle » ; p-006 avec un seul passage à 0 dB ; V_e, V_s complexes en figure 10 ; étiquette 0,95 E de la figure 6 ; tension « appliquée » ; K = H₀ ; espaces fines avant unités ; js/card-render.js : « Résultat sans dimension » au recto ; libellés de T20.py) · tour 4 : exactitude 4/5, couverture, progression et lisibilité 5/5, schémas et langue 4/5, 0 bloquant, 0 majeur, 13 mineurs, tous corrigés (zéro à partie réelle positive dans les marches de phase ; passe-bas « sans zéro » ; puissance moitié dans une résistance qui ne charge pas ; f_réseau ; « pôle stable, retard d'au plus 90° », carte p-006 comprise ; V_A fléchée et graduations en figure 10 ; indices romains Z_R, Z_L, Z_C et u_C ; grandeurs en jeu coupées aussi sur les inégalités quand il n'y a pas d'égalité ; 2021-E1 Q32 lue jusqu'au bout, K ≈ 60 kN·m·V⁻¹ et τ ≈ 60 min, document réponse R4 ; 2023-E1 Q16 ; figure 5 ; titre « Filtres du premier et du second ordre ») · tour 5 : exactitude 4/5, couverture 5/5, schémas, progression, lisibilité et langue 4/5, 0 bloquant, 0 majeur, 16 mineurs · notes des tours 1 à 5 en exactitude : 3, 3, 4, 4, 4 | Les 16 défauts mineurs du tour 5 sont corrigés mais n'ont pas été relus : pente du passe-bande (±20 dB par décade loin de ω₀ seulement, chute plus raide près de ω₀ quand Q est grand, seule imprécision scientifique retenue) ; titre de méthode sans $…$ (le sommaire n'interprète pas KaTeX) ; pôles, zéros, pôle stable et minimum de phase définis au §2 ; étiquette « −6 dB/octave » de la figure 5 dégagée ; graduations ω₀/10 et 10 ω₀ de la figure 11 ; appel de la figure 14 ; 2023-E2 D5 à D8 « reprises aux chapitres 12 à 14 » ; « sa figure 18 », C_bras et U_com définis ; espaces fines avant kN·m ; auto-tests 2 et 6 en atténuations positives ; étapes de méthode coupées (paragraphes ≤ 6 lignes) ; indices romains Z_L, Z_C des Formules clés ; ponctuation de « H² = 1/2 » ; « réseau à 50 Hz » ; u_red notée u_d au chapitre 8 ; js/card-render.js : ≈ traité en dernier recours dans grandeursEnJeu, latex de f-012 séparé par \qquad. Faire un tour de relecture de confirmation en passe finale (exactitude à confirmer à 5/5). |
| 11. Amplificateur opérationnel | T19 | T01, T20 | en cours | 0 | 4/13 · relevé : 3 ép., 16 q. · 12 F, 7 P, 1 S · extraits : X-2023-01 · 17 schémas, générés par un script Python (scratchpad), symbole CEI ▷∞ comme au chapitre 1, plus le schéma de la carte s-001 redessiné (svg/T19-s-001.svg) · méthodes sur 2024-E2 E1 à E10 (amplificateur d'instrumentation de sa figure 22, décalage de sa figure 23, montage de Howland de sa figure 24, DR10, boucle 4–20 mA ; G1 = 3,397 donne 339,7·e_AB, le sujet écrit 337,7), 2023-E2 F6 à F10 (comparateur inverseur à hystérésis, seuils 2,503 et 2,305 V, DR6), 2025-E1 Q59 (gain d'un amplificateur différentiel) · filtres actifs : premier ordre et Sallen et Key, qui remplace la bobine de l'exemple du chapitre 10 · exemple : alarme de température à LM35, gain 10 et trigger non inverseur 35/32 °C · recalculs : cours/calculs/T19.py, montages résolus par analyse nodale avec un AOP de gain fini, comparateurs simulés pas à pas · cartes corrigées : unités de f-007 et f-009 (sans dimension), conditions remplies (f-004 à f-010), indices entre accolades (f-001 à f-012), saturation de f-011 ((R_ref + R_ch)·I_s < V_sat, question reformulée : c'est la charge qui est dans la boucle), f-001 sans ±V_cc, label de f-010 sans source, p-003 et p-005 en erreurs, p-006 (trigger inverseur et non inverseur distingués), p-007 (charge flottante et Howland), s-001 redessinée (caractéristique descendante du trigger inverseur) et réponse corrigée · tour 1 : exactitude 3/5, schémas 3/5, autres critères 4/5, 3 bloquants (cycle d'hystérésis non fermé dans la figure du trigger et la carte s-001 ; courants de la figure de Howland, redessinée comme sa figure 24 du sujet, R vers l'entrée +, fil + → A portant I₂′ ; bruit du LM35 compté après le gain, 10 mV sur v_a), 2 majeurs (recto de f-005 qui livrait la condition ; étapes de méthode « gain 1 attendu » et « même courant que sa voisine » fausses en général), 18 mineurs, tous corrigés (produit gain-bande et gain de bruit ; 4/(11,8·10⁻³) ; 25,03 % et 23,05 % ; légende « en bas » ; étiquette I_s ; source traversée par le conducteur ; v₂ de la figure 6 ; coupure de f-006 ; titres de p-001 et p-007 ; homonymies ; R = R₅ ; notes de f-010 et f-012 ; espaces fines avant µV ; rappel p = jω et notation de Laplace sans soulignement ; 2025-E1 Q59 chiffrée, notre lecture de sa figure 31, K_A ≈ 1,5·10⁵ ; DT6 cité ; nouvelle figure 11, passe-bas actif du premier ordre, figures suivantes renumérotées) | — |
| 12. Modélisation des systèmes linéaires | T26 | T01, T20 | à faire | 0 | 9/13 · relevé : 8 ép., 29 q. · 10 F, 7 P, 1 S | — |
| 13. Fonctions de transfert et diagramme de Bode | T21 | T20, T26 | à faire | 0 | 8/13 · relevé : 2 ép., 5 q. · 13 F, 8 P, 1 S · extraits : X-2023-02 | — |
| 14. Systèmes bouclés, correcteurs, stabilité | T27 | T21, T26 | à faire | 0 | 9/13 · relevé : 9 ép., 31 q. · 9 F, 7 P, 1 S | — |
| 15. Machine à courant continu | T11 | T07, T26 | à faire | 0 | 10/13 · relevé : 1 ép., 2 q. · 15 F, 6 P, 1 S | — |
| 16. Machine asynchrone | T13 | T02, T06, T26 | à faire | 0 | 7/13 · relevé : 8 ép., 37 q. · 17 F, 7 P, 1 S · extraits : X-2019-01 | — |
| 17. Machine synchrone et brushless | T12 | T09, T13 | à faire | 0 | 4/13 · relevé : 3 ép., 5 q. · 11 F, 6 P, 1 S | — |
| 18. Variation de vitesse | T14 | T09, T11, T13, T27 | à faire | 0 | 5/13 · relevé : 6 ép., 18 q. · 9 F, 7 P, 1 S · extraits : X-2021-01 | — |
| 19. Stockage d'énergie électrique | T15 | T01, T07 | à faire | 0 | 5/13 · relevé : 11 ép., 58 q. · 10 F, 7 P, 1 S · extraits : X-2020-01 | — |
| 20. Distribution BT, protection et régimes de neutre | T17 | T02, T06 | à faire | 0 | 5/13 · relevé : 8 ép., 36 q. · 7 F, 7 P, 1 S | — |
| 21. Capteurs et conditionnement du signal | T23 | T19, T20 | à faire | 0 | 9/13 · relevé : 11 ép., 60 q. · 4 F, 6 P, 1 S · extraits : X-2024-01 | — |
| 22. CAN, CNA et échantillonnage | T22 | T20, T23 | à faire | 0 | 6/13 · relevé : 5 ép., 26 q. · 9 F, 6 P, 1 S · extraits : X-2026-04 | — |
| 23. Métrologie, instrumentation, schématisation | T30 | T01, T22, T23 | à faire | 0 | 12/13 · relevé : 9 ép., 12 q. · 7 F, 8 P, 1 S | — |
| 24. Logique combinatoire | T28 | — | à faire | 0 | 3/13 · relevé : 3 ép., 8 q. · 3 F, 6 P, 1 S | — |
| 25. Logique séquentielle, GRAFCET, automates | T29 | T28 | à faire | 0 | 5/13 · relevé : 7 ép., 12 q. · 0 F, 7 P, 1 S | — |
| 26. Systèmes embarqués : microcontrôleurs, API, FPGA | T24 | T22, T28, T29 | à faire | 0 | 6/13 · relevé : 17 ép., 49 q. · 2 F, 6 P, 1 S | — |
| 27. Transmission numérique et protocoles | T25 | T24, T28 | à faire | 0 | 4/13 · relevé : 8 ép., 48 q. · 10 F, 6 P, 1 S · extraits : X-2026-01 | — |

## Infrastructure construite avec le premier chapitre

Mise en place à l'itération du chapitre 1 (T01), documentée dans README-app.md
(section « Cours ») :

- [x] `cours/textes/TXX.html` : un fragment HTML par chapitre (pas de
      `<html>`, pas de `<body>`), titres `<h2>`/`<h3>` munis d'un `id`
      préfixé par le thème (`t01-bref`, `t01-ohm`…).
- [x] `cours/index.json` : `{"chapitres": [{"id", "theme", "ordre", "titre",
      "prerequis": [...], "sommaire": [{"niveau": 2|3, "texte", "id"}],
      "schemas": N}]}`, dans l'ordre du plan. À générer par un script
      (`scripts/indexer_cours.py`) qui lit les fragments, plutôt qu'à la main.
- [x] `js/views/cours.js` : liste des chapitres (`#/cours`) et lecteur
      (`#/cours?theme=TXX`) sur le modèle de `vueEpreuve`
      (`js/views/sujets.js`) : sommaire replié, `rendreMathsDans`, schémas SVG
      agrandissables par `ouvrirPleinEcran`, chapitre précédent / suivant.
- [x] Route `#/cours` dans `js/app.js` (rattachée à l'onglet Catégories pour
      `aria-current`, pas de nouvel onglet dans la barre du bas).
- [x] Écran Catégories (`js/views/categories.js`) : bouton « Lire le cours »
      par catégorie (premier chapitre de la catégorie) et par thème, plus un
      accès à la liste des chapitres. Thèmes hors périmètre : pas de bouton.
- [x] `sw-cours.js` (`self.ASSETS_COURS = [...]` : `cours/index.json` et les
      fragments), importé par `sw.js` comme `sw-sujets.js` ; ajouter
      `./js/views/cours.js` au `SOCLE`. Changer `CACHE_VERSION` dans
      `sw-assets.js` à chaque modification du cours. `build_cards.py`, qui
      générait ce fichier, n'est pas dans ce dépôt : écrire la commande de
      mise à jour (hash du contenu précaché) et la documenter dans
      `README-app.md`.
- [x] Styles du lecteur dans `css/style.css`, avec les jetons existants
      (`--accent`, `--ink`, `--surface`…) : encadré « Formules clés »,
      `<details>` de l'auto-test, `figure`/`figcaption`, `.table-scroll`.
- [x] Harnais de vérification réutilisable (`scripts/verifier_cours.mjs`,
      Playwright Node global 1.56.1 ; Chromium dans `/opt/pw-browsers`) :
      393×852, `isMobile`, thèmes clair et sombre, erreurs KaTeX et console,
      `scrollWidth` = 393, taille rendue des `<text>` SVG ≥ 12 px, largeur
      des formules ≤ 340 px, cibles tactiles ≥ 44 px, captures pleine page.
      Plus un script Python : orthographe (`pyspellchecker`, français) et
      contrôle des ids de cartes cités contre `cards.json`.
- [x] Liens vers une carte : tranché, route `#/reviser?carte=<id>` (une seule
      carte, « Retour au cours » ramène au chapitre). Écrire
      `<a class="id-carte" href="#/reviser?carte=T07-f-003">T07-f-003</a>`.

## Conventions communes à tous les chapitres

Fixées ici pour que la passe finale n'ait pas à harmoniser après coup.

- Structure fixe en onze rubriques (voir la consigne) : En bref, Prérequis,
  L'idée physique, Cours, Schémas, Formules clés, Méthode concours, Pièges,
  Exemple chiffré résolu, Auto-test, Pour réviser.
- Grandeurs : minuscule pour l'instantané ($v(t)$, $i(t)$), majuscule pour
  l'efficace ($V$, $I$), $\langle v\rangle$ pour la moyenne, $\hat V$ pour
  l'amplitude, soulignement pour le complexe ($\underline{V}$), $V$ tension
  simple et $U$ tension composée en triphasé, $\omega$ pulsation électrique,
  $\Omega$ vitesse angulaire en rad/s et $N$ en tr/min (notation des cartes), $p$ variable de
  Laplace (et nombre de paires de pôles en machines : le dire quand les deux
  se côtoient), $\alpha$ rapport cyclique (et angle d'amorçage en T08 : le
  signaler).
- Indices : descriptifs en romain (`\mathrm{}` dans les formules,
  `font-style="normal"` dans les SVG) : $V_\mathrm{s}$, $R_\mathrm{th}$,
  $P_\mathrm{J}$, $i_\mathrm{L1}$ ; indices variables en italique ($E_k$,
  $\varphi_i$) ; noms de points en romain ($\mathrm{A}$, $\mathrm{N}$) ; grandeur
  continue en majuscule (courant $I$, f.é.m. $E$), instantanée en minuscule
  (potentiels $v_\mathrm{A}$, f.é.m. $e$) ; charge notée $R_\mathrm{ch}$.
  Renvoyer à une figure d'un sujet par « sa figure N » ou « figure N du
  sujet », jamais « figure N » seul (confusion avec les figures du cours).
  Un schéma de carte faux se redessine dans `svg/TXX-s-00N.svg`
  et se redirige par le champ `svg` de `corrections/cartes.json` ;
  `indexer_cours.py` l'ajoute au précache.
- Conventions de signe : récepteur par défaut, générateur pour les sources ;
  la convention est dite dans le texte et visible sur le schéma (flèches de
  tension et de courant).
- Nombres : virgule décimale, espace fine avant l'unité, unités SI, puissance
  en W, var, VA (jamais « VAR » ni « kVAR »).
- Schémas : symboles IEC 60617 (résistance rectangulaire, inductance en
  demi-cercles, masse et terre distinctes), SVG inline écrit à la main,
  `viewBox` de 360 de large au plus, `stroke="currentColor"`, accent en
  `var(--accent)`, `role="img"`, `aria-label`, `<figcaption>`. Le corps du
  texte du lecteur fait environ 337 px de large sur l'iPhone 17 : une police
  de 13 unités dans un `viewBox` de 360 rend à environ 12,2 px. Viser 13 au
  minimum et mesurer.
- Citations d'épreuves : « [2024-E2, B7](#/epreuve?id=2024-E2) ». Les numéros
  de question sont ceux du sujet ; le détail de chaque question est dans
  `cours/releve-sujets.json`.
- Formules clés : chaque formule porte l'id de sa carte (ex. T07-f-003). En cas
  de désaccord entre le cours et une carte, revenir à la physique ; si la carte
  est fausse, la corriger dans `corrections/cartes.json` (voir README-app.md)
  et le noter dans la colonne « notes ».
- Complexes (depuis T03) : unité imaginaire $\mathrm{j}$ en romain, y compris
  dans les SVG ; module = valeur efficace ; $\varphi = \varphi_u - \varphi_i$
  (déphasage de la tension sur le courant), à dire en toutes lettres ;
  facteur de puissance $\mathrm{FP}$ (noté $k$ au chapitre 1) ; $\mathrm{THD}_i$
  (indice en italique, comme $\varphi_i$) ; phase asymptotique d'un Bode en
  marches. Toute homonymie (Q, X, p, G, C, K, V_s…) est signalée à sa
  première rencontre. Les conditions de validité d'un critère (marge de
  phase : boucle ouverte stable, intégrateurs admis, un seul passage à 0 dB)
  sont écrites partout où le critère apparaît, cartes comprises.
- Puissances (depuis T02) : $Q_\mathrm{C}$ est le réactif absorbé par une
  batterie de condensateurs, négatif ($Q_\mathrm{C} = -3C\omega V^2$, convention
  des cartes T02) ; le chapitre 1 l'employait au sens « fourni », positif, ce que
  T02 signale. Facteur de puissance $\mathrm{FP}$, $\mathrm{THD}_i$ ; identifiants de
  cartes groupés par formule quand plusieurs cartes portent la même relation.
- Chiffres tirés d'un sujet : vérifier qu'ils sont cohérents entre eux (S,
  P, FP…) et dans quel régime ils valent (sinusoïdal ou non) ; lire les
  documents (DT, DR) avant de citer une valeur, et dire « notre lecture »
  quand elle est lue sur une courbe.

## Constats du relevé des épreuves (2026-10-13)

- **2019-E2 est le mauvais sujet.** `sujets/textes/2019-E2.html` contient
  l'épreuve de l'option Ingénierie des constructions (Pont de la Citadelle,
  Strasbourg), et non « Transformation d'une rame de métro » annoncé par
  `sujets/index.json`. À corriger à la source (`scripts/integrer_sujets.py`
  et le dépôt des sujets, hors de ce dépôt). Ne pas citer 2019-E2 dans le
  cours.
- 2015-E2 et 2016-E2 sont des épreuves d'exploitation pédagogique (quatre
  questions chacune, sans calcul).
- Les épreuves 1 sont communes à toutes les options : mécanique (T10),
  thermique (T05) et questions hors programme électrique y dominent. Les
  questions d'électrotechnique se trouvent surtout dans les épreuves 2 de
  2017 à 2025.
- **Aucune question dédiée** au transformateur (T06) ni aux filtres (T20)
  dans les 22 épreuves de l'app : le transformateur n'y apparaît que comme
  « transformateur parfait » en contexte (2024-E2, B7–B9) et comme bloc
  fonctionnel « Transformer » d'une alimentation (2022-E1, Q22, DR7). Les 13 sujets
  sur lesquels `cards.json` compte les fréquences forment un autre corpus.
  Pour ces chapitres, la méthode concours s'appuie sur les questions voisines
  (chute de tension au secondaire, filtrage d'un conditionneur ou d'un
  anti-repliement) et le dit franchement.
- Formes dominantes, tous thèmes confondus : calcul, « établir une
  expression », compléter un document réponse, conclure sur une conformité à
  un cahier des charges. La méthode concours de chaque chapitre doit couvrir
  ces quatre gestes.

## Relevé par thème

Numéros de question tels qu'imprimés dans le sujet ; le thème est principal
sauf mention « secondaire ». 2019-E2 est listé pour mémoire (mauvais sujet).

### T01 — Grandeurs électriques fondamentales et électrocinétique

Cartes : tombe dans 13 sujets sur 13 · 20 formules, 6 pièges, 2 schéma(s).  
Relevé 2015–2025 : 17 épreuves, 78 questions (30 en thème principal).  
Formes : calcul 40 · établir une expression 24 · lecture de documentation 5 · compléter document réponse 3 · justifier/expliquer 3

- [2025-E1](#/epreuve?id=2025-E1) : — (secondaire : 56, 57)
- [2025-E2](#/epreuve?id=2025-E2) : Q1, Q2, Q25, Q26, Q36 (secondaire : Q4, Q8, Q21, Q27, Q31)
- [2024-E1](#/epreuve?id=2024-E1) : 37, 40 (secondaire : 4, 38, 39, 41)
- [2024-E2](#/epreuve?id=2024-E2) : — (secondaire : E1, E4, E6, E7, E8, E9)
- [2023-E2](#/epreuve?id=2023-E2) : B2 (secondaire : C1, C2, C3, C4, F2, F6, F7)
- [2022-E1](#/epreuve?id=2022-E1) : 4, 5
- [2022-E2](#/epreuve?id=2022-E2) : 25, 33, 34
- [2020-E1](#/epreuve?id=2020-E1) : 19
- [2020-E2](#/epreuve?id=2020-E2) : 9, 14 (secondaire : 3, 13)
- [2019-E1](#/epreuve?id=2019-E1) : 4, 16 (secondaire : 8, 18)
- [2019-E2](#/epreuve?id=2019-E2) : — (secondaire : 13)
- [2018-E1](#/epreuve?id=2018-E1) : — (secondaire : 18, 21, 22)
- [2018-E2](#/epreuve?id=2018-E2) : 11, 28, 29 (secondaire : 4, 5, 10, 27)
- [2017-E1](#/epreuve?id=2017-E1) : — (secondaire : 24)
- [2017-E2](#/epreuve?id=2017-E2) : C1.1, C1.2, C3.1, C3.3, C3.5, C3.7, C3.9, D2.3 (secondaire : C3.2, C3.4, C3.6, C3.8, C3.10, D1.1, D2.2, D2.4)
- [2016-E1](#/epreuve?id=2016-E1) : — (secondaire : 17, 18, 19)
- [2015-E1](#/epreuve?id=2015-E1) : 29

### T03 — Représentation complexe et impédances

Cartes : tombe dans 12 sujets sur 13 · 19 formules, 6 pièges, 1 schéma(s).  
Relevé 2015–2025 : 3 épreuves, 4 questions (1 en thème principal).  
Formes : calcul 3 · établir une expression 1

- [2025-E2](#/epreuve?id=2025-E2) : — (secondaire : Q22)
- [2024-E2](#/epreuve?id=2024-E2) : — (secondaire : A4)
- [2018-E2](#/epreuve?id=2018-E2) : 10 (secondaire : 11)

### T02 — Puissance en régime alternatif sinusoïdal (AC)

Cartes : tombe dans 13 sujets sur 13 · 35 formules, 8 pièges, 1 schéma(s).  
Relevé 2015–2025 : 8 épreuves, 26 questions (18 en thème principal).  
Formes : calcul 16 · justifier/expliquer 3 · choix/dimensionnement 3 · établir une expression 2 · lecture de documentation 2

- [2025-E2](#/epreuve?id=2025-E2) : Q22
- [2024-E1](#/epreuve?id=2024-E1) : — (secondaire : 46)
- [2024-E2](#/epreuve?id=2024-E2) : B1, B2, B3, B4, B6, B7 (secondaire : A5, B8)
- [2021-E1](#/epreuve?id=2021-E1) : — (secondaire : 18)
- [2020-E2](#/epreuve?id=2020-E2) : — (secondaire : 19, 20)
- [2018-E2](#/epreuve?id=2018-E2) : 13, 14, 15, 27 (secondaire : 7, 8)
- [2017-E2](#/epreuve?id=2017-E2) : B1.1, B1.2, B2.1, B2.2, B2.3
- [2015-E1](#/epreuve?id=2015-E1) : 28, 30

### T04 — Harmoniques réseau, THD et puissance déformante

Cartes : tombe dans 9 sujets sur 13 · 15 formules, 6 pièges, 1 schéma(s).  
Relevé 2015–2025 : 5 épreuves, 12 questions (8 en thème principal).  
Formes : justifier/expliquer 6 · compléter document réponse 2 · calcul 2 · conclure/valider 1 · lecture de documentation 1

- [2025-E2](#/epreuve?id=2025-E2) : Q23
- [2024-E1](#/epreuve?id=2024-E1) : — (secondaire : 47)
- [2024-E2](#/epreuve?id=2024-E2) : B10, B11, B12 (secondaire : B13)
- [2023-E1](#/epreuve?id=2023-E1) : — (secondaire : 16, 17)
- [2018-E2](#/epreuve?id=2018-E2) : 7, 8, 9, 12

### T06 — Transformateur (monophasé et triphasé)

Cartes : tombe dans 13 sujets sur 13 · 14 formules, 6 pièges, 1 schéma(s).  
Relevé 2015–2025 : 2 épreuves, 4 questions (0 en thème principal), aucune question dédiée.  
Formes : calcul 2 · compléter document réponse 1 · conclure/valider 1

- [2024-E2](#/epreuve?id=2024-E2) : — (secondaire : B7, B8, B9 ; transformateur « parfait » en amont d'une ligne)
- [2022-E1](#/epreuve?id=2022-E1) : — (secondaire : 22 ; bloc « Transformer » 230 V eff → 15 V eff du DR7)

### T18 — Circuits électroniques - composants (diode, transistor)

Cartes : tombe dans 4 sujets sur 13 · 7 formules, 7 pièges, 1 schéma(s).  
Relevé 2015–2025 : 2 épreuves, 2 questions (1 en thème principal).  
Formes : compléter document réponse 1 · justifier/expliquer 1

- [2025-E2](#/epreuve?id=2025-E2) : — (secondaire : Q24)
- [2022-E1](#/epreuve?id=2022-E1) : 27

### T07 — Hacheurs (1, 2 et 4 quadrants)

Cartes : tombe dans 12 sujets sur 13 · 13 formules, 6 pièges, 1 schéma(s).  
Relevé 2015–2025 : 5 épreuves, 34 questions (23 en thème principal).  
Formes : établir une expression 12 · compléter document réponse 6 · justifier/expliquer 6 · calcul 4 · tracé/chronogramme 2

- [2025-E2](#/epreuve?id=2025-E2) : Q14, Q19, Q24, Q27, Q28, Q29, Q30, Q31, Q32, Q35 (secondaire : Q15, Q18, Q25, Q26, Q37, Q38, Q39, Q40)
- [2024-E1](#/epreuve?id=2024-E1) : — (secondaire : 48)
- [2023-E2](#/epreuve?id=2023-E2) : C3, C4, C5, C6, C7, C8 (secondaire : B3)
- [2022-E1](#/epreuve?id=2022-E1) : 21, 22
- [2022-E2](#/epreuve?id=2022-E2) : 30, 31, 35, 36, 37 (secondaire : 32)

### T08 — Redresseurs (monophasé et triphasé)

Cartes : tombe dans 13 sujets sur 13 · 12 formules, 6 pièges, 1 schéma(s).  
Relevé 2015–2025 : 4 épreuves, 7 questions (3 en thème principal).  
Formes : compléter document réponse 4 · justifier/expliquer 1 · conclure/valider 1 · pédagogie 1

- [2024-E1](#/epreuve?id=2024-E1) : 47, 48, 49
- [2023-E1](#/epreuve?id=2023-E1) : — (secondaire : 16)
- [2022-E2](#/epreuve?id=2022-E2) : — (secondaire : 31, 32)
- [2022-E1](#/epreuve?id=2022-E1) : — (secondaire : 22)

### T09 — Onduleurs (monophasé et triphasé)

Cartes : tombe dans 12 sujets sur 13 · 13 formules, 7 pièges, 1 schéma(s).  
Relevé 2015–2025 : 5 épreuves, 11 questions (5 en thème principal).  
Formes : justifier/expliquer 4 · compléter document réponse 2 · choix/dimensionnement 2 · tracé/chronogramme 1 · calcul 1

- [2025-E2](#/epreuve?id=2025-E2) : Q20, Q21 (secondaire : Q14, Q23)
- [2024-E2](#/epreuve?id=2024-E2) : B13 (secondaire : B12)
- [2023-E1](#/epreuve?id=2023-E1) : 16, 17
- [2021-E2](#/epreuve?id=2021-E2) : — (secondaire : 13)
- [2016-E1](#/epreuve?id=2016-E1) : — (secondaire : 29, 30)

### T20 — Filtres RC/RL - 1er et 2e ordre

Cartes : tombe dans 5 sujets sur 13 · 12 formules, 7 pièges, 1 schéma(s).  
Relevé 2015–2025 : aucune question dédiée dans les 22 épreuves de l'app.

### T19 — AOP (amplificateur opérationnel)

Cartes : tombe dans 4 sujets sur 13 · 12 formules, 7 pièges, 1 schéma(s).  
Relevé 2015–2025 : 3 épreuves, 16 questions (15 en thème principal).  
Formes : établir une expression 8 · calcul 4 · conclure/valider 2 · compléter document réponse 1 · tracé/chronogramme 1

- [2025-E1](#/epreuve?id=2025-E1) : — (secondaire : 59)
- [2024-E2](#/epreuve?id=2024-E2) : E1, E2, E3, E4, E5, E6, E7, E8, E9, E10
- [2023-E2](#/epreuve?id=2023-E2) : F6, F7, F8, F9, F10

### T26 — Modélisation des systèmes linéaires (automatique)

Cartes : tombe dans 9 sujets sur 13 · 10 formules, 7 pièges, 1 schéma(s).  
Relevé 2015–2025 : 8 épreuves, 29 questions (17 en thème principal).  
Formes : établir une expression 11 · calcul 5 · justifier/expliquer 4 · compléter document réponse 4 · conclure/valider 3

- [2025-E2](#/epreuve?id=2025-E2) : Q37, Q38, Q39, Q40, Q41 (secondaire : Q42)
- [2024-E2](#/epreuve?id=2024-E2) : C3, C4, C6 (secondaire : C5, C7)
- [2023-E1](#/epreuve?id=2023-E1) : — (secondaire : 45)
- [2023-E2](#/epreuve?id=2023-E2) : D6 (secondaire : D4, D5)
- [2021-E1](#/epreuve?id=2021-E1) : 14, 15, 31, 32 (secondaire : 19, 20)
- [2017-E1](#/epreuve?id=2017-E1) : 23 (secondaire : 22, 25)
- [2017-E2](#/epreuve?id=2017-E2) : — (secondaire : C1.1)
- [2015-E1](#/epreuve?id=2015-E1) : 10, 11, 12 (secondaire : 13)

### T21 — Fonctions de transfert - Diagramme de Bode

Cartes : tombe dans 8 sujets sur 13 · 13 formules, 8 pièges, 1 schéma(s).  
Relevé 2015–2025 : 2 épreuves, 5 questions (2 en thème principal).  
Formes : lecture de documentation 3 · tracé/chronogramme 1 · calcul 1

- [2024-E2](#/epreuve?id=2024-E2) : — (secondaire : C10, C12)
- [2023-E2](#/epreuve?id=2023-E2) : D4, D7 (secondaire : D8)

### T27 — Systèmes bouclés, correcteurs, stabilité

Cartes : tombe dans 9 sujets sur 13 · 9 formules, 7 pièges, 1 schéma(s).  
Relevé 2015–2025 : 9 épreuves, 31 questions (23 en thème principal).  
Formes : conclure/valider 9 · justifier/expliquer 5 · établir une expression 5 · lecture de documentation 4 · calcul 3

- [2025-E1](#/epreuve?id=2025-E1) : 18 (secondaire : 28)
- [2025-E2](#/epreuve?id=2025-E2) : Q42
- [2024-E2](#/epreuve?id=2024-E2) : C5, C7, C8, C9, C10, C11, C12, C13 (secondaire : C6)
- [2023-E1](#/epreuve?id=2023-E1) : 45, 48, 49 (secondaire : 50)
- [2023-E2](#/epreuve?id=2023-E2) : D8, D9 (secondaire : D6, D7)
- [2022-E2](#/epreuve?id=2022-E2) : 26, 27, 28, 29 (secondaire : 37)
- [2021-E1](#/epreuve?id=2021-E1) : 33
- [2019-E1](#/epreuve?id=2019-E1) : — (secondaire : 13)
- [2015-E1](#/epreuve?id=2015-E1) : 13, 14, 15 (secondaire : 11)

### T11 — Machine à courant continu (MCC)

Cartes : tombe dans 10 sujets sur 13 · 15 formules, 6 pièges, 1 schéma(s).  
Relevé 2015–2025 : 1 épreuves, 2 questions (0 en thème principal).  
Formes : justifier/expliquer 1 · choix/dimensionnement 1

- [2020-E2](#/epreuve?id=2020-E2) : — (secondaire : 16, 18)

### T13 — Machine asynchrone (MAS)

Cartes : tombe dans 7 sujets sur 13 · 17 formules, 7 pièges, 1 schéma(s).  
Relevé 2015–2025 : 8 épreuves, 37 questions (23 en thème principal).  
Formes : calcul 12 · conclure/valider 9 · établir une expression 5 · choix/dimensionnement 3 · justifier/expliquer 3

- [2025-E1](#/epreuve?id=2025-E1) : 54 (secondaire : 60)
- [2024-E2](#/epreuve?id=2024-E2) : A3, A4, A5, A6, A7, A8, C1, C2, D15, D16, D17 (secondaire : A2)
- [2023-E1](#/epreuve?id=2023-E1) : 18, 19 (secondaire : 20, 40)
- [2022-E1](#/epreuve?id=2022-E1) : — (secondaire : 11, 13, 15)
- [2021-E1](#/epreuve?id=2021-E1) : 13, 16, 17, 18, 19, 20, 40 (secondaire : 12, 14)
- [2021-E2](#/epreuve?id=2021-E2) : — (secondaire : 15, 16)
- [2017-E1](#/epreuve?id=2017-E1) : 8 (secondaire : 6)
- [2015-E1](#/epreuve?id=2015-E1) : 19 (secondaire : 18, 22)

### T12 — Machine synchrone et brushless (PMSM,/,BLDC)

Cartes : tombe dans 4 sujets sur 13 · 11 formules, 6 pièges, 1 schéma(s).  
Relevé 2015–2025 : 3 épreuves, 5 questions (3 en thème principal).  
Formes : justifier/expliquer 2 · compléter document réponse 1 · calcul 1 · choix/dimensionnement 1

- [2025-E1](#/epreuve?id=2025-E1) : — (secondaire : 18)
- [2024-E1](#/epreuve?id=2024-E1) : 45, 46 (secondaire : 44)
- [2020-E1](#/epreuve?id=2020-E1) : 8

### T14 — Variation de vitesse et de couple des machines

Cartes : tombe dans 5 sujets sur 13 · 9 formules, 7 pièges, 1 schéma(s).  
Relevé 2015–2025 : 6 épreuves, 18 questions (8 en thème principal).  
Formes : compléter document réponse 4 · établir une expression 3 · choix/dimensionnement 3 · conclure/valider 2 · justifier/expliquer 2

- [2024-E1](#/epreuve?id=2024-E1) : 44 (secondaire : 49)
- [2024-E2](#/epreuve?id=2024-E2) : — (secondaire : B13, C1, C2, C4)
- [2023-E1](#/epreuve?id=2023-E1) : 20, 21 (secondaire : 15, 19, 25)
- [2023-E2](#/epreuve?id=2023-E2) : A7
- [2021-E2](#/epreuve?id=2021-E2) : 15, 16, 18, 19 (secondaire : 17)
- [2017-E1](#/epreuve?id=2017-E1) : — (secondaire : 7)

### T15 — Stockage d'énergie électrique

Cartes : tombe dans 5 sujets sur 13 · 10 formules, 7 pièges, 1 schéma(s).  
Relevé 2015–2025 : 11 épreuves, 58 questions (38 en thème principal).  
Formes : calcul 31 · conclure/valider 10 · choix/dimensionnement 5 · justifier/expliquer 5 · lecture de documentation 2

- [2025-E2](#/epreuve?id=2025-E2) : Q8, Q9, Q10, Q11, Q12, Q13, Q33, Q34 (secondaire : Q35)
- [2024-E1](#/epreuve?id=2024-E1) : 51, 52, 53 (secondaire : 50)
- [2023-E2](#/epreuve?id=2023-E2) : A8, A9, C1, C2, F1 (secondaire : B2, B3, B4, B5)
- [2022-E1](#/epreuve?id=2022-E1) : — (secondaire : 20, 26)
- [2021-E2](#/epreuve?id=2021-E2) : 1, 5, 6, 9, 10, 27, 28 (secondaire : 29)
- [2020-E1](#/epreuve?id=2020-E1) : 20, 21, 22 (secondaire : 16, 19, 30)
- [2020-E2](#/epreuve?id=2020-E2) : 12, 13, 15, 16 (secondaire : 9, 14)
- [2019-E1](#/epreuve?id=2019-E1) : 15, 17, 18, 19, 20 (secondaire : 16, 28)
- [2018-E1](#/epreuve?id=2018-E1) : 20, 21, 22 (secondaire : 23)
- [2016-E1](#/epreuve?id=2016-E1) : — (secondaire : 30)
- [2016-E2](#/epreuve?id=2016-E2) : — (secondaire : 1, 4)

### T17 — Distribution et sécurité électrique, régimes de neutre

Cartes : tombe dans 5 sujets sur 13 · 7 formules, 7 pièges, 1 schéma(s).  
Relevé 2015–2025 : 8 épreuves, 36 questions (26 en thème principal).  
Formes : choix/dimensionnement 11 · calcul 6 · justifier/expliquer 6 · schéma/câblage 5 · établir une expression 4

- [2024-E1](#/epreuve?id=2024-E1) : 38, 39, 41, 42, 43 (secondaire : 40)
- [2024-E2](#/epreuve?id=2024-E2) : B5, B8, B9 (secondaire : B7)
- [2022-E1](#/epreuve?id=2022-E1) : 13, 15 (secondaire : 14)
- [2021-E2](#/epreuve?id=2021-E2) : 17 (secondaire : 18, 19)
- [2020-E2](#/epreuve?id=2020-E2) : 17, 18, 19, 20, 21
- [2018-E2](#/epreuve?id=2018-E2) : 6, 16, 17, 18, 19, 20, 21, 22 (secondaire : 15, 23)
- [2017-E2](#/epreuve?id=2017-E2) : B1.3, B1.4 (secondaire : B2.3)
- [2015-E1](#/epreuve?id=2015-E1) : — (secondaire : 28, 30)

### T23 — Capteurs et Conditionnement du signal

Cartes : tombe dans 9 sujets sur 13 · 4 formules, 6 pièges, 1 schéma(s).  
Relevé 2015–2025 : 11 épreuves, 60 questions (40 en thème principal).  
Formes : calcul 15 · justifier/expliquer 10 · établir une expression 6 · choix/dimensionnement 6 · conclure/valider 6

- [2025-E1](#/epreuve?id=2025-E1) : 25, 26, 55, 56, 57, 58, 59 (secondaire : 29)
- [2024-E1](#/epreuve?id=2024-E1) : 22, 23, 24
- [2024-E2](#/epreuve?id=2024-E2) : D1, D2, D3, D4, D5 (secondaire : E5, E10)
- [2023-E1](#/epreuve?id=2023-E1) : 46, 47, 50 (secondaire : 49, 52)
- [2023-E2](#/epreuve?id=2023-E2) : D2, D3, D5, E1, E2, F2 (secondaire : F4, F10)
- [2022-E1](#/epreuve?id=2022-E1) : 26 (secondaire : 16, 17, 24)
- [2021-E1](#/epreuve?id=2021-E1) : 22, 25, 26 (secondaire : 21, 23, 27)
- [2021-E2](#/epreuve?id=2021-E2) : 20, 21, 22, 25 (secondaire : 23, 24)
- [2020-E1](#/epreuve?id=2020-E1) : 15 (secondaire : 12, 13)
- [2020-E2](#/epreuve?id=2020-E2) : 2, 3, 4, 5, 6, 7, 23 (secondaire : 8, 24)
- [2019-E1](#/epreuve?id=2019-E1) : — (secondaire : 6)

### T22 — CAN/CNA - Numérisation et échantillonnage

Cartes : tombe dans 6 sujets sur 13 · 9 formules, 6 pièges, 1 schéma(s).  
Relevé 2015–2025 : 5 épreuves, 26 questions (17 en thème principal).  
Formes : calcul 12 · compléter document réponse 3 · établir une expression 3 · tracé/chronogramme 2 · lecture de documentation 2

- [2025-E1](#/epreuve?id=2025-E1) : 19, 23, 24, 27, 65 (secondaire : 21, 26, 66)
- [2024-E2](#/epreuve?id=2024-E2) : D6, D7, D8, D9, D10, D11, D12 (secondaire : D14)
- [2023-E2](#/epreuve?id=2023-E2) : F3, F4 (secondaire : D2, D3)
- [2022-E1](#/epreuve?id=2022-E1) : 23, 24 (secondaire : 25, 27, 30)
- [2021-E2](#/epreuve?id=2021-E2) : 23

### T30 — Métrologie, instrumentation, schématisation

Cartes : tombe dans 12 sujets sur 13 · 7 formules, 8 pièges, 1 schéma(s).  
Relevé 2015–2025 : 9 épreuves, 12 questions (4 en thème principal).  
Formes : schéma/câblage 3 · calcul 3 · conclure/valider 3 · pédagogie 2 · justifier/expliquer 1

- [2025-E1](#/epreuve?id=2025-E1) : — (secondaire : 35)
- [2024-E1](#/epreuve?id=2024-E1) : — (secondaire : 54)
- [2022-E1](#/epreuve?id=2022-E1) : 14
- [2021-E2](#/epreuve?id=2021-E2) : — (secondaire : 21, 25)
- [2020-E2](#/epreuve?id=2020-E2) : 8 (secondaire : 7)
- [2019-E2](#/epreuve?id=2019-E2) : 20, 21
- [2018-E2](#/epreuve?id=2018-E2) : — (secondaire : 22)
- [2017-E2](#/epreuve?id=2017-E2) : — (secondaire : B1.4)
- [2015-E1](#/epreuve?id=2015-E1) : — (secondaire : 7)

### T28 — Logique combinatoire

Cartes : tombe dans 3 sujets sur 13 · 3 formules, 6 pièges, 1 schéma(s).  
Relevé 2015–2025 : 3 épreuves, 8 questions (3 en thème principal).  
Formes : compléter document réponse 3 · programmation/algorithme 2 · schéma/câblage 1 · tracé/chronogramme 1 · calcul 1

- [2024-E1](#/epreuve?id=2024-E1) : — (secondaire : 26, 29)
- [2024-E2](#/epreuve?id=2024-E2) : D13 (secondaire : D19, D20, D21)
- [2018-E1](#/epreuve?id=2018-E1) : 26, 27

### T29 — Logique séquentielle, GRAFCET, automates programmables

Cartes : tombe dans 5 sujets sur 13 · 0 formules, 7 pièges, 1 schéma(s).  
Relevé 2015–2025 : 7 épreuves, 12 questions (10 en thème principal).  
Formes : programmation/algorithme 4 · tracé/chronogramme 2 · lecture de documentation 2 · calcul 1 · conclure/valider 1

- [2024-E1](#/epreuve?id=2024-E1) : 69
- [2024-E2](#/epreuve?id=2024-E2) : D20, D21
- [2021-E1](#/epreuve?id=2021-E1) : 29 (secondaire : 30)
- [2021-E2](#/epreuve?id=2021-E2) : 3, 7
- [2019-E1](#/epreuve?id=2019-E1) : 3
- [2017-E1](#/epreuve?id=2017-E1) : 30, 31, 32
- [2017-E2](#/epreuve?id=2017-E2) : — (secondaire : A3)

### T24 — Systèmes embarqués - Microcontrôleurs, API, FPGA

Cartes : tombe dans 6 sujets sur 13 · 2 formules, 6 pièges, 1 schéma(s).  
Relevé 2015–2025 : 17 épreuves, 49 questions (33 en thème principal).  
Formes : programmation/algorithme 24 · schéma/câblage 5 · compléter document réponse 5 · calcul 4 · lecture de documentation 4

- [2025-E1](#/epreuve?id=2025-E1) : 21, 67, 68 (secondaire : 22)
- [2025-E2](#/epreuve?id=2025-E2) : Q5
- [2024-E1](#/epreuve?id=2024-E1) : 68 (secondaire : 23)
- [2024-E2](#/epreuve?id=2024-E2) : D14, D18, D19 (secondaire : D3, D6, D7, D10)
- [2023-E1](#/epreuve?id=2023-E1) : 56, 57 (secondaire : 51, 54)
- [2023-E2](#/epreuve?id=2023-E2) : — (secondaire : E3)
- [2022-E1](#/epreuve?id=2022-E1) : 9, 17, 25 (secondaire : 23)
- [2022-E2](#/epreuve?id=2022-E2) : 20, 21, 22 (secondaire : 23)
- [2021-E1](#/epreuve?id=2021-E1) : 27
- [2021-E2](#/epreuve?id=2021-E2) : 24 (secondaire : 19, 20)
- [2020-E1](#/epreuve?id=2020-E1) : 13, 14
- [2020-E2](#/epreuve?id=2020-E2) : 24, 25
- [2019-E1](#/epreuve?id=2019-E1) : 5, 6 (secondaire : 3, 4)
- [2018-E1](#/epreuve?id=2018-E1) : 23, 24, 25
- [2018-E2](#/epreuve?id=2018-E2) : 24
- [2017-E1](#/epreuve?id=2017-E1) : — (secondaire : 30)
- [2017-E2](#/epreuve?id=2017-E2) : A1, A2, A3, A4, A5

### T25 — Transmission numérique - Modulations et protocoles

Cartes : tombe dans 4 sujets sur 13 · 10 formules, 6 pièges, 1 schéma(s).  
Relevé 2015–2025 : 8 épreuves, 48 questions (42 en thème principal).  
Formes : calcul 15 · lecture de documentation 8 · justifier/expliquer 6 · conclure/valider 6 · compléter document réponse 4

- [2025-E1](#/epreuve?id=2025-E1) : 20, 22, 61, 62, 63, 64, 66, 69, 70, 71 (secondaire : 65, 68)
- [2024-E1](#/epreuve?id=2024-E1) : 25, 26, 27, 28, 29, 30, 31, 32 (secondaire : 33, 34)
- [2023-E1](#/epreuve?id=2023-E1) : 22, 23, 24, 25 (secondaire : 26, 27)
- [2023-E2](#/epreuve?id=2023-E2) : E3, E4, E5, E6, E7, E8
- [2022-E1](#/epreuve?id=2022-E1) : 16, 28, 29, 30, 31
- [2018-E2](#/epreuve?id=2018-E2) : 23, 25, 26
- [2017-E1](#/epreuve?id=2017-E1) : 29
- [2015-E1](#/epreuve?id=2015-E1) : 23, 24, 25, 26, 27

