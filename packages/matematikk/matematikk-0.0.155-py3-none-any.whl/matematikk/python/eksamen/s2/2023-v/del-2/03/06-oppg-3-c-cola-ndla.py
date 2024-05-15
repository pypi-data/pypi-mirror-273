# 🚀 programmering.no | 🤓 matematikk.as
# S2 - Eksamen - 2023 Vår (NDLA)
# Oppgave 3 c) Coca-Cola vs. Pepsi-Cola - 20 glass 

from scipy.stats import binom
import numpy as np

n = 30      # antall forsøk
p = 0.5     # sannsynligheten
X = []      # ei liste for de ulike verdiene X kan ha

for i in range(n+1):
    X.append(i) # legger inn alle de mulige verdiene til X
rettesvar = binom.pmf(X,n,p) # lager en array med sannsynlighetsfordelingen
merenna = np.cumsum(rettesvar) #finner de kumulative sannsynlighetene
a = 15 #antall rette
sannsynlighet = 1 #starter løkka med sannsynlighet 1

while sannsynlighet > 0.05:
    sannsynlighet = 1 - merenna[a]
    a = a + 1

print(f"Marte må svare rett minst {a} ganger for at det skal være sannsynlig at huns smaker forskjell")
