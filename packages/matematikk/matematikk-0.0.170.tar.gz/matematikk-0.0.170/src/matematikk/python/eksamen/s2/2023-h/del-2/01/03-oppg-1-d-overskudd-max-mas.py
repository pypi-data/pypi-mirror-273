# 🚀 programmering.no | 🤓 matematikk.as
# S2 - Eksamen - 2023 Høst (Matematikk AS)
# Oppgave 1 d) Etterspørsel - Størst overskudd (optimal produksjonsmengde) 
# - Løser oppgaven med CAS i Python
# - Kopier denne kommandoen i terminalen for å importere sympy: 
#   $ pip install sympy

import sympy as sp  

# Variabler
x                   = sp.Symbol("x")        # Etterspørsel (antall produserte enheter)
p                   = sp.Symbol("p")        # Pris per enhet
I                   = sp.Symbol("I")        # Inntekt
K                   = sp.Symbol("K")        # Kostnad
svar_d_ls           = list()                # Svar-setninger
desimal             = None                  # Avrunding

# Definerer uttrykket for pris-funksjonen, p(x)
p = 79 - 12.2 * sp.ln(x)

# Definerer uttrykket for inntekts-funksjonen, I(x)
I = x * p

# Deriverer I mhp. x og får dI = 66.8 - 12.2*log(x)
dI = sp.diff(I, x) # I'(x)

# Definerer uttrykket for kostnads-funksjonen, K(x)
K = 0.021 * x**2 + 10 * x + 910

# Deriverer K mhp. x og får dK = 0.042*x + 10
dK = sp.diff(K, x) # K'(x)

# Lager likningen dI = dK mhp. x med sp.Eq(vs, hs)
likning = sp.Eq(dI, dK)

# Løser likningen med nsolve() og får 79.8935006531202
x_opt = sp.nsolve(likning, x, 1)

# Runder av f.eks. 1234.56789 -> 1234.6
x_opt = round(x_opt, desimal)

# Svar-setninger
svar_d_ls.append(f"")
svar_d_ls.append(f"Oppg d)")
svar_d_ls.append(f"")
svar_d_ls.append(f"- Grense-inntekten er lik grense-kostnaden ved {x_opt} enheter")
svar_d_ls.append(f"- Dette betyr at {x_opt} enheter gir størst overskudd fordi:")
svar_d_ls.append(f"     O`(x) = 0, max overskudd")
svar_d_ls.append(f"     O`(x) = I`(x) - K`(x), definisjonen av overskudd")
svar_d_ls.append(f"     0 = I`(x) - K`(x)")
svar_d_ls.append(f"     K`(x) = I`(x)")

# Print svar-setninger
for svar in svar_d_ls: print(svar)
