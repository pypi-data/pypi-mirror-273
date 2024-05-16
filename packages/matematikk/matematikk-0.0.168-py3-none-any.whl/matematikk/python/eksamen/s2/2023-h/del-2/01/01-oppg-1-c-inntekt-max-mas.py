# 🚀 programmering.no | 🤓 matematikk.as
# S2 - Eksamen - 2023 Høst (Matematikk AS)
# Oppgave 1 c) Etterspørsel - Størst inntekt 
# - Løser oppgaven med CAS i Python
# - Kopier denne kommandoen i terminalen for å importere sympy: 
#   $ pip install sympy

import sympy as sp

# Variabler
x                   = sp.Symbol("x")        # Etterspørsel (antall produserte enheter)
p                   = sp.Symbol("p")        # Pris per enhet
I                   = sp.Symbol("I")        # Inntekt
svar_c_ls           = list()                # Svar-setninger
desimal             = 1                     # Avrunding

# Definerer uttrykket for pris-funksjonen, p(x)
p = 79 - 12.2 * sp.ln(x)

# Definerer uttrykket for inntekts-funksjonen, I(x)
I = x * p

# Deriverer I mhp. x og får dI = 66.8 - 12.2*log(x)
dI = sp.diff(I, x) # I'(x)

# Lager likningen dI = 0 med sp.Eq(vs, hs)
likning = sp.Eq(dI, 0)

# Løser likningen for x med solveset() og får løsnings-settet {238.748294544347}
x_inntekt_max_set = sp.solveset(likning, x, domain=sp.Reals) # Løsnings-domene i ℝ (Reals)

# Henter elementet i fra løsnings-settet, 238.748294544347
x_inntekt_max = x_inntekt_max_set.args[0]

# Runder av 238.748294544347 -> 239
x_inntekt_max = round(x_inntekt_max, None)

# Setter x_inntekt_max = 239 inn i p og definerer det nye uttrykket som p_inntekt_max
p_inntekt_max = p.subs(x, x_inntekt_max)

# Henter verdien til p_inntekt_max
p_inntekt_max_val = p_inntekt_max.evalf()

# Runder av 12.1871446664356 -> 12.20
p_inntekt_max_val = round(p_inntekt_max_val, desimal)

# Svar-setninger
svar_c_ls.append(f"")
svar_c_ls.append(f"Oppg c)")
svar_c_ls.append(f"")
svar_c_ls.append(f"- Inntekten er størst når etterspørselen er ca. {x_inntekt_max} enheter")
svar_c_ls.append(f"- Dette gir en pris på ca. {p_inntekt_max_val} kr")

# Print svar-setninger
for svar in svar_c_ls: print(svar)
