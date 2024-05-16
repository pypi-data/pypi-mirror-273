# 🚀 programmering.no | 🤓 matematikk.as

import matematikk as mt

def enhet_fra_overskudd_max(variabel = mt.Symbol(""),
                            uttrykk  = mt.Symbol(""),
                            desimal  = None,
                            debug    = -1):

    # overskudd_max() er en undergruppe av ekstremalpunkt_max()
    variabel_max = mt.ekstremalpunkt_max(variabel = variabel,
                                         uttrykk  = uttrykk,
                                         rund     = desimal,
                                         debug    = debug)

    return variabel_max

# Alias > 1
enhet_fra_overskudd_maks          = enhet_fra_overskudd_max
enhet_fra_overskudd_maksimalt     = enhet_fra_overskudd_max
enhet_fra_overskudd_mest          = enhet_fra_overskudd_max
enhet_fra_overskudd_storst        = enhet_fra_overskudd_max
enhet_fra_overskudd_størst        = enhet_fra_overskudd_max

# Alias > 2
enhet_fra_maks_overskudd          = enhet_fra_overskudd_max
enhet_fra_maksimalt_overskudd     = enhet_fra_overskudd_max
enhet_fra_mest_overskudd          = enhet_fra_overskudd_max
enhet_fra_storst_overskudd        = enhet_fra_overskudd_max
enhet_fra_størst_overskudd        = enhet_fra_overskudd_max

