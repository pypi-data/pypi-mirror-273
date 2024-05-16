# 🚀 programmering.no | 🤓 matematikk.as
# S2 - Eksamen - 2023 Vår (NDLA)
# Oppgave 5 a) Karakter-statestikk - Normalfordelt karakter-snitt til 20 elever fra 3 skoler 

import numpy as np

E = []     #liste for elevenes karakterer

for i in range(20):
    s = np.random.randint(3) # trekker en av tre skoler

if s == 0:
    E.append(np.random.normal(3.8,1.2))
elif s == 1:
    E.append(np.random.normal(3.4,1.4))
else:
    E.append(np.random.normal(4.1,1.1))
print(f"Gjennomsnittskarakteren er {np.mean(E):.1f}.")
