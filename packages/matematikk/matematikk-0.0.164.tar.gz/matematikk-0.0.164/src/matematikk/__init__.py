# Versjon: 0.0.163 YOYO

# '''
# numpy()
from numpy import(
    polyfit
    )

# sympy()
from sympy import (
    ConditionSet,
    core,
    diff,
    Eq,
    FiniteSet,
    Intersection,
    ln,
    log,
    nsolve,
    Reals,
    solve,
    solveset,
    Symbol
    )

# deriver()
from ._exports.def_deriver_mas import (
    deriver,

    # Alias > 1
    derivert,
    momentan_vekst,
    momentan_vekstfart
    )

# vekstfaktor_cas()
from ._exports.def_vekstfaktor_cas import (
    vekstfaktor_cas
    )

# reggis()
from ._exports.def_reggis_matematikk_mas import (
    reggis,

    # Alias > 1
    reggis_cas,
    regresjon,
    regresjon_cas,
    regresjon_polynom,
    regresjon_polynom_cas,

    # Alias > 2
    cas_regresjon,
    cas_regresjon_polynom,
    regresjon_polynom_cas
    )

# superlos()
from ._exports.def_superlos_matematikk_mas import (
    superløs,

    # Alias > 1
    los,
    losning,
    løs,
    løsning,
    superlos,
    super_los,
    super_løs,

    # Alias > 2
    los_super,
    løs_super
    )

# ekstremalpunkt_max()
from ._exports.def_ekstremalpunkt_max_mas import (
    ekstremalpunkt_max,

    # Alias > 1
    ekstremalpunkt_maks,
    ekstremalpunkt_maksimalt,
    toppunkt

    # Alias > 2 > ...
    )

# overskudd_max()
from ._exports.def_overskudd_max_mas import (
    overskudd_max,

    # Alias > 1
    overskudd_maks,
    overskudd_maksimalt,
    overskudd_mest,
    overskudd_storst,
    overskudd_størst,

    # Alias > 2
    maks_overskudd,
    maksimalt_overskudd,
    mest_overskudd,
    storst_overskudd,
    størst_overskudd
    )

# enhet_fra_overskudd_max()
from ._exports.def_enhet_fra_overskudd_max_mas import (
    enhet_fra_overskudd_max,

    # Alias > 1
    enhet_fra_max_overskudd

    # Alias > 2 > ...
    )

# enhet_og_pris_fra_inntekt_max()
from ._exports.def_enhet_og_pris_fra_inntekt_max_mas import (
    enhet_og_pris_fra_inntekt_max,

    # Alias > 1
    enhet_og_pris_fra_inntekt_max

    # Alias > 2 > ...
    )

# '''
