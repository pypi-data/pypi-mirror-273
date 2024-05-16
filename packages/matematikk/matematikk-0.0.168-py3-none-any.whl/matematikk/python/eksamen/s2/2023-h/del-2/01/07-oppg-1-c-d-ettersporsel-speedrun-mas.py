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

    # Antall enheter (etterspørsel) og pris per enhet når inntekten er størst
    enhet_og_pris_ls = mt.enhet_og_pris_fra_inntekt_max(pris_uttrykk_hs = 79 - 12.2 * mt.ln(mt.Symbol("x")),
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

    # Optimalt antall enheter (ettspørsel) når overskuddet er størst
    x_opt = mt.enhet_fra_overskudd_max(kostnad_uttrykk_hs = 0.021 * mt.Symbol("x")**2 + 10 * mt.Symbol("x") + 910,
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

