# 🚀 programmering.no | 🤓 matematikk.as
# S2 - Eksamen - 2023 Vår (Matematikk AS)
# Oppgave 3 a), b) og c) Coca-Cola vs. Pepsi-Cola 

from scipy.stats import binom
import numpy as np

_blokk = 1
if _blokk == 1:
    n                       = int()   # Forsøk
    p                       = 0.5     # Sannsynlighet
    x_liste                 = []      # Liste med verdiene til x
    fordeling_liste         = []      # Liste med sannsynlighetsfordelingen til x
    riktig                  = 0       # Antall riktige
    riktig_liste            = []      # Liste med antall riktige (flere enn)
    riktig_sannsyn          = float() # Sannsynligheten for å gjette X > riktige
    konfidens               = 0.05    # Konfidens
    desimal                 = 3       # Antall desimaler i avrunding
    _debug_fordeling        = 0       # 0: Ikke debug, 1: Debug
    _debug_fordeling_kum    = 0       # 0: Ikke debug, 1: Debug

# Debug fordelingen (%): Å gjette 1 riktig betyr også å gjette 9 feil (lav sannsynlighet)
def _debugging_fordeling(ls):
    if _debug_fordeling == 1:
        print(""); print("Fordeling")
        for i in range(len(ls)):
            print(ls[i] * 100) # 0, 0, 4, 11, 20, 24, 20, 11, 4, 0, 0

# Debug kumulativ fordelingen (%): Vokser til 100 % (alle gjette-kombinasjoner)
def _debugging_fordeling_kum(ls):
    if _debug_fordeling_kum == 1:
        print(""); print("Kumulativ fordeling")
        for i in range(len(riktig_liste)):
            print(riktig_liste[i] * 100)

# a) Sannsynligheten for å gjette 6 riktige
if _blokk == 1:

    # Verdier
    n = 10
    riktig = 6

    # Legger alle mulige x-verdier i listen: 0 -> 10
    for i in range(n + 1): x_liste.append(i)

    # Liste med fordelingen
    fordeling_liste = binom.pmf(x_liste, n, p)

    fordeling_liste[riktig] = round(fordeling_liste[riktig], desimal)
    print(""); print(f"a) Sannsynlighet for å gjette 6 riktig: {fordeling_liste[riktig]}")

# b) Hypotese-test
if _blokk == 1:

    # Verdier
    n = 10
    riktig = 6

    # Legger alle mulige x-verdier i listen: 0 -> 10
    for i in range(n + 1): x_liste.append(i)

    # Liste med fordelingen
    fordeling_liste = binom.pmf(x_liste, n, p)

    # Debug fordelingen (%): Å gjette 1 riktig betyr også å gjette 9 feil (lav sannsynlighet)
    _debugging_fordeling(fordeling_liste)

    # Liste med kumulative sannsynligheter (større eller mindre)
    riktig_liste = np.cumsum(fordeling_liste)

    # Sannsynligheten for å gjette riktig 8 av 10 er 94 %
    sannsyn_riktige = 1 - riktig_liste[riktig - 1]

    # Ser om kumulativ sannsynlighet for å gjette X > riktig er:
    print("")
    if sannsyn_riktige  > konfidens:
        # 1. Større enn konfidens: Stor sannsynlighet for å gjette riktig / smaker ikke forskjell
        print("b) Det er ikke sannsynlig at Marte smaker forskjell.")
    if sannsyn_riktige <= konfidens:
        # 1. Mindre enn konfidens: Liten sannsynlighet for å gjette riktig / smaker forskjell
        print("b) Det er sannsynlig at Marte smaker forskjell.")

# c) Overbevise Birger
if _blokk == 1:

    # Verdier
    n = 30
    riktig_sannsyn = 1

    # Legger alle mulige x-verdier i listen: 0 -> 10
    for i in range(n + 1): x_liste.append(i)

    # Liste med fordelingen
    fordeling_liste = binom.pmf(x_liste, n, p)

    # Debug fordelingen (%): Å gjette 1 riktig betyr også å gjette 9 feil (lav sannsynlighet)
    _debugging_fordeling(fordeling_liste)

    # Liste med kumulative sannsynligheter (større eller mindre)
    riktig_liste = np.cumsum(fordeling_liste)

    # Debug kumulativ fordelingen (%): Vokser til 100 % (alle gjette-kombinasjoner)
    _debugging_fordeling_kum(riktig_liste)

    # Sannsynligheten for å gjette riktig 8 av 10 er 94 %
    print("")
    while riktig_sannsyn > konfidens:
        riktig_sannsyn = 1 - riktig_liste[riktig]
        riktig += 1

    print(f"c) Må smake riktig minst {riktig} for at det er sannsynlig at hun smaker forskjell")

