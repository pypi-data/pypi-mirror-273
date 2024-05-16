# 🚀 programmering.no | 🤓 matematikk.as
# S2 - Eksamen - 2023 Vår (Udir)
# Oppgave 3 a) Aritmetisk rekke - Sum av n = 10 ledd 

a = 3
d = 4

N = 10
S = 0

for i in range(N):
	S = S + a
	a = a + d

print(S)
