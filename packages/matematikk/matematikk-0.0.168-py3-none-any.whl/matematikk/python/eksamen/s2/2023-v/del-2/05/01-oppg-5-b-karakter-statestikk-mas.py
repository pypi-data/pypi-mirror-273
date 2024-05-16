# 🚀 programmering.no | 🤓 matematikk.as
# S2 - Eksamen - 2023 Vår (Matematikk AS)
# Oppgave 5 b) Karakter-statestikk - Sannsynligheten for et karakter-snitt over karakter 4.0 

import numpy as np

_blokk = 1
if _blokk == 1:
    elev_ant    = 20        # Antall elever som trekkes
    elev_kar    = float()   # Gjennomsnitts-karakteren til tilfeldig elev
    elev_liste  = list()    # Liste for elevenes karakterer
    elev_snitt  = float()   # Karaktersnittet til elevene
    skole_ant   = 3         # Antall skoler
    skole_r     = int()     # Tilfeldig trukket skole
    skole_a_mu  = 3.8       # Skole A: Forventingsverdi (mu)
    skole_b_mu  = 3.4       # Skole B: Forventingsverdi (mu)
    skole_c_mu  = 4.1       # Skole C: Forventingsverdi (mu)
    skole_a_st  = 1.2       # Skole A: Standardavvik (sigma)
    skole_b_st  = 1.4       # Skole B: Standardavvik (sigma)
    skole_c_st  = 1.1       # Skole C: Standardavvik (sigma)
    kar_grense  = 4.0       # Karakter-grense
    kar_gunstig = 0         # Antall topp-karakter
    sim_ant     = 10000     # Antall simulering
    sannyn_kar  = float()   # Sannsynlighet for topp-karakter
    desimal     = 2         # Avrunding

# Funksjon for snitt
def elev_karaktersnitt(n):

    # Resetting
    elev_liste = []

    # For hver av de 20 elevene
    for i in range(n):

        # Trekker eleven tilfeldig fra 1 av 3 skoler
        skole_r = np.random.randint(skole_ant)

        # Regner ut gjennomsnitts-karakteren med numpy
        if skole_r == 0: elev_kar = np.random.normal(skole_a_mu, skole_a_st)
        if skole_r == 1: elev_kar = np.random.normal(skole_b_mu, skole_b_st)
        if skole_r == 2: elev_kar = np.random.normal(skole_c_mu, skole_c_st)

        # Legger karakteren i karakter-listen
        elev_liste.append(elev_kar)

    # Regner ut gjennomsnittet til de 20 elevene
    elev_snitt = round(np.mean(elev_liste), desimal)

    return elev_snitt

# Simulering
for i in range(sim_ant):

    # Snittet fra n elever
    elev_snitt = elev_karaktersnitt(elev_ant)

    # Øk med en for hver topp-karakter
    if elev_snitt > kar_grense: kar_gunstig += 1

# Sannsynlighet for topp-karakter: P = g / m
sannyn_kar = (kar_gunstig / sim_ant) * 100

# Avrunding
sannyn_kar = round(sannyn_kar, desimal)

# Print svar
print(f"Sannsynlighet for {kar_grense} er: {sannyn_kar} %")
