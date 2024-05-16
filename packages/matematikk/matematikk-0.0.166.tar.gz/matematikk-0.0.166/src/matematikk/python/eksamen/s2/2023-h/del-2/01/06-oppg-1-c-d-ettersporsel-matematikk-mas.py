# 🚀 programmering.no | 🤓 matematikk.as
# S2 - Eksamen - 2023 Høst (Matematikk AS)
# Oppgave 1 c) og d) Etterspørsel 
# - Løser oppgaven med CAS i Python
# - Kopier denne kommandoen i terminalen for å importere matematikk: 
#   $ pip install matematikk

import matematikk as mt

# Variabler
_blokk = 1
if _blokk == 1:

    # Variabler
    x                   = mt.Symbol("x")        # Etterspørsel (antall produserte enheter)
    p                   = mt.Symbol("p")        # Pris per enhet
    I                   = mt.Symbol("I")        # Inntekt
    K                   = mt.Symbol("K")        # Kostnad
    svar_c_ls           = list()                # Svar-setninger
    svar_d_ls           = list()                # Svar-setninger
    x_desimal           = None                  # Avrunding (heltall)
    desimal_x_opt       = None                  # Avrunding
    p_desimal           = 1                     # Avrunding

# Felles: Oppg c) og d)
if _blokk == 1:

    # Definerer uttrykket for pris-funksjonen, p(x)
    p = 79 - 12.2 * mt.ln(x)

    # Definerer uttrykket for inntekts-funksjonen, I(x)
    I = x * p

    # Deriverer I mhp. x og får dI = 66.8 - 12.2*log(x)
    dI = mt.deriver(I, x) # I'(x)

# Oppg c)
if _blokk == 1:

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

# Oppg d)
if _blokk == 1:

    # Definerer uttrykket for kostnads-funksjonen, K(x)
    K = 0.021 * x**2 + 10 * x + 910

    # Deriverer K mhp. x og får dK = 0.042*x + 10
    dK = mt.deriver(K, x) # K'(x)

    # Løser likningen dI = dK mhp. x
    x_opt = mt.superløs(variabel = x,
                        vs       = dI,
                        hs       = dK,
                        rund     = desimal_x_opt,
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
