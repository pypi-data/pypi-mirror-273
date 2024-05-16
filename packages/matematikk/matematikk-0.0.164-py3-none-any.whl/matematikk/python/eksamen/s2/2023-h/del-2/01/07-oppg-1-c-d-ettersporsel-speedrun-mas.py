# 🚀 programmering.no | 🤓 matematikk.as
# S2 - Eksamen - 2023 Høst (Matematikk AS)
# Oppgave 1 c) og d) Etterspørsel - SPEEDRUN 
# - Løser oppgaven med CAS i Python
# - Kopier denne kommandoen i terminalen for å importere matematikk: 
#   $ pip install matematikk

import matematikk as mt

_blokk = 1

# Oppg c) - pris_og_enheter_fra_inntekt_max
if _blokk == 1:

    # Funksjon
    def enhet_og_pris_fra_inntekt_max(pris_uttrykk_hs = mt.Symbol("2*x + 1"),
                                      pris_desimal    = -1,
                                      enhet_vari      = mt.Symbol("x"),
                                      enhet_desimal   = None,
                                      enhet_debug     = - 1):

        # Variabler
        x = enhet_vari
        p = pris_uttrykk_hs

        # Definerer uttrykket for inntekts-funksjonen, I(x)
        I = x * p

        # Deriverer I mhp. x og får dI = 66.8 - 12.2*log(x)
        dI = mt.deriver(I, x) # I'(x)

        # Løser likningen dI = 0
        x_inntekt_max = mt.superløs(variabel = x,
                                    vs       = dI,
                                    hs       = 0,
                                    rund     = enhet_desimal,
                                    debug    = enhet_debug)

        # Setter x_inntekt_max = 239 inn i p og definerer det nye uttrykket som p_inntekt_max
        p_inntekt_max = p.subs(x, x_inntekt_max)

        # Henter verdien til p_inntekt_max
        p_inntekt_max_val = p_inntekt_max.evalf()

        # Runder av 12.1871446664356 -> 12.20
        p_inntekt_max_val = round(p_inntekt_max_val, pris_desimal)

        return [x_inntekt_max, p_inntekt_max_val]

    # Antall enheter (etterspørsel) og pris per enhet når inntekten er størst
    enhet_og_pris_ls = enhet_og_pris_fra_inntekt_max(pris_uttrykk_hs = 79 - 12.2 * mt.ln(mt.Symbol("x")),
                                                     pris_desimal    = 2,
                                                     enhet_vari      = mt.Symbol("x"),
                                                     enhet_desimal   = None,
                                                     enhet_debug     = -1)

    # Svar-setninger
    print(f""); print(f"Oppg c)"); print(f"")
    print(f"- Inntekten er størst når etterspørselen er ca. {enhet_og_pris_ls[0]} enheter")
    print(f"- Dette gir en pris på ca. {enhet_og_pris_ls[1]} kr")

# Oppg d)
if _blokk == 1:

    # Funksjon
    def enhet_fra_overskudd_max(kostnad_uttrykk_hs = mt.Symbol("3*x + 4"),
                                pris_uttrykk_hs    = mt.Symbol("2*x + 1"),
                                enhet_vari         = mt.Symbol("x"),
                                enhet_desimal      = None,
                                enhet_debug        = -1):

        # Variabler
        x = enhet_vari
        p = pris_uttrykk_hs
        K = kostnad_uttrykk_hs

        # Definerer uttrykket for inntekts-funksjonen, I(x)
        I = x * p

        # Deriverer I mhp. x og får dI = 66.8 - 12.2*log(x)
        dI = mt.deriver(I, x) # I'(x)

        # Definerer x og uttrykket for kostnads-funksjonen, K(x)


        # Deriverer K mhp. x og får dK = 0.042*x + 10
        dK = mt.deriver(K, x) # K'(x)

        # Løser likningen dI = dK mhp. x
        x_opt = mt.superløs(variabel = x,
                            vs       = dI,
                            hs       = dK,
                            rund     = enhet_desimal,
                            debug    = enhet_debug)

        return x_opt

    # Optimalt antall enheter (ettspørsel) når overskuddet er størst
    x_opt = enhet_fra_overskudd_max(kostnad_uttrykk_hs = 0.021 * mt.Symbol("x")**2 + 10 * mt.Symbol("x") + 910,
                                    enhet_vari         = mt.Symbol("x"),
                                    enhet_desimal      = None,
                                    enhet_debug        = -1)

    # Svar-setninger
    print(f""); print(f"Oppg d)"); print(f"")
    print(f"- Grense-inntekten er lik grense-kostnaden ved {x_opt} enheter")
    print(f"- Dette betyr at {x_opt} enheter gir størst overskudd fordi:")
    print(f"     O`(x) = 0, max overskudd")
    print(f"     O`(x) = I`(x) - K`(x), definisjonen av overskudd")
    print(f"     0 = I`(x) - K`(x) <=> K`(x) = I`(x)")

