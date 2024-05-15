# 🚀 programmering.no | 🤓 matematikk.as
# S2 - Eksamen - 2023 Vår (NDLA)
# Oppgave 3 b) Coca-Cola vs. Pepsi-Cola - Hypotese-test 

from scipy.stats import binom
import numpy as np

n = 10      # antall forsøk
p = 0.5     # sannsynligheten
X = []      # ei liste for de ulike verdiene X kan ha

for i in range(n+1):
    X.append(i) # legger inn alle de mulige verdiene til X
rettesvar = binom.pmf(X,n,p) # lager en array med sannsynlighetsfordelingen
merenna = np.cumsum(rettesvar) #finner de kumulative sannsynlighetene
a = 8 #antall rette

# sjekker om summen av sannsynlighetene for X>a er
# større eller mindre enn 0.05
if 1 - merenna[a-1] < 0.05:
    print("Det er sannsynlig at Marte kan gjenkjenne de to colatype.")
else:
    print("Det er ikke sannsynlig at Marte kan gjenkjenne de to colatype.")
