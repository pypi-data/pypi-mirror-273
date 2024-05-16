# 🚀 programmering.no | 🤓 matematikk.as
# S2 - Eksamen - 2023 Høst (Matematikk AS)
# Oppgave 1 d) Etterspørsel - Størst overskudd (optimal produksjonsmengde) 
# - Løser oppgaven med CAS i Python
# - Kopier denne kommandoen i terminalen for å importere sympy: 
#   $ pip install sympy

import matematikk as mt

# Variabler
x                   = mt.Symbol("x")        # Etterspørsel (antall produserte enheter)
p                   = mt.Symbol("p")        # Pris per enhet
I                   = mt.Symbol("I")        # Inntekt
K                   = mt.Symbol("K")        # Kostnad
svar_d_ls           = list()                # Svar-setninger
desimal             = None                  # Avrunding

# Definerer uttrykket for pris-funksjonen, p(x)
p = 79 - 12.2 * mt.ln(x)

# Definerer uttrykket for inntekts-funksjonen, I(x)
I = x * p

# Deriverer I mhp. x og får dI = 66.8 - 12.2*log(x)
dI = mt.deriver(I, x) # I'(x)

# Definerer uttrykket for kostnads-funksjonen, K(x)
K = 0.021 * x**2 + 10 * x + 910

# Deriverer K mhp. x og får dK = 0.042*x + 10
dK = mt.deriver(K, x) # K'(x)

# Løser likningen dI = dK mhp. x
x_opt = mt.superløs(variabel = x,
                    vs       = dI,
                    hs       = dK,
                    rund     = desimal,
                    debug    = -1)

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
