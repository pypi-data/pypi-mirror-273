# 🚀 programmering.no | 🤓 matematikk.as
# S2 - Eksamen - 2023 Vår (NDLA)
# Oppgave 4 b) Aritmetisk- og geometrisk rekke - Uker før tilbud 2 gir mer ukelønn enn tilbud 1 

an = 100            # setter startverdi
bn = 100            # setter startverdi
n = 1               # setter startverdi
while bn <= an:
    n = n + 1       # oppdaterer verdien til n
    an = an + 10    # oppdaterer verdien til an
    bn = bn*1.05    # oppdaterer verdien til bn

print(f"I den {n} uka får hun for første gang mer med tilbud 2.")
