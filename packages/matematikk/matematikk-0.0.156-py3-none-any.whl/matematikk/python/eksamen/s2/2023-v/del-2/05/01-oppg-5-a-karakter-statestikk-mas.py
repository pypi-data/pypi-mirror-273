# 🚀 programmering.no | 🤓 matematikk.as
# S2 - Eksamen - 2023 Vår (Matematikk AS)
# Oppgave 5 a) Karakter-statestikk - Normalfordelt karakter-snitt til 20 elever fra 3 skoler 

import numpy as np

_blokk = 1
if _blokk == 1:
    elev_ant        = 20        # Antall elever vi trekker
    elev_kar        = float()   # Gjenommsnitts-karakter til en elev
    elev_liste      = list()    # Liste med gjenommsnitts-karakterer til elevene
    elev_snitt      = float()   # Snittet av alle elevene
    skole_ant       = 3         # Antall skoler
    skole_a_mu      = 3.8       # Skole A: Forventningsverdi (mu)
    skole_a_st      = 1.2       # Skole A: Standardavvik (st)
    skole_b_mu      = 3.4       # Skole B: Forventningsverdi (mu)
    skole_b_st      = 1.4       # Skole B: Standardavvik (st)
    skole_c_mu      = 4.1       # Skole C: Forventningsverdi (mu)
    skole_c_st      = 1.1       # Skole C: Standardavvik (st)
    desimal         = 2         # Avrunding

# For hver av 20 elevene
for i in range(elev_ant):

    # Trekker tilfeldig skole
    skole_r = np.random.randint(skole_ant)

    # Vi får gjennomsnitskarakter fra numpy sin normalfordeling
    if skole_r == 0: elev_kar = np.random.normal(skole_a_mu, skole_a_st)
    if skole_r == 1: elev_kar = np.random.normal(skole_b_mu, skole_b_st)
    if skole_r == 2: elev_kar = np.random.normal(skole_c_mu, skole_c_st)

    # Liste med gjenommsnitts-karakterer til elevene
    elev_liste.append(elev_kar)

# Snittet av alle elevene
elev_snitt = round(np.mean(elev_liste), desimal)

# Print svar
print(f"Gjennomsnitts-karakteren er: {elev_snitt}")

