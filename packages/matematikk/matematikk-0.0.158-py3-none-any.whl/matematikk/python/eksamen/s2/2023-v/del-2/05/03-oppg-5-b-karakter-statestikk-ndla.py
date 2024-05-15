# 🚀 programmering.no | 🤓 matematikk.as
# S2 - Eksamen - 2023 Vår (NDLA)
# Oppgave 5 b) Karakter-statestikk - Sannsynligheten for et karakter-snitt over karakter 4.0 

import numpy as np
def trekk(n):
    E=[]     #liste for elevenes karakterer
    for i in range(n):
        s = np.random.randint(3) #trekker en av tre skoler
        if s == 0:
            E.append(np.random.normal(3.8,1.2))
        elif s == 1:
            E.append(np.random.normal(3.4,1.4))
        else:
            E.append(np.random.normal(4.1,1.1))
    return np.mean(E)

N = 10000
merennfire = 0
i=0

for i in range(N):
    if trekk(20)>4:
        merennfire = merennfire + 1

print(f"Sannsynligheten for at snittkarakteren er mer enn fire, er {100*merennfire/N:.1f} prosent. ")
