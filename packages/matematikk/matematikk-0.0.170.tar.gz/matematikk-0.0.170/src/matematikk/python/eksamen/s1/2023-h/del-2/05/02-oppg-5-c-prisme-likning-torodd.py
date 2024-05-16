# 🚀 programmering.no | 🤓 matematikk.as
# S1 - Eksamen - 2023 Høst (Torodd)
# Oppgave 5 c) Volum av prisme - Minste samlede areal til platene når kassen er 80 cm^3 

from sympy import Symbol, diff, solve, solveset, Eq, Reals

# definerer symboler
s = Symbol("s")
h = Symbol("h")

# Set opp likningane
A = s**2 + 4*s*h
V = s**2 * h

# Finn uttrykk for h når A=120 og s=5
A_2 = A.subs(s, 5)
likning = Eq(A_2, 120)
løysing = solveset(likning, h, domain=Reals)
print(løysing)
