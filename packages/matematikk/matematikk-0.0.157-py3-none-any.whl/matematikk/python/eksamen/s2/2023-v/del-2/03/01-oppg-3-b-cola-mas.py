# 🚀 programmering.no | 🤓 matematikk.as
# S2 - Eksamen - 2023 Vår (Matematikk AS)
# Oppgave 3 b) Coca-Cola vs. Pepsi-Cola - Hypotese-test 

from scipy.stats import binom
import numpy as np

_blokk = 1
if _blokk == 1:
    n                       = 10      # Antall forsøk
    p                       = 0.5     # Sannsynlighet (sannsyn) for riktig cola-type
    x_liste                 = []      # Liste med alle mulige x-verdier
    x_riktig                = 8       # Antall riktige
    fordeling_liste         = []      # Liste med sannsynlighetsfordelingen til x
    fordeling_liste_kum     = []      # Liste med kumulativ sannsynlighetsfordeling
    sannsyn_riktig_kum      = 0       # Sannsyn for å gjette X > riktige
    konfidens               = 0.05    # Konfidens
    desimal                 = 3       # Antall desimaler i avrunding
    _debug_fordeling        = 1       # 0: Ikke debug, 1: Debug
    _debug_fordeling_kum    = 0       # 0: Ikke debug, 1: Debug

def _debugging(ls, txt):
    print(""); print(txt)
    for i in range(len(ls)): print(ls[i] * 100)

# Legger alle x-verdiene i listen: 0, 1, 2, ... 10 (0 er ingen rette)
for i in range(n + 1): x_liste.append(i)

# Liste med fordelingen: 0, 0, 4, 11, 20, 24, 20, 11, 4, 0, 0
fordeling_liste = binom.pmf(x_liste, n, p)

# Debugger fordelingen (%): Å gjette 1 riktig betyr også å gjette 9 feil (lav sannsynlighet)
if _debug_fordeling == 1: _debugging(fordeling_liste, "Fordeling")

# Liste med kumulativ fordeling: Større eller mindre => Summere flere sannsyn
fordeling_liste_kum = np.cumsum(fordeling_liste)

# Debugger kumulativ fordeling (%): Vokser til 100 % ("mindre eller lik alle")
if _debug_fordeling_kum == 1: _debugging(fordeling_liste_kum, "Kumulativ fordeling")

# Sannsyn for å gjette minst riktig 8 av 10 er 94 %
# Vi antar mao. her at hun ikke gjetter, men kan smake forskjell (på alle!)
# Derfor summerer vi sannsyn fra 8 til 10
# Fra 8 (og f.eks. ikke 9) fordi dette var "feilmarginen" i hennes smaks-kompetanse
sannsyn_riktig_kum = 1 - fordeling_liste_kum[x_riktig - 1] # - 1 fordi starter på 0

# Ser om kumulativ sannsynlighet for å gjette X > x_riktig er:
if sannsyn_riktig_kum  > konfidens:
    # 1. Større enn konfidens: Stor sannsynlighet for å gjette x_riktig => smaker ikke forskjell
    print("Det er ikke sannsynlig at Marte smaker forskjell.")
if sannsyn_riktig_kum <= konfidens:
    # 1. Mindre enn konfidens: Liten sannsynlighet for å gjette x_riktig => smaker forskjell
    print("Det er sannsynlig at Marte smaker forskjell.")
