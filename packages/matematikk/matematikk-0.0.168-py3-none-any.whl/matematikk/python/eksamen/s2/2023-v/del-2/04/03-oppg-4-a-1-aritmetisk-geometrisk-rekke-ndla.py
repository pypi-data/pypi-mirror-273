# 🚀 programmering.no | 🤓 matematikk.as
# S2 - Eksamen - 2023 Vår (NDLA)
# Oppgave 4 a) Aritmetisk- og geometrisk rekke - Ukentlig beløp de 4 første ukene 

an = 100                # setter startverdi for ukelønna
print("Tilbud 1:")

for i in range(4):      # for-løkke som kjører 4 ganger
    print(an)           # skriver ut ukelønna
    an = an + 10        # regner ut ukelønn for neste uke

bn = 100                # setter startverdi for ukelønna
print("Tilbud 2:")
for i in range(4):      # for-løkke som kjører 4 ganger
    print(bn)           # skriver ut ukelønna
    bn = bn*1.05        # regner ut ukelønn for neste uke
