# 🚀 programmering.no | 🤓 matematikk.as
# S2 - Eksamen - 2023 Vår (NDLA)
# Oppgave 3 a) Coca-Cola vs. Pepsi-Cola - 10 glass 

from scipy.stats import binom

n = 10      # antall forsøk
p = 0.5     # sannsynligheten
X = []      # ei liste for de ulike verdiene X kan ha

for i in range(n+1):
    X.append(i) # legger inn alle de mulige verdiene til X
rettesvar = binom.pmf(X,n,p) # lager en array med sannsynlighetsfordelingen
print("ant :: ", len(X))
print(f"Sannsynligheten for 6 rette svar er {rettesvar[6]:.3f}.") # printer ut svaret
