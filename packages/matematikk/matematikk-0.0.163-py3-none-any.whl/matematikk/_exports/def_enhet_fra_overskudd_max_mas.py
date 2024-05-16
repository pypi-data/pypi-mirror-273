import matematikk as mt

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

    # Deriverer K mhp. x og får dK = 0.042*x + 10
    dK = mt.deriver(K, x) # K'(x)

    # Løser likningen dI = dK mhp. x
    x_opt = mt.superløs(variabel = x,
                        vs       = dI,
                        hs       = dK,
                        rund     = enhet_desimal,
                        debug    = enhet_debug)

    return x_opt

# Alias > 1 ...

# Alias > 2 > ...
enhet_fra_max_overskudd = enhet_fra_overskudd_max
