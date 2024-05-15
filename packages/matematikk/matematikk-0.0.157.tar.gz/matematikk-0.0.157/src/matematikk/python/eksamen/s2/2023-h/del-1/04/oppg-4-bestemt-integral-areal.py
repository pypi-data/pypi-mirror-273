# 🚀 programmering.no | 🤓 matematikk.as
# S2 - Eksamen - 2023 Høst (Udir)
# Oppgave 4) Areal med bestemt integral - Bestemt integral og areal 

N = 1000
start = -2
slutt = 2
dx = (slutt - start)/N

def f(x):
	return x**2-1

S = 0
for i in range(N):
	xi = start + i*dx
	S = S + abs(f(xi))*dx # abs(f(x)) gir absoluttverdien til f(x)

print(S)
