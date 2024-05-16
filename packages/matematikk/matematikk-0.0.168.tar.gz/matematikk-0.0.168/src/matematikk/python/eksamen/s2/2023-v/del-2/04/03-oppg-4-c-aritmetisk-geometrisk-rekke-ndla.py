# 🚀 programmering.no | 🤓 matematikk.as
# S2 - Eksamen - 2023 Vår (NDLA)
# Oppgave 4 c) Aritmetisk- og geometrisk rekke - Uker før tilbud 2 til sammen gir mer lønn enn tilbud 1 

an = 100            # setter startverdi
bn = 100            # setter startverdi
san = an
sbn = bn
n=1
while sbn <= san:
    n = n + 1 # oppdaterer verdien til n
    an = an + 10      # oppdaterer verdien til an
    bn = bn*1.05      # oppdaterer verdien til bn
    san = san + an    # oppdaterer verdien til san
    sbn = sbn + bn    # oppdaterer verdien til sbn

print(f"Etter {n} uker vil hun for første gang ha fått mer "
"til sammen med tilbud 2 enn med tilbud 1.")
