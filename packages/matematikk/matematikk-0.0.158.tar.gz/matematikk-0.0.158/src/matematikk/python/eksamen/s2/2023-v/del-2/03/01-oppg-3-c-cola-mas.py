# 🚀 programmering.no | 🤓 matematikk.as
# S2 - Eksamen - 2023 Vår (Matematikk AS)
# Oppgave 3 c) Coca-Cola vs. Pepsi-Cola - 20 glass 

from scipy.stats import binom
import numpy as np

_blokk = 1
if _blokk == 1:
    n                       = 30      # Antall forsøk
    p                       = 0.5     # Sannsynlighet (sannsyn) for riktig cola-type
    x_liste                 = []      # Liste med alle mulige x-verdier
    x_riktig                = 0       # Antall riktige
    fordeling_liste         = []      # Liste med sannsynlighetsfordelingen til x
    fordeling_liste_kum     = []      # Liste med kumulativ sannsynlighetsfordeling
    sannsyn_riktig_kum      = 1       # Starter på 1 og trekker fra økende x_riktig til liten nok konfidens
    konfidens               = 0.05    # Konfidens
    desimal                 = 3       # Antall desimaler i avrunding
    _debug_fordeling        = 0       # 0: Ikke debug, 1: Debug
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

# While løkken kjører så lenge sannsyn for å gjette riktig er stor (større enn konfidens)
# Bryter ut når antall riktige er så stor at det ikke er enkelt å gjette (lik konfidens)
# x_riktig starter på 0 og trekker fra økende "få" riktige fordi vi vil ha
# konfidensen til mange riktige (vanskelig å gjette riktig) på høyre side av fordelingen
while sannsyn_riktig_kum > konfidens:
    sannsyn_riktig_kum = 1 - fordeling_liste_kum[x_riktig] # Regnes ut fra "skratsj" hver gang
    x_riktig += 1

# Printer svaret
print(f"Må smake riktig minst {x_riktig} for at det er sannsynlig at hun smaker forskjell")
