# 🚀 programmering.no | 🤓 matematikk.as
# S2 - Eksamen - 2023 Vår (Udir)
# Oppgave 3 b) Aritmetisk rekke - Sum av n = 100 ledd 

a = 3
d = 4

N = 100
S = 0

for i in range(N):
	S = S + a
	a = a + d

print(S)
