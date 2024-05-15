# 🚀 programmering.no | 🤓 matematikk.as
# S2 - Eksamen - 2023 Vår (Matematikk AS)
# Oppgave 4 a), b) og c) Aritmetisk- og geometrisk rekke 

_blokk = 1
if _blokk == 1:
    lonn_0      = 100       # Ukelønn første uke
    a_n         = float()   # Tilbud 1: Ukelønn første uke
    a_d         = 10        # Tilbud 1: Aritmetisk økning (differanse)
    a_s         = 0         # Tilbud 1: Aritmetisk sum
    g_n         = float()   # Tilbud 2: Ukelønn første uke
    g_k         = 1.05      # Tilbud 2: Geometrisk økning (kvotient)
    g_s         = 0         # Tilbud 2: Geometrisk sum
    uker        = int()     # Antall uker
    desimal     = 2         # Antall desimaler i avrund

# Print-funksjon
def printing_rader(uker, tilbud, belop): print(f"Uke {uker} | Tilbud {tilbud} | Beløp: {round(belop, desimal)}")

# Oppgave a)
if _blokk == 1:

    # Print
    print("")
    print("Oppg a)")

    # Variabler
    a_n     = lonn_0
    g_n     = lonn_0
    uker    = 4

    # Aritmetisk rekke
    print("")
    for i in range(uker + 1): printing_rader(uker, "1 (A)", a_n); a_n += a_d;

    # Geometrisk rekke
    print("")
    for i in range(uker + 1): printing_rader(uker, "1 (G)", g_n); g_n *= g_k;

# Oppgave b)
if _blokk == 1:

    # Print
    print("")
    print("Oppg b)")

    # Variabler
    a_n     = lonn_0
    g_n     = lonn_0
    uker    = 1

    # Kjøres så lenge geometrisk ukelønn er lavere enn aritmetisk
    while g_n <= a_n:
        printing_rader(uker, "1 (A)", a_n); a_n += a_d  # Aritmetisk formel
        printing_rader(uker, "2 (G)", g_n); g_n *= g_k  # Geometrisk formel
        print("")
        uker += 1    # Uker øker med 1

    # Print svar
    print(f"Etter {uker} uker er geometrisk ukelønn størst ({round(g_n, desimal)} > {a_n})")

# Oppgave c)
if _blokk == 1:

    # Print
    print("")
    print("Oppg c)")

    # Variabler
    a_n     = lonn_0
    g_n     = lonn_0
    uker    = 1

    # Kjøres så lenge geometrisk ukelønn er lavere enn aritmetisk
    while g_s <= a_s:
        a_s  += a_n  # Aritmetisk sum
        a_n  += a_d  # Aritmetisk formel
        g_s  += g_n  # Geometrisk sum
        g_n  *= g_k  # Geometrisk formel
        printing_rader(uker, "1 (A)", a_s);
        printing_rader(uker, "2 (G)", g_s);
        print("")
        uker += 1    # Uker øker med 1

    # Trekker fra 1 uke
    uker -= 1

    # Print svar
    print(f"Etter {uker} uker er den geometrisk summen størst ({round(g_s, desimal)} > {a_s})")
