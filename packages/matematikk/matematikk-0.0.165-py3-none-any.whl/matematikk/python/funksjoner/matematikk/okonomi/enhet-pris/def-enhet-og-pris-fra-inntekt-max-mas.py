import matematikk as mt

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

# Alias > 1 ...

# Alias > 2 > ...
enhet_og_pris_fra_inntekt_max = enhet_og_pris_fra_inntekt_max

