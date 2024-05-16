# 🚀 programmering.no | 🤓 matematikk.as
# S2 - Eksamen - 2023 Vår (NDLA)
# Oppgave 4 a) Aritmetisk- og geometrisk rekke - Ukentlig beløp de 4 første ukene (alternativ versjon) 

an = 100            # setter startverdi for ukelønna
a = [] 				# lager tom liste for ukelønn tilbud 1
bn = 100            # setter startverdi for ukelønna
b = [] 				# lager tom liste for ukelønn tilbud 2

for i in range(4):	# for-løkke som kjører 4 ganger
	a.append(an) 	# legger til gjeldende ukelønn til lista a
	an = an + 10 	# regner ut ukelønn for neste uke
	b.append(bn) 	# legger til gjeldende ukelønn til lista b
	bn = bn*1.05    # regner ut ukelønn for neste uke

print("Tilbud 1:")
print(a)            # skriver ut lista med ukelønnene
print("Tilbud 2:")
print(b)            # skriver ut lista med ukelønnene
