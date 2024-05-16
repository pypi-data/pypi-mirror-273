# 🚀 programmering.no | 🤓 matematikk.as
# S2 - Eksamen - 2023 Høst (Matematikk AS)
# Oppgave 1 c) Etterspørsel - Størst inntekt 
# - Løser oppgaven med CAS i Python
# - Kopier denne kommandoen i terminalen for å importere matematikk: 
#   $ pip install matematikk

import matematikk as mt
    
# Variabler
x                   = mt.Symbol("x")        # Etterspørsel (antall produserte enheter)
x_desimal           = None                  # Avrunding (heltall)
p                   = mt.Symbol("p")        # Pris per enhet
p_desimal           = 1                     # Avrunding
I                   = mt.Symbol("I")        # Inntekt
svar_c_ls           = list()                # Svar-setninger

# Definerer uttrykket for pris-funksjonen, p(x)
p = 79 - 12.2 * mt.ln(x)

# Definerer uttrykket for inntekts-funksjonen, I(x)
I = x * p

# Deriverer I mhp. x og får dI = 66.8 - 12.2*log(x)
dI = mt.deriver(I, x) # I'(x)

# Løser likningen dI = 0
x_inntekt_max = mt.superløs(variabel = x,
                            vs       = dI,
                            hs       = 0,
                            rund     = x_desimal,
                            debug    = -1)

# Setter x_inntekt_max = 239 inn i p og definerer det nye uttrykket som p_inntekt_max
p_inntekt_max = p.subs(x, x_inntekt_max)

# Henter verdien til p_inntekt_max
p_inntekt_max_val = p_inntekt_max.evalf()

# Runder av 12.1871446664356 -> 12.20
p_inntekt_max_val = round(p_inntekt_max_val, p_desimal)

# Svar-setninger
svar_c_ls.append(f"")
svar_c_ls.append(f"Oppg c)")
svar_c_ls.append(f"")
svar_c_ls.append(f"- Inntekten er størst når etterspørselen er ca. {x_inntekt_max} enheter")
svar_c_ls.append(f"- Dette gir en pris på ca. {p_inntekt_max_val} kr")

# Print svar-setninger
for svar in svar_c_ls: print(svar)
